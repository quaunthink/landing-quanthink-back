# backend/app/auth/routes.py

from flask import Blueprint, request, jsonify, current_app, make_response
from app.models import User, UserRole
from app import db
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

def _make_token_response(user):
    """Crea el JWT, lo guarda en cookie HttpOnly y devuelve JSON con el usuario."""
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    is_secure_cookie = not current_app.debug  # Secure=True en producción
    resp = make_response(jsonify({
        "ok": True,
        "user": {"id": user.id, "email": user.email, "role": user.role.value}
    }))
    resp.set_cookie(
        "access_token_cookie",
        value=token,
        httponly=True,
        secure=is_secure_cookie,
        samesite="Lax",
    )
    return resp

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role_raw = (data.get("role") or "client").strip().lower()

    if not email or not password:
        return jsonify({"message": "Email y contraseña son requeridos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "El correo ya está registrado"}), 409

    try:
        role = UserRole.ADMIN if role_raw == "admin" else UserRole.CLIENT
        user = User(email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return _make_token_response(user)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al registrar: {e}"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "Email y contraseña son requeridos"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Credenciales inválidas"}), 401

    return _make_token_response(user)

@auth_bp.route("/me", methods=["GET"])
def me():
    token = request.cookies.get("access_token_cookie")
    if not token:
        return jsonify({"ok": False}), 401

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({
            "ok": True,
            "user": {"id": data["user_id"], "email": data["email"], "role": data["role"]}
        })
    except jwt.ExpiredSignatureError:
        return jsonify({"ok": False, "message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"ok": False, "message": "Token inválido"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logout exitoso"}))
    resp.set_cookie("access_token_cookie", value="", expires=0)
    return resp
