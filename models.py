from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ck_value = db.Column(db.Float, nullable=False)
    transaminase = db.Column(db.Float, nullable=False)
    bilirubin = db.Column(db.Float, nullable=False)
    muscle_symptoms = db.Column(db.Boolean, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())