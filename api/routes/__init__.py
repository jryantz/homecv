from flask import Blueprint
from .check import blueprint as check_blueprint

routes = Blueprint("routes", __name__)

routes.register_blueprint(check_blueprint, url_prefix="/check")
