from flask import Blueprint, flash, render_template, redirect, url_for, request
from ..forms import PropertyPageForm
from ..models.property import *

page = Blueprint("page", __name__)


@page.route("/property_page")
def property_page():
    form = PropertyPageForm()
    property_id = request.args.get("property_id")
    selected_property = Property.query.get(property_id)
    selected_property_amenities = Amenity.query.filter_by(property_id=property_id).all()
    return render_template("property_page.html", selected_property=selected_property, form=form,
                           selected_property_amenities=selected_property_amenities, title_page="Product Page")
