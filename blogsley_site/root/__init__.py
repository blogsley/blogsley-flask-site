from flask import Blueprint

bp = Blueprint('root', __name__)

from blogsley_site.root import routes
