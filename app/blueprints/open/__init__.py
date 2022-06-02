from flask import Blueprint, render_template, send_file, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from train import main_flask
import shutil
import sys

bp_open = Blueprint('bp_open', __name__)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@bp_open.route('/', methods=['GET', "POST"])
@bp_open.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    path = (sys.path[1])
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               f'{path}/app/static/files/images',
                               secure_filename('image.jpg')))

        original = rf'{path}/app/static/files/images/image.jpg'
        target = rf'{path}/app/static/test_images/image.jpg'

        shutil.copyfile(original, target)
        main_flask()
        return redirect(url_for('bp_open.redirect_super_resolution'))
    return render_template('index.html', form=form)


@bp_open.route('/redirect')
def redirect_super_resolution():
    return render_template('redirect.html')


@bp_open.route('/index')
def show_images():
    original_image = os.path.join('static/files/images', 'image.jpg')
    enhanced_image = os.path.join('static/enhanced', 'image.jpg')
    return render_template("images.html", original_image=original_image, enhanced_image=enhanced_image)


@bp_open.route('/download')
def download_file(file='static/enhanced/image.jpg'):
    return send_file(file, as_attachment=True)
