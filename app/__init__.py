# third-party imports
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    Bootstrap(app)

    from .home import home as home_blueprint
    from .auth import auths as auth_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("home/error.html", title="Error")

    return app
