from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from website.forms import *
from website.models.property import *
from website import db
import os


account = Blueprint("account", __name__)

AMENITY_LIST = ["Central A/C", "Central Heating", "Chiller Free", "Balcony", "Private Gym", "Shared Pool",
                "Pets Allowed", "Private Garden", "Security", "Covered Parking", "Prayer Room", "Satellite/Cable TV",
                "View of Water", "Day Care Center", "Service Elevators", "ATM Facility", "Kids Play Area", "Reception",
                "Maintenance Staff", "CCTV Security", "Cafeteria or Canteen", "Cleaning Services", "Maids Room",
                "Lobby in Building", "Waste Disposal", "Women's Pool", "Women's Gym", "Shared Sauna"]


@account.route("/")
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template("index.html", register_form=register_form, login_form=login_form, title_page="Home")


def save_image(image_file, img_dir):
    image_name = secure_filename(image_file.filename)
    image_path = os.path.join(account.root_path, f'../static/assets/img/{img_dir}', image_name)
    image_file.save(image_path)
    return image_name


def post_new_property(form):
    new_property = Property(owner=current_user,
                            property_title=form.title.data,
                            description=form.description.data,
                            property_type=form.type.data,
                            city=form.city.data,
                            location=form.location.data,
                            video_url=form.video_url.data,
                            map_url=form.map_url.data,
                            price=form.price.data,
                            payment_mode=form.payment_mode.data,
                            furnishing=form.furnishing.data,
                            area=form.area.data,
                            num_of_bed=form.num_of_bed.data,
                            num_of_bath=form.num_of_bath.data,
                            num_of_garage=form.num_of_garage.data,
                            )
    db.session.add(new_property)
    db.session.commit()
    return new_property


def upload_floor_plan(user_property, form):
    img_dir = "property_images"
    floor_plan_file = form.floor_plan.data
    image_file = save_image(floor_plan_file, img_dir)
    user_property.floor_plan = image_file
    db.session.commit()


def upload_property_images(user_property, form):
    try:
        img_dir = "property_images"
        for image in form.images.data:
            image_file = save_image(image, img_dir)
            new_image = ImageSet(image_name=image_file,
                                 property_image=user_property)
            db.session.add(new_image)
            db.session.commit()
    except FileNotFoundError:
        pass


def update_property_amenities(checked_amenity, user_property):
    for amenity in checked_amenity:
        new_amenity = Amenity(amenity_name=amenity,
                              property_amenity=user_property)
        db.session.add(new_amenity)
        db.session.commit()


@account.route("/post_property", methods=["POST", "GET"])
@login_required
def post_property():
    form = PropertyForm()
    if form.validate_on_submit():
        checked_amenities = request.form.getlist("amenity")
        new_property = post_new_property(form)
        if form.floor_plan.data:
            upload_floor_plan(new_property, form)
        if form.images.data:
            upload_property_images(new_property, form)
        if checked_amenities:
            update_property_amenities(checked_amenities, new_property)
        flash("Property has been submitted for verification", "success")
        return redirect(url_for('account.post_property'))
    return render_template("post_property.html", form=form, title_page="Post Property", amenity_list=AMENITY_LIST)


def fill_user_profile_forms():
    form = ProfileForm(email=current_user.email,
                       first_name=current_user.first_name,
                       last_name=current_user.last_name,
                       mobile=current_user.mobile if current_user.mobile else "",
                       birthdate=current_user.birthdate if current_user.birthdate else "",
                       )
    return form


def update_user_profile(form):
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.email = form.email.data
    current_user.mobile = form.mobile.data
    current_user.birthdate = form.birthdate.data
    db.session.commit()


def update_profile_pic(form):
    img_dir = "profile_pictures"
    new_profile_pic = form.profile_pic.data
    image_file = save_image(new_profile_pic, img_dir)
    current_user.profile_pic = image_file
    db.session.commit()


@account.route("/update_profile", methods=["POST", "GET"])
@login_required
def update_profile():
    form = fill_user_profile_forms()
    if form.validate_on_submit():
        update_user_profile(form)
        if form.profile_pic.data:
            update_profile_pic(form)
        current_user.modified_at = datetime.now()
        db.session.commit()
        flash("Profile has been updated", "success")
    return render_template("profile.html", form=form, title_page="Profile")


def hash_password(form):
    hashed_and_salted_password = generate_password_hash(form.new_password.data,
                                                        method="pbkdf2:sha256",
                                                        salt_length=8)
    return hashed_and_salted_password


def change_user_password(form):
    old_password = form.old_password.data
    hashed_and_salted_password = hash_password(form)
    if check_password_hash(current_user.password, old_password):
        if check_password_hash(hashed_and_salted_password, form.confirm_new_password.data):
            current_user.password = hashed_and_salted_password
            current_user.modified_at = datetime.now()
            db.session.commit()
            flash("Password has been updated", "success")
        else:
            flash("New Password does not match, please try again", "danger")
    else:
        flash("Old password incorrect, please try again", "danger")


