
from flask import Flask


def create_app():
    _app = Flask(__name__)
    _app.config['SECRET_KEY'] = 'supersecretkey'
    _app.config['UPLOAD_FOLDER'] = 'static/files'

    from app.blueprints.open import bp_open
    _app.register_blueprint(bp_open)

    return _app


if __name__ == '__main__':

    app = create_app()
    app.run()
