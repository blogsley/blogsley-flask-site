  
import os
import sys

from dotenv import load_dotenv

basedir = os.getcwd()
load_dotenv(os.path.join(basedir, '.env'))

# Globals
share_folder = None
db_folder = None
static_folder = None

# Set Globals
pip_share_folder = os.path.join(sys.prefix, 'share/blogsley-flask-site')
is_pip_install = os.path.isdir(pip_share_folder)

if is_pip_install:
    share_folder = pip_share_folder
else:
    share_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../share/blogsley-flask-site'))


project_share_folder = 'share/blogsley-flask-site'
is_project = os.path.isdir(project_share_folder)

if is_project:
    db_folder = project_share_folder
else:
    db_folder = share_folder


static_folder = f'{share_folder}/static'

'''
if debug:
    if is_pip_install:
        raise Exception('You need to run this in the project root directory!')
else:
    pass
'''


class Config:
    if os.environ.get("DOKKU_APP_TYPE"):
        MEDIA_ROOT = '/storage/media'
    else:
        MEDIA_ROOT = basedir + '/public/media'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(db_folder, 'blogsley.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_PER_PAGE = 25

    PUBLISH_HOOK = os.environ.get('PUBLISH_HOOK')