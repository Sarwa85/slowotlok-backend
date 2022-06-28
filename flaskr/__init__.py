import os

from flask import Flask
from flask_cors import CORS
from flaskr.baseinit import init as initBase
# from flaskr.login import logincontroller, loginservice
# from flask_session import Session

# from flask_login import (
#     LoginManager,
#     # current_user,
#     # login_required,
#     # login_user,
#     # logout_user,
# )


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # login_manager = LoginManager()
    # login_manager.init_app(app)

    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:////home/sarwas/test.db",
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE = True
    )
    app.config['SESSION_TYPE'] = 'filesystem'
    # Session(app)

    # db
    initBase()

    # Flask-Login helper to retrieve a user from our db
    # @login_manager.user_loader
    # def load_user(user_id):
    #     print("load user " + user_id)
    #     return loginservice.load_user(user_id)

    # @login_manager.request_loader
    # def load_user_from_request(request):
    #     return loginservice.load_user_from_request(request)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr.card import cardcontroler
    app.register_blueprint(cardcontroler.bp)
    # app.register_blueprint(logincontroller.bp)




    return app

