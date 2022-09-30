from website.models.inquiry import *
from website import db
from datetime import datetime
from flask_login import UserMixin


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
    inquiry = db.relationship("Inquiry", backref="inquirer")
    my_review = db.relationship("MyReview", backref="reviewer")
    user_review = db.relationship("UserReview", backref="reviewee")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime(timezone=True))


class MyReview(db.Model):
    __tablename__ = "my_review"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.now)


class UserReview(db.Model):
    __tablename__ = "user_review"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    reviewee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.now)




