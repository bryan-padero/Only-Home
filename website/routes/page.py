from flask import Blueprint, flash, render_template, redirect, url_for, request
from website import db
from ..models.property import Property

page = Blueprint("page", __name__)


@page.route("/property_page")
def property_page():
    property_id = request.args.get("property_id")
    selected_property = Property.query.get(property_id)
    return render_template("property_page.html", selected_property=selected_property)
