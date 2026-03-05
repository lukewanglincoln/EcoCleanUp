import os
import sys
from flask import render_template, request, redirect, url_for, session
from flask import flash
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
from loginapp import app, db
from loginapp.decorators import login_required, role_required


@app.route("/volunteer/home")
@login_required
@role_required("volunteer")
def volunteer_home():
    """Volunteer homepage with notifications."""
    with db.get_cursor() as cursor:
        # get current user
        cursor.execute(
            "SELECT * FROM users WHERE user_id = %s;",
            (session["user_id"],),
        )
        user = cursor.fetchone()

        # Get notifications
        cursor.execute(
            """
            SELECT n.*, e.event_name, e.event_date, e.event_time, e.location
            FROM notifications n
            JOIN events e ON n.event_id = e.event_id
            WHERE n.user_id = %s AND n.is_read = FALSE
            ORDER BY n.created_at DESC;
        """,
            (session["user_id"],),
        )
        notifications = cursor.fetchall()

        # Mark notifications as read
        if notifications:
            cursor.execute(
                """
                UPDATE notifications SET is_read = TRUE 
                WHERE user_id = %s AND is_read = FALSE;
            """,
                (session["user_id"],),
            )

        # Get upcoming events the volunteer is registered for
        cursor.execute(
            """
            SELECT e.event_name, e.location, e.event_date, e.event_time
            FROM event_registrations er
            JOIN events e ON er.event_id = e.event_id
            WHERE er.volunteer_id = %s
              AND e.event_date >= CURRENT_DATE
              AND er.attendance_status = 'registered'
            ORDER BY e.event_date;
        """,
            (session["user_id"],),
        )
        upcoming_events = cursor.fetchall()

    return render_template(
        "volunteer_home.html",
        user=user,
        notifications=notifications,
        upcoming_events=upcoming_events,
    )


# ==================== BROWSE EVENTS ====================
@app.route("/volunteer/events")
@login_required
def browse_events():
    """Browse and filter cleanup events - accessible by all logged-in users."""
    # Get filter parameters
    filter_date = request.args.get("date", "")
    filter_location = request.args.get("location", "")
    filter_type = request.args.get("type", "")

    query = """
        SELECT e.*, z.zone_name,
               (SELECT COUNT(*) FROM event_registrations 
                WHERE event_id = e.event_id) as volunteer_count
    """

    # Add registration status only for volunteers
    if session.get("role") == "volunteer":
        query += """,
               CASE WHEN EXISTS (
                   SELECT 1 FROM event_registrations 
                   WHERE event_id = e.event_id AND volunteer_id = %s
               ) THEN TRUE ELSE FALSE END as is_registered
        """
        params = [session["user_id"]]
    else:
        params = []
        # Add placeholder for is_registered for non-volunteers
        query += ", FALSE as is_registered"

    query += """
        FROM events e
        LEFT JOIN cleanup_zones z ON e.zone_id = z.zone_id
        WHERE e.event_date >= CURRENT_DATE
    """

    if filter_date:
        query += " AND e.event_date = %s"
        params.append(filter_date)
    if filter_location:
        query += " AND (e.location ILIKE %s OR z.zone_name ILIKE %s)"
        params.extend([f"%{filter_location}%", f"%{filter_location}%"])
    if filter_type:
        query += " AND z.zone_name ILIKE %s"
        params.append(f"%{filter_type}%")

    query += " ORDER BY e.event_date, e.event_time;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params) if params else None)
        events = cursor.fetchall()

        # Get unique locations for filter dropdown
        cursor.execute("SELECT DISTINCT location FROM events ORDER BY location;")
        locations = cursor.fetchall()

        # Get zone types for filter dropdown
        cursor.execute("SELECT zone_name FROM cleanup_zones ORDER BY zone_name;")
        zone_types = cursor.fetchall()

    return render_template(
        "browse_events.html",
        events=events,
        locations=locations,
        zone_types=zone_types,
        filter_date=filter_date,
        filter_location=filter_location,
        filter_type=filter_type,
    )


