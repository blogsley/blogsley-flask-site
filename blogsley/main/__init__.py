from flask import Blueprint

bp = Blueprint('main', __name__)

from blogsley.main import routes
