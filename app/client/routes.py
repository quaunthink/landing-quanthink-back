from flask import Blueprint, jsonify

client_bp = Blueprint('client', __name__)

@client_bp.route('/dashboard', methods=['GET'])
def client_dashboard():
    return jsonify({"message": "Panel de Cliente"})