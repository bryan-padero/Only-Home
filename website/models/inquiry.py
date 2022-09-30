from website import db
from datetime import datetime


class Inquiry(db.Model):
    __tablename__ = "inquiry"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(250), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"))
    inquirer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
