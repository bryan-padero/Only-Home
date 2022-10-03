from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime


class Property(db.Model):
    __tablename__ = "property"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    property_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    floor_plan = db.Column(db.String(100))
    property_type = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    payment_mode = db.Column(db.String(100), nullable=False)
    furnishing = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Integer, nullable=False)
    num_of_bed = db.Column(db.Integer, nullable=False)
    num_of_bath = db.Column(db.Integer, nullable=False)
    num_of_garage = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime(timezone=True))
    is_verified = db.Column(db.Boolean, default=False)
    images = db.relationship("ImageSet", backref="property_image")
    amenities = db.relationship("Amenity", backref="property_amenity")
    inquiries = db.relationship("Inquiry", backref="property_inquiry")


class Amenity(db.Model):
    __tablename__ = "amenity"
    id = db.Column(db.Integer, primary_key=True)
    amenity_name = db.Column(db.String(100))
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)


class ImageSet(db.Model):
    __tablename__ = "imageset"
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(100))
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
