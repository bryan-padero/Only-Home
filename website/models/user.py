from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.DateTime(100))
    profile_pic = db.Column(db.String(100))
    mobile = db.Column(db.String(100))
    property = db.relationship("Property", backref="owner")
    inquiry = db.relationship("User", backref="inquirer")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime(timezone=True))




