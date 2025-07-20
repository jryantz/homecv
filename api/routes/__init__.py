from flask import Blueprint
from .check import blueprint as check_blueprint
from .health import blueprint as health_blueprint

routes = Blueprint("routes", __name__)

routes.register_blueprint(health_blueprint)  # No prefix - at root
routes.register_blueprint(check_blueprint, url_prefix="/check")
