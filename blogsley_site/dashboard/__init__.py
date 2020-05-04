from flask import Blueprint

bp = Blueprint('dashboard', __name__, template_folder='templates')

from blogsley_site.dashboard import routes
