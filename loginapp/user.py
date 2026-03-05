import os
import sys
from flask import render_template, request, redirect, url_for, session, flash
from flask import send_from_directory
import re
from werkzeug.utils import secure_filename
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
from loginapp import app, db, bcrypt
from loginapp.decorators import login_required

DEFAULT_USER_ROLE = "volunteer"

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.root_path, "static", "uploads"), filename
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user."""
    if "loggedin" in session:
        role = session.get("role", None)
        if role == "volunteer":
            home_endpoint = "volunteer_home"
        elif role == "event_leader":
            home_endpoint = "event_leader_home"
        elif role == "admin":
            home_endpoint = "admin_home"
        else:
            home_endpoint = "logout"
    else:
        home_endpoint = "login"
    return url_for(home_endpoint)


@app.route("/")
def root():
    """Root endpoint redirects to appropriate home page."""
    return redirect(user_home_url())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page endpoint."""
    if "loggedin" in session:
        return redirect(user_home_url())

    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, username, password_hash, person_role, status 
                FROM users WHERE username = %s;
            """,
                (username,),
            )
            account = cursor.fetchone()

            if account:
                print(
                    f"User found: {account['username']} with status {account['status']}"
                )
                if account["status"] == "inactive":
                    return render_template(
                        "login.html", username=username, account_inactive=True
                    )

                if bcrypt.check_password_hash(account["password_hash"], password):
                    print(
                        f"Password for user {account['username']} is correct. Logging in."
                    )
                    session["loggedin"] = True
                    session["user_id"] = account["user_id"]
                    session["username"] = account["username"]
                    session["role"] = account["person_role"]

                    # Check for unread notifications
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM notifications 
                        WHERE user_id = %s AND is_read = FALSE;
                    """,
                        (account["user_id"],),
                    )
                    notification_count = cursor.fetchone()["count"]
                    print(
                        f"User {account['username']} has {notification_count} unread notifications."
                    )
                    session["unread_notifications"] = notification_count

                    return redirect(user_home_url())
                else:
                    return render_template(
                        "login.html", username=username, password_invalid=True
                    )
            else:
                return render_template(
                    "login.html", username=username, username_invalid=True
                )

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup page endpoint with all required volunteer fields."""
    if "loggedin" in session:
        return redirect(user_home_url())

    if request.method == "POST":
        # Get all form fields
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        full_name = request.form.get("full_name", "")
        home_address = request.form.get("home_address", "")
        contact_number = request.form.get("contact_number", "")
        environmental_interests = request.form.get("environmental_interests", "")

        # Validation
        username_error = None
        email_error = None
        password_error = None
        full_name_error = None
        contact_error = None

        # Check username uniqueness
        with db.get_cursor() as cursor:
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s;", (username,)
            )
            if cursor.fetchone():
                username_error = "Username already taken."

        # Username validation
        if not username_error and (
            len(username) > 20 or not re.match(r"^[A-Za-z0-9]+$", username)
        ):
            username_error = "Username must be letters/numbers only, max 20 chars."

        # Email validation
        if len(email) > 320 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_error = "Invalid email address."

        # Password validation
        if len(password) < 8:
            password_error = "Password must be at least 8 characters."
        elif not re.search(r"[A-Z]", password):
            password_error = "Password must contain at least one uppercase letter."
        elif not re.search(r"[a-z]", password):
            password_error = "Password must contain at least one lowercase letter."
        elif not re.search(r"[0-9]", password):
            password_error = "Password must contain at least one number."
        elif password != confirm_password:
            password_error = "Passwords do not match."

        # Contact number validation (NZ format)
        if not re.match(r"^[0-9\-+\s()]{8,20}$", contact_number):
            contact_error = "Invalid contact number format."

        # Full name validation
        if not full_name or len(full_name) > 100:
            full_name_error = "Please enter your full name (max 100 chars)."

        if any(
            [
                username_error,
                email_error,
                password_error,
                full_name_error,
                contact_error,
            ]
        ):
            return render_template(
                "signup.html",
                username=username,
                email=email,
                full_name=full_name,
                home_address=home_address,
                contact_number=contact_number,
                environmental_interests=environmental_interests,
                username_error=username_error,
                email_error=email_error,
                password_error=password_error,
                full_name_error=full_name_error,
                contact_error=contact_error,
            )

        # Handle profile image upload
        profile_image = "default_profile.jpg"
        if "profile_image" in request.files:
            file = request.files["profile_image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{username}_{file.filename}")
                file.save(os.path.join("static/uploads", filename))
                profile_image = filename

        # Hash password and create user
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users 
                (username, password_hash, email, person_role, full_name, 
                 home_address, contact_number, environmental_interests, profile_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
                (
                    username,
                    password_hash,
                    email,
                    DEFAULT_USER_ROLE,
                    full_name,
                    home_address,
                    contact_number,
                    environmental_interests,
                    profile_image,
                ),
            )

        return render_template("signup.html", signup_successful=True)

    return render_template("signup.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """View and edit user profile."""
    if request.method == "POST":
        # Check if this is an image upload/remove request
        if "update_image" in request.form:
            # Handle image upload
            if "profile_image" in request.files:
                file = request.files["profile_image"]
                if file and file.filename and allowed_file(file.filename):
                    # Generate unique filename
                    # Create secure filename with timestamp to avoid duplicates
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    original_filename = secure_filename(file.filename)
                    filename = f"{session['username']}_{timestamp}_{original_filename}"

                    # Ensure upload directory exists
                    upload_dir = os.path.join(app.root_path, "static", "uploads")
                    os.makedirs(upload_dir, exist_ok=True)

                    # Save file
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)

                    # Update database with new filename
                    with db.get_cursor() as cursor:
                        cursor.execute(
                            """
                            UPDATE users 
                            SET profile_image = %s 
                            WHERE user_id = %s;
                        """,
                            (filename, session["user_id"]),
                        )

                    flash("Profile image updated successfully!", "success")
        elif "remove_image" in request.form:
            # Remove profile image
            with db.get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users 
                    SET profile_image = 'default_profile.jpg' 
                    WHERE user_id = %s;
                """,
                    (session["user_id"],),
                )
            # delete old image file if it exists and is not the default
            image_path = os.path.join(
                app.root_path, "static", "uploads", session.get("profile_image", "")
            )
            if (
                os.path.exists(image_path)
                and session.get("profile_image", "") != "default_profile.jpg"
            ):
                os.remove(image_path)
            flash("Profile image removed.", "success")
        else:
            # Update profile details
            full_name = request.form.get("full_name", "")
            email = request.form.get("email", "")
            home_address = request.form.get("home_address", "")
            contact_number = request.form.get("contact_number", "")
            environmental_interests = request.form.get("environmental_interests", "")

            with db.get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users 
                    SET full_name = %s, email = %s, home_address = %s, 
                        contact_number = %s, environmental_interests = %s
                    WHERE user_id = %s;
                """,
                    (
                        full_name,
                        email,
                        home_address,
                        contact_number,
                        environmental_interests,
                        session["user_id"],
                    ),
                )

            flash("Profile updated successfully!", "success")

        return redirect(url_for("profile"))

    # GET request - display profile
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT username, email, person_role, full_name, home_address, 
                   contact_number, environmental_interests, profile_image
            FROM users WHERE user_id = %s;
        """,
            (session["user_id"],),
        )
        profile = cursor.fetchone()

    return render_template("profile.html", profile=profile)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password."""
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Verify current password
        with db.get_cursor() as cursor:
            cursor.execute(
                "SELECT password_hash FROM users WHERE user_id = %s;",
                (session["user_id"],),
            )
            user = cursor.fetchone()

            if not bcrypt.check_password_hash(user["password_hash"], current_password):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("profile"))

            # Validate new password
            if len(new_password) < 8:
                flash("Password must be at least 8 characters.", "error")
                return redirect(url_for("profile"))

            if not re.search(r"[A-Z]", new_password):
                flash("Password must contain at least one uppercase letter.", "error")
                return redirect(url_for("profile"))

            if not re.search(r"[a-z]", new_password):
                flash("Password must contain at least one lowercase letter.", "error")
                return redirect(url_for("profile"))

            if not re.search(r"[0-9]", new_password):
                flash("Password must contain at least one number.", "error")
                return redirect(url_for("profile"))

            if new_password != confirm_password:
                flash("New passwords do not match.", "error")
                return redirect(url_for("profile"))

            if new_password == current_password:
                flash("New password must be different from current password.", "error")
                return redirect(url_for("profile"))

            # Update password
            new_password_hash = bcrypt.generate_password_hash(new_password).decode(
                "utf-8"
            )
            cursor.execute(
                """
                UPDATE users SET password_hash = %s WHERE user_id = %s;
            """,
                (new_password_hash, session["user_id"]),
            )

            flash("Password changed successfully!", "success")
            return redirect(url_for("profile"))

    # GET request - show the change password page
    return render_template("change_password.html")


@app.route("/logout")
def logout():
    """Logout user and clear session."""
    session.clear()
    return redirect(url_for("login"))
