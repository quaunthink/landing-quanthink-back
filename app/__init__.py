# backend/app/__init__.py

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # CORS con credenciales (para cookies HttpOnly)
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True
    )

    # Carpeta de uploads
    upload_folder = app.config.get('UPLOAD_FOLDER') or os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # Blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from .client.routes import client_bp
    app.register_blueprint(client_bp, url_prefix='/client')

    # Archivos subidos
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/test')
    def test_page():
        return '<h1>Backend funcionando</h1>'

    return app
