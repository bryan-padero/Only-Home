from flask import Blueprint, flash, render_template, redirect, url_for, request
from website import db
from ..models import *

page = Blueprint("page", __name__)


@page.route("/property_page")
def property_page():
    return render_template("property_page.html")