# ==================== REGISTER FOR EVENT ====================
@app.route("/volunteer/register/<int:event_id>", methods=["POST"])
@login_required
@role_required("volunteer")
def register_for_event(event_id):
    """Register volunteer for an event with conflict checking."""
    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute(
            """
            SELECT event_date, event_time, duration_hours, event_name 
            FROM events WHERE event_id = %s;
        """,
            (event_id,),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found.", "error")
            return redirect(url_for("browse_events"))

        # Check for scheduling conflicts
        cursor.execute(
            """
            SELECT e.event_name, e.event_date, e.event_time
            FROM event_registrations er
            JOIN events e ON er.event_id = e.event_id
            WHERE er.volunteer_id = %s 
              AND e.event_date = %s
              AND er.attendance_status != 'absent';
        """,
            (session["user_id"], event["event_date"]),
        )

        conflict = cursor.fetchone()
        if conflict:
            flash(
                f"You're already registered for '{conflict['event_name']}' on this date.",
                "warning",
            )
            return redirect(url_for("browse_events"))

        # Register for event
        try:
            cursor.execute(
                """
                INSERT INTO event_registrations (event_id, volunteer_id)
                VALUES (%s, %s);
            """,
                (event_id, session["user_id"]),
            )
            flash(f"Successfully registered for {event['event_name']}!", "success")
        except Exception as e:
            flash("Error registering for event. Please try again.", "error")

    return redirect(url_for("browse_events"))


# ==================== PARTICIPATION HISTORY ====================
@app.route("/volunteer/history")
@login_required
@role_required("volunteer")
def participation_history():
    """View volunteer's participation history."""
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.event_id, e.event_name, e.location, e.event_date, e.event_time,
                   er.attendance_status, er.bags_collected, er.recyclables_sorted,
                   f.rating, f.comments as feedback_comment,
                   CASE WHEN f.feedback_id IS NOT NULL THEN TRUE ELSE FALSE END as has_feedback
            FROM event_registrations er
            JOIN events e ON er.event_id = e.event_id
            LEFT JOIN feedback f ON er.event_id = f.event_id AND er.volunteer_id = f.volunteer_id
            WHERE er.volunteer_id = %s
            ORDER BY e.event_date DESC;
        """,
            (session["user_id"],),
        )
        history = cursor.fetchall()

    return render_template("participation_history.html", history=history)


# ==================== SUBMIT FEEDBACK ====================
@app.route("/volunteer/feedback/<int:event_id>", methods=["GET", "POST"])
@login_required
@role_required("volunteer")
def submit_feedback(event_id):
    """Submit feedback for an event."""
    # Check if volunteer attended the event
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT attendance_status FROM event_registrations
            WHERE event_id = %s AND volunteer_id = %s;
        """,
            (event_id, session["user_id"]),
        )
        registration = cursor.fetchone()

        if not registration:
            flash("You are not registered for this event.", "error")
            return redirect(url_for("participation_history"))

        if registration["attendance_status"] != "attended":
            flash("You can only provide feedback for events you attended.", "warning")
            return redirect(url_for("participation_history"))

    if request.method == "POST":
        rating = request.form.get("rating")
        comments = request.form.get("comments", "")

        with db.get_cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO feedback (event_id, volunteer_id, rating, comments)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (event_id, volunteer_id) 
                    DO UPDATE SET rating = %s, comments = %s, submitted_at = CURRENT_TIMESTAMP;
                """,
                    (event_id, session["user_id"], rating, comments, rating, comments),
                )
                flash("Thank you for your feedback!", "success")
                return redirect(url_for("participation_history"))
            except Exception as e:
                flash("Error submitting feedback. Please try again.", "error")

    # Get event details for the form
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT event_name, event_date FROM events WHERE event_id = %s;
        """,
            (event_id,),
        )
        event = cursor.fetchone()

    return render_template("submit_feedback.html", event=event, event_id=event_id)


# ==================== CANCEL REGISTRATION ====================
@app.route("/volunteer/cancel/<int:event_id>", methods=["POST"])
@login_required
@role_required("volunteer")
def cancel_registration(event_id):
    """Cancel volunteer's registration for an event."""
    with db.get_cursor() as cursor:
        # Check if event is in the future
        cursor.execute(
            """
            SELECT event_name FROM events 
            WHERE event_id = %s AND event_date >= CURRENT_DATE;
        """,
            (event_id,),
        )
        event = cursor.fetchone()

        if not event:
            flash("Cannot cancel registration for past events.", "error")
            return redirect(url_for("participation_history"))

        # Delete registration
        cursor.execute(
            """
            DELETE FROM event_registrations
            WHERE event_id = %s AND volunteer_id = %s;
        """,
            (event_id, session["user_id"]),
        )

        if cursor.rowcount > 0:
            flash(f"Registration for {event['event_name']} cancelled.", "success")
        else:
            flash("Registration not found.", "error")

    return redirect(url_for("browse_events"))
