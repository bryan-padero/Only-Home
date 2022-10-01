from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from website.forms import PropertyPageForm, ReviewForm
from website.models.property import Property
from website.models.inquiry import Inquiry
from website.models.user import User, Review
from website import db

page = Blueprint("page", __name__)


@page.route("/property_page", methods=["POST", "GET"])
def property_page():
    property_id = request.args.get("property_id")
    selected_property = Property.query.get_or_404(property_id)
    selected_property_amenities = selected_property.amenities
    form = PropertyPageForm(
        message=f"I would like to inquire about your property OnlyHome - (Property ID: {selected_property.id}) {selected_property.property_title}."
                f" Please contact me at your earliest convenience.")
    context = {
        "selected_property": selected_property,
        "selected_property_amenities": selected_property_amenities,
        "form": form,
        "title_page": "Property Page"
    }
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_inquiry = Inquiry(name=form.name.data,
                                  email=form.email.data,
                                  mobile=form.mobile.data,
                                  message=form.message.data,
                                  property_id=selected_property.id,
                                  inquirer_id=current_user.id)
            db.session.add(new_inquiry)
            db.session.commit()
            flash("Message sent", "success")
            return redirect(url_for("page.property_page", property_id=property_id))
        else:
            flash("Please login first to inquire", "danger")
            return redirect(url_for("auth.login"))
    return render_template("property_page.html", **context)


@page.route("/review", methods=["POST", "GET"])
@login_required
def review():
    owner_id = request.args.get("owner_id")
    owner = User.query.get_or_404(owner_id)
    form = ReviewForm(name=f"{current_user.first_name} {current_user.last_name}",
                      email=current_user.email)
    form.mobile.data = owner.mobile if owner.mobile else "N/A"
    context = {
        "title_page": "Review",
        "form": form,
        "owner": owner,
    }
    if form.validate_on_submit():
        rating = request.form["rating"]
        new_review = Review(comment=form.comment.data,
                            rating=rating,
                            reviewer_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()
        flash("Review submitted", "success")
    return render_template("review.html", **context)
