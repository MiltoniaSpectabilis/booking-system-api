from flask import Flask
from app.utils.database import init_db
from app.routes import users_bp, rooms_bp, bookings_bp, auth_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(rooms_bp, url_prefix="/api")
app.register_blueprint(bookings_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

init_db()

if __name__ == "__main__":
    app.run(debug=True)
