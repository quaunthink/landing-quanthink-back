# backend/app/models.py

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRole(enum.Enum):
    ADMIN = 'admin'
    CLIENT = 'client'

class User(db.Model):
    # El nombre de la tabla debe ser explícito para evitar conflictos con la palabra reservada 'user'
    __tablename__ = 'users' 
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Aumentamos el tamaño para hashes más largos y seguros
    password_hash = db.Column(db.String(256)) 
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CLIENT)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))