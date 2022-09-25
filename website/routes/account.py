from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
from website.forms import *
from website.models.property import ImageSet, Amenity, Property
from website.models.user import User
from website import db
import os


account = Blueprint("account", __name__)


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


@account.route("/post-property", methods=["POST", "GET"])
@login_required
def post_property():
    form = PropertyForm()
    if form.validate_on_submit():
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
        if form.floor_plan.data:
            img_dir = "property_images"
            floor_plan_file = form.floor_plan.data
            image_file = save_image(floor_plan_file, img_dir)
            new_property.floor_plan = image_file
            db.session.commit()
        if form.images.data:
            img_dir = "property_images"
            for image in form.images.data:
                image_file = save_image(image, img_dir)
                new_image = ImageSet(image_name=image_file,
                                     property_image=new_property)
                db.session.add(new_image)
                db.session.commit()
        if form.amenity.data:
            for amenity in form.amenity.data:
                new_amenity = Amenity(amenity_name=amenity,
                                      property_amenity=new_property)
                db.session.add(new_amenity)
                db.session.commit()
        flash("Property has been submitted for verification", "success")
        return redirect(url_for('account.post_property'))
    return render_template("post-property.html", form=form, title_page="Post Property")


@account.route("/update_profile", methods=["POST", "GET"])
@login_required
def update_profile():
    form = ProfileForm(email=current_user.email,
                       first_name=current_user.first_name,
                       last_name=current_user.last_name,
                       mobile=current_user.mobile if current_user.mobile else "",
                       birthdate=current_user.birthdate if current_user.birthdate else "",
                       )
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.mobile = form.mobile.data
        current_user.birthdate = form.birthdate.data
        if form.profile_pic.data:
            img_dir = "profile_pictures"
            new_profile_pic = form.profile_pic.data
            image_file = save_image(new_profile_pic, img_dir)
            current_user.profile_pic = image_file
        current_user.modified_at = datetime.now()
        db.session.commit()
        flash("Profile has been updated", "success")
    return render_template("profile.html", form=form, title_page="Profile")


@account.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        if form.new_password.data:
            old_password = form.old_password.data
            hashed_and_salted_password = generate_password_hash(form.new_password.data,
                                                                method="pbkdf2:sha256",
                                                                salt_length=8)
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
    return render_template("change_password.html", form=form, title_page="Change Password")


@account.route("/my_posts", methods=["POST", "GET"])
@login_required
def my_posts():
    user_properties = Property.query.filter_by(owner_id=current_user.id).all()
    property_img = [user_property.images[0] for user_property in user_properties if user_property.images != []]
    return render_template("my_posts.html", title_page="My Posts", user_properties=user_properties,
                           property_img=property_img)


@account.route("/delete_post", methods=["POST", "GET"])
@login_required
def delete_post():
    property_id = request.args.get("property_id")
    property_to_delete = Property.query.filter_by(id=property_id).first()
    db.session.delete(property_to_delete)
    db.session.commit()
    flash("Property deleted", "success")
    return redirect(url_for("account.my_posts"))


@account.route("/modify_post", methods=["POST", "GET"])
@login_required
def modify_post():
    property_id = request.args.get("property_id")
    flash("Property Updated", "success")
    return redirect(url_for("account.my_posts"))
