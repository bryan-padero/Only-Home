from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user
from website.forms import PropertyPageForm, ReviewForm
from website.models.property import Property
from website.models.inquiry import Inquiry
from website.models.user import User, Review
from website.extensions import db, or_, func

page = Blueprint("page", __name__)


@page.route("/property_page", methods=["POST", "GET"])
def property_page():
    property_id = request.args.get("property_id")
    selected_property = Property.query.get_or_404(property_id)
    selected_property_amenities = selected_property.amenities
    print(len(selected_property.owner.received_review))
    form = PropertyPageForm(
        message=f"I would like to inquire about your property OnlyHome - (Property ID: {selected_property.id})"
                f" {selected_property.property_title}."
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


def get_average_rating(owner):
    rating = [owner_review.rating for owner_review in owner.received_review]
    avg_rating = float((sum(rating) / len(rating))) if owner.received_review else None
    return avg_rating


@page.route("/review", methods=["POST", "GET"])
def review():
    owner_id = request.args.get("owner_id")
    owner = User.query.get_or_404(owner_id)
    page_num = request.args.get("page_num")
    avg_rating = get_average_rating(owner)
    avg_rating = round(avg_rating, 1) if avg_rating else None
    page_num = 1 if page_num is None else int(page_num)
    paginate_reviews = Review.query.filter(Review.reviewee_id == owner.id).paginate(page=page_num,
                                                                                    per_page=3, error_out=True)
    if current_user.is_authenticated:
        form = ReviewForm(name=f"{current_user.first_name} {current_user.last_name}",
                          email=current_user.email)
        form.mobile.data = current_user.mobile if current_user.mobile else "N/A"
    else:
        form = ReviewForm()
    context = {
        "title_page": "Review",
        "form": form,
        "owner": owner,
        "avg_rating": avg_rating,
        "paginate_reviews": paginate_reviews,
    }
    if form.validate_on_submit():
        if current_user.is_authenticated:
            rating = request.form["rating"]
            new_review = Review(comment=form.comment.data,
                                rating=rating,
                                reviewer_id=current_user.id,
                                reviewee_id=owner.id)
            db.session.add(new_review)
            db.session.commit()
            flash("Review submitted", "success")
        else:
            flash("Please login first to submit review", "danger")
    return render_template("review.html", **context)


def clean_query_list(query_list):
    query_list = [query[0] for query in query_list]
    return query_list


@page.route("/property_grid", methods=["POST", "GET"])
def property_grid():
    all_properties = Property.query.all()
    search_query = request.form.get("search_query")
    available_cities = clean_query_list(db.session.query(Property.city).distinct().all())
    available_property_types = clean_query_list(db.session.query(Property.property_type).distinct().all())
    available_num_of_baths = clean_query_list(db.session.query(Property.num_of_bath).distinct().all())
    available_num_of_beds = clean_query_list(db.session.query(Property.num_of_bed).distinct().all())
    available_num_of_garages = clean_query_list(db.session.query(Property.num_of_garage).distinct().all())
    available_furnishings = clean_query_list(db.session.query(Property.furnishing).distinct().all())
    available_payment_modes = clean_query_list(db.session.query(Property.payment_mode).distinct().all())

    if request.method == "POST":
        all_properties = Property.query.filter(
            or_(Property.location.like(f"%{search_query}%"), Property.zip_code.like(f"%{search_query}%"),
                Property.city.like(f"%{search_query}%"))).all()
    context = {
        "title_page": "Properties",
        "all_properties": all_properties,
        "available_cities": available_cities,
        "available_property_types": available_property_types,
        "available_num_of_baths": available_num_of_baths,
        "available_num_of_beds": available_num_of_beds,
        "available_num_of_garages": available_num_of_garages,
        "available_furnishings": available_furnishings,
        "available_payment_modes": available_payment_modes,
    }
    return render_template("property_grid.html", **context)


