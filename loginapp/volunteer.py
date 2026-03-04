import os
import sys
from flask import render_template, request, redirect, url_for, session
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
        notifications=notifications,
        upcoming_events=upcoming_events,
    )


@app.route("/volunteer/events")
@login_required
@role_required("volunteer")
def browse_events():
    """Browse and filter cleanup events."""
    # Get filter parameters
    filter_date = request.args.get("date", "")
    filter_location = request.args.get("location", "")
    filter_type = request.args.get("type", "")

    query = """
        SELECT e.*, z.zone_name,
               (SELECT COUNT(*) FROM event_registrations 
                WHERE event_id = e.event_id) as volunteer_count,
               CASE WHEN EXISTS (
                   SELECT 1 FROM event_registrations 
                   WHERE event_id = e.event_id AND volunteer_id = %s
               ) THEN TRUE ELSE FALSE END as is_registered
        FROM events e
        LEFT JOIN cleanup_zones z ON e.zone_id = z.zone_id
        WHERE e.event_date >= CURRENT_DATE
    """
    params = [session["user_id"]]

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
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

    return render_template("browse_events.html", events=events)


@app.route("/volunteer/register/<int:event_id>", methods=["POST"])
@login_required
@role_required("volunteer")
def register_for_event(event_id):
    """Register volunteer for an event with conflict checking."""
    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute(
            """
            SELECT event_date, event_time, duration_hours 
            FROM events WHERE event_id = %s;
        """,
            (event_id,),
        )
        event = cursor.fetchone()

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
            return render_template(
                "browse_events.html",
                error=f"You're already registered for '{conflict['event_name']}' on this date.",
            )

        # Register for event
        cursor.execute(
            """
            INSERT INTO event_registrations (event_id, volunteer_id)
            VALUES (%s, %s);
        """,
            (event_id, session["user_id"]),
        )

    return redirect(url_for("browse_events"))


@app.route("/volunteer/history")
@login_required
@role_required("volunteer")
def participation_history():
    """View volunteer's participation history."""
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.event_name, e.location, e.event_date, e.event_time,
                   er.attendance_status, er.bags_collected, er.recyclables_sorted,
                   f.rating, f.comments as feedback_comment
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


@app.route("/volunteer/feedback/<int:event_id>", methods=["GET", "POST"])
@login_required
@role_required("volunteer")
def submit_feedback(event_id):
    """Submit feedback for an event."""
    if request.method == "POST":
        rating = request.form.get("rating")
        comments = request.form.get("comments", "")

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO feedback (event_id, volunteer_id, rating, comments)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (event_id, volunteer_id) 
                DO UPDATE SET rating = %s, comments = %s, submitted_at = CURRENT_TIMESTAMP;
            """,
                (event_id, session["user_id"], rating, comments, rating, comments),
            )

        return redirect(url_for("participation_history"))

    # Get event details
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT event_name, event_date FROM events WHERE event_id = %s;
        """,
            (event_id,),
        )
        event = cursor.fetchone()

    return render_template("submit_feedback.html", event=event, event_id=event_id)
