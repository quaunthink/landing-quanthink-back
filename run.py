from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()

from app import db
from app.models import Demo, User, UserRole # <-- Asegúrate que User y UserRole estén importados

@app.cli.command("seed-db")
def seed_db():
    """Añade datos de prueba a la base de datos."""
    # Limpiar datos existentes para evitar duplicados
    Demo.query.delete()
    User.query.delete()

    print("Añadiendo demo de prueba...")
    demo1 = Demo(title="Demo desde la Base de Datos", description="Este contenido es servido por PostgreSQL.")
    db.session.add(demo1)

    print("Añadiendo usuario admin...")
    # Creamos un usuario admin con una contraseña
    admin_user = User(email="admin@quanthink.com", role=UserRole.ADMIN)
    admin_user.set_password("supersecret") # <-- La contraseña se hashea automáticamente
    db.session.add(admin_user)

    db.session.commit()
    print("¡Datos de prueba añadidos!")