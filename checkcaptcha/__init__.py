import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

__version__ = (0, 1, 0, "dev")

db = SQLAlchemy()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL", 'sqlite:///{}'.format(os.path.join(app.root_path, 'tmp.db')))

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False,
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.update(test_config)

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)

    # apply the blueprints to the app
    from checkcaptcha import captcha_views
    from checkcaptcha.models import init_db_command
    app.register_blueprint(captcha_views.bp)
    app.cli.add_command(init_db_command)

    return app