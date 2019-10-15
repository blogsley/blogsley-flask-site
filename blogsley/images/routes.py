import os
from flask import Response, request, abort, render_template_string, send_from_directory
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from blogsley import app, db
from blogsley.jwt import encode_auth_token
from blogsley.images import bp
from blogsley.models.users import User
from blogsley.models.images import Image as Img

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

IMG_WIDTH = 200
IMG_HEIGHT = 160

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
@bp.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    print(request.files)
    if 'filepond' not in request.files:
        raise Exception('No file part')
    file = request.files['filepond']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise Exception('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['MEDIA'], filename))
        img = Img(
            title=filename,
            filename=filename
        )
        db.session.add(img)
        db.session.commit()
        return 'ok'
'''
@bp.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    print(request.files)
    for filename, file in request.files.items():
        # if user does not select file, browser also
        # submit an empty part without filename
        if filename == '':
            raise Exception('No selected file')
        if file and allowed_file(filename):
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['MEDIA_ROOT'], filename))
            img = Img(
                title=filename,
                filename=filename
            )
            db.session.add(img)
            db.session.commit()
    return 'ok'

@bp.route('/<path:filename>')
def image(filename):
    root = app.config['MEDIA_ROOT']
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory(root, filename)
    try:
        im = Image.open(os.path.join(root, filename))
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = BytesIO()
        im.save(io, format='PNG')
        return Response(io.getvalue(), mimetype='image/png')
    except IOError:
        abort(404)

    return send_from_directory(root, filename)
