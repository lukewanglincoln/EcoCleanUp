from functools import wraps
from flask import session, redirect, url_for, render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "loggedin" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "loggedin" not in session:
                return redirect(url_for("login"))
            if session.get("role") not in allowed_roles:
                return render_template("access_denied.html"), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator
