# backend/app/api/routes.py
from flask import Blueprint, jsonify, request
from app.models import Demo

api_bp = Blueprint('api', __name__)

@api_bp.route('/demos', methods=['GET'])
def get_demos():
    demos_from_db = Demo.query.all()

    demos_list = [
        {
            "id": demo.id,
            "title": demo.title,
            "description": demo.description,
            "imageUrl": demo.image_url # <-- Asegurarse que se envía la URL
        }
        for demo in demos_from_db
    ]

    return jsonify(demos_list)