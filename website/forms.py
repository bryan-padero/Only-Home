from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TelField, FloatField, IntegerField, \
    SelectField, TextAreaField, MultipleFileField, FileField, SelectMultipleField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, EqualTo, Length, Email, URL, Optional


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthdate = DateField("Birthdate", validators=[Optional()])
    profile_pic = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    mobile = TelField("Mobile Number", validators=[Length(max=20)])
    submit = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired(), Length(min=8, max=20)])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired()])
    submit = SubmitField("Update")


class PropertyForm(FlaskForm):
    types = [("", "Please select"), ("Villa", "Villa"), ("Apartment", "Apartment")]
    cities = [("", "Please select"), ("Abu Dhabi", "Abu Dhabi"), ("Dubai", "Dubai"), ("Al Ain", "Al Ain"),
              ("Sharjah", "Sharjah"), ("Ajman", "Ajman"), ("Fujairah", "Fujairah"), ("Umm Al Quwain", "Umm Al Quwain")]
    payment_modes = [("", "Please select"), ("Monthly", "Monthly"), ("Quarterly", "Quarterly"),
                     ("Bi-Yearly", "Bi-Yearly"), ("Yearly", "Yearly")]
    furnishings = [("", "Please select"), ("Unfurnished", "Unfurnished"), ("Furnished", "Furnished"),
                   ("Semi-Furnished", "Semi-Furnished"), ]
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    floor_plan = FileField("Floor Plan", validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField("Property Type", choices=types, validators=[DataRequired()])
    city = SelectField("City", choices=cities, validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    video_url = StringField("Video URL", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    payment_mode = SelectField("Rent is paid", choices=payment_modes, validators=[DataRequired()])
    area = IntegerField("Area", validators=[DataRequired()])
    num_of_bed = IntegerField("Bedrooms", validators=[DataRequired()])
    num_of_bath = IntegerField("Bathrooms", validators=[DataRequired()])
    num_of_garage = IntegerField("Garages", validators=[DataRequired()])
    furnishing = SelectField("Furnishings", choices=furnishings, validators=[DataRequired()])
    images = MultipleFileField("Upload Images", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit")
