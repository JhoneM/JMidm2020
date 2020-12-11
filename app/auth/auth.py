import functools
from flask import (
    flash,
    g,
    render_template,
    request,
    url_for,
    session,
    redirect,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from ..conf.db import get_db, close_db

from . import auths


@auths.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute(
            "SELECT id from user where username = %s", (username,)
        )
        if not username:
            error = "Username es requerido"
        elif not password:
            error = "Password es requerido"

        elif c.fetchone() is not None:
            error = "Usuario {} se encuentra registrado.".format(
                username
            )
        if error is None:
            c.execute(
                "INSERT INTO user (username,password) values (%s, %s)",
                (username, generate_password_hash(password)),
            )
            db.commit()

            return redirect(url_for("auth.login"))

        flash(error)
        close_db()
    return render_template("auths/register.html", title="Registro")


@auths.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute("SELECT * FROM user where username = %s", (username,))
        user = c.fetchone()

        if user is None:
            error = "Usuario y/o contraseña invalida"
        elif not check_password_hash(user["password"], password):
            error = "Usuario y/o contraseña invalida"
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("home.index"))
        flash(error)
        close_db()
    return render_template("auths/login.html", title="Ingreso")


@auths.before_app_request
def load_logger_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute("SELECT * FROM user where id = %s", (user_id,))
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@auths.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
