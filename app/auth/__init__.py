from flask import Blueprint

auths = Blueprint("auth", __name__, url_prefix="/auth")

from . import auth
