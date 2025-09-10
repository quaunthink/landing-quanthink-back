# backend/app/admin/routes.py
from flask import Blueprint, jsonify, request, current_app
from app.utils.decorators import admin_required
from app.models import Demo
from app import db
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/demos', methods=['POST'])
@admin_required
def create_demo():
    # Los datos de texto ahora vienen en request.form
    title = request.form.get('title')
    description = request.form.get('description')

    if not title or not description:
        return jsonify({"message": "Título y descripción son requeridos"}), 400

    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            # Guardamos la URL para acceder al archivo
            image_url = f"/uploads/{filename}"

    new_demo = Demo(title=title, description=description, image_url=image_url)
    db.session.add(new_demo)
    db.session.commit()

    return jsonify({"message": "Demo creado exitosamente"}), 201

@admin_bp.route('/demos/<int:demo_id>', methods=['PUT'])
@admin_required
def update_demo(demo_id):
    demo_to_update = Demo.query.get(demo_id)
    if not demo_to_update:
        return jsonify({"message": "Demo no encontrado"}), 404

    title = request.form.get('title')
    description = request.form.get('description')

    if not title or not description:
        return jsonify({"message": "Título y descripción son requeridos"}), 400

    demo_to_update.title = title
    demo_to_update.description = description

    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            demo_to_update.image_url = f"/uploads/{filename}"

    db.session.commit()
    return jsonify({"message": "Demo actualizado exitosamente"}), 200

@admin_bp.route('/demos/<int:demo_id>', methods=['DELETE'])
@admin_required
def delete_demo(demo_id):
    demo_to_delete = Demo.query.get(demo_id)
    if not demo_to_delete:
        return jsonify({"message": "Demo no encontrado"}), 404

    db.session.delete(demo_to_delete)
    db.session.commit()

    return jsonify({"message": f"Demo con ID {demo_id} eliminado exitosamente"}), 200