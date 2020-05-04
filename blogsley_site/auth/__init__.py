from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('auth', __name__, template_folder='templates')
CORS(bp)
from blogsley_site.auth import routes