@account.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        if form.new_password.data:
            change_user_password(form)
    return render_template("change_password.html", form=form, title_page="Change Password")


@account.route("/my_posts", methods=["POST", "GET"])
@login_required
def my_posts():
    user_properties = Property.query.filter_by(owner_id=current_user.id).all()
    property_images = [user_property.images[0] for user_property in user_properties if user_property.images != []]
    return render_template("my_posts.html", title_page="My Posts", user_properties=user_properties,
                           property_img=property_images)


@account.route("/delete_post", methods=["POST", "GET"])
@login_required
def delete_post():
    property_id = request.args.get("property_id")
    property_to_delete = Property.query.filter_by(id=property_id).first()
    db.session.delete(property_to_delete)
    db.session.commit()
    flash("Property deleted", "success")
    return redirect(url_for("account.my_posts"))


def fill_property_to_update_forms(property_to_update):
    form = PropertyForm(title=property_to_update.property_title,
                        description=property_to_update.description,
                        type=property_to_update.property_type,
                        city=property_to_update.city,
                        location=property_to_update.location,
                        map_url=property_to_update.map_url,
                        video_url=property_to_update.video_url,
                        price=property_to_update.price,
                        payment_mode=property_to_update.payment_mode,
                        area=property_to_update.area,
                        num_of_bed=property_to_update.num_of_bed,
                        num_of_bath=property_to_update.num_of_bath,
                        num_of_garage=property_to_update.num_of_garage,
                        furnishing=property_to_update.furnishing,
                        )
    return form


def update_property_forms(property_to_update, form):
    property_to_update.property_title = form.title.data
    property_to_update.description = form.description.data
    property_to_update.property_type = form.type.data
    property_to_update.city = form.city.data
    property_to_update.location = form.location.data
    property_to_update.video_url = form.video_url.data
    property_to_update.map_url = form.map_url.data
    property_to_update.price = form.price.data
    property_to_update.payment_mode = form.payment_mode.data
    property_to_update.furnishing = form.furnishing.data
    property_to_update.area = form.area.data
    property_to_update.num_of_bed = form.num_of_bed.data
    property_to_update.num_of_bath = form.num_of_bath.data
    property_to_update.num_of_garage = form.num_of_garage.data
    db.session.commit()


def delete_property_amenities(property_to_update_amenities):
    for amenity in property_to_update_amenities:
        db.session.delete(amenity)
        db.session.commit()


@account.route("/modify_post", methods=["POST", "GET"])
@login_required
def modify_post():
    property_to_update_id = request.args.get("property_id")
    property_to_update = Property.query.filter_by(id=property_to_update_id).first()
    property_to_update_img = ImageSet.query.filter_by(property_id=property_to_update_id).all()
    property_to_update_amenities = Amenity.query.filter_by(property_id=property_to_update_id).all()
    form = fill_property_to_update_forms(property_to_update)
    property_amenities = []
    if property_to_update_amenities:
        property_amenities = [amenity.amenity_name for amenity in property_to_update_amenities]
    if form.validate_on_submit():
        checked_amenities = request.form.getlist("amenity")
        update_property_forms(property_to_update, form)
        if form.floor_plan.data:
            upload_floor_plan(property_to_update, form)
        if form.images.data:
            upload_property_images(property_to_update, form)
        delete_property_amenities(property_to_update_amenities)
        if checked_amenities:
            update_property_amenities(checked_amenities, property_to_update)
        property_to_update.modified_at = datetime.now()
        db.session.commit()
        flash("Property Updated", "success")
        return redirect(url_for('account.my_posts', title_page="My Posts"))
    return render_template("modify_post.html", form=form, property_to_update=property_to_update,
                           title_page="Modify Post", property_to_update_img=property_to_update_img,
                           amenity_list=AMENITY_LIST, property_amenities=property_amenities)


@account.route("/delete_post_item", methods=["POST", "GET"])
@login_required
def delete_post_item():
    post_item_to_delete_id = request.args.get("item_id")
    post_img_to_delete_id = request.args.get("img_id")
    post_item_to_delete = Property.query.filter_by(id=post_item_to_delete_id).first()
    post_img_to_delete = ImageSet.query.filter_by(id=post_img_to_delete_id).first()
    if post_item_to_delete:
        post_item_to_delete.floor_plan = ""
        flash("Post Floor Plan Deleted", "success")
    if post_img_to_delete:
        db.session.delete(post_img_to_delete)
        flash(f"Post {post_img_to_delete.image_name} Deleted", "success")
    db.session.commit()
    return redirect(url_for("account.my_posts", title_page="My Posts"))
