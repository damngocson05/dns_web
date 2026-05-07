from models.db import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FullName = db.Column(db.Unicode(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(15), nullable=True)
    Address = db.Column(db.Unicode(255), nullable=True)
    Role = db.Column(db.String(20), default='Customer')
    CreatedAt = db.Column(db.DateTime, default=datetime.now)

    def get_id(self):
        return str(self.UserID)