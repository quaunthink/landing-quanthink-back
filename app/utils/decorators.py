# backend/app/utils/decorators.py

from functools import wraps
from flask import request, jsonify, current_app
import jwt

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')

        if not token:
            return jsonify({'message': 'Falta el token de autenticación'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            if data.get('role') != 'admin':
                return jsonify({'message': 'Permisos de administrador requeridos'}), 403
            
            # Puedes pasar el id del usuario a la ruta si lo necesitas
            # kwargs['current_user_id'] = data['user_id']

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated_function