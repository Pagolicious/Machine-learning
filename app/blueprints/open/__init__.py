from flask import Blueprint, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

bp_open = Blueprint('bp_open', __name__)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@bp_open.route('/', methods=['GET', "POST"])
@bp_open.route('/home', methods=['GET', "POST"])
def home(path='C:/Teknikhögskolan/super_resolution/app/static/files'):  # change this to your own path
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), path, secure_filename(
            'original_image.jpg')))  # Then save the file
    return render_template('index.html', form=form)


@bp_open.route('/index')
def show_images():
    original_image = os.path.join('static/files', 'original_image.jpg')
    enhanced_image = os.path.join('static/files', 'enhanced_image.jpg')
    return render_template("images.html", original_image=original_image, enhanced_image=enhanced_image)


@bp_open.route('/download')
def download_file(file='static/files/enhanced_image.jpg'):
    return send_file(file, as_attachment=True)
