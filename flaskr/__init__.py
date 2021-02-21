import os
from .extensions import db
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:////home/sarwas/test.db",
    )

    db.init_app(app)
    # from . import commands
    # app.register_blueprint(commands.commands_bp)

    from . import cards_controller
    app.register_blueprint(cards_controller.cards_bp)
    # from . import scores_controller
    # app.register_blueprint(scores_controller.bp)

    # create all db tables
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
