import os
import sys
from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
from loginapp import app, db
from loginapp.decorators import login_required, role_required


# ==================== EVENT LEADER HOME ====================
@app.route("/event_leader/home")
@login_required
@role_required("event_leader")
def event_leader_home():
    """Event Leader homepage."""
    with db.get_cursor() as cursor:
        # get current user
        cursor.execute("SELECT * FROM users WHERE user_id = %s;", (session["user_id"],))
        user = cursor.fetchone()
        # Get stats for events created by this leader
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_events,
                SUM(CASE WHEN event_date >= CURRENT_DATE THEN 1 ELSE 0 END) as upcoming_events,
                COUNT(DISTINCT er.volunteer_id) as total_volunteers,
                COALESCE(SUM(er.bags_collected), 0) as total_bags,
                COALESCE(SUM(er.recyclables_sorted), 0) as total_recyclables
            FROM events e
            LEFT JOIN event_registrations er ON e.event_id = er.event_id
            WHERE e.created_by = %s;
        """,
            (session["user_id"],),
        )
        stats = cursor.fetchone()

        # Get recent events
        cursor.execute(
            """
            SELECT event_id, event_name, location, event_date, status, 
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteers
            FROM events e
            WHERE created_by = %s
            ORDER BY created_at DESC
            LIMIT 5;
        """,
            (session["user_id"],),
        )
        recent_events = cursor.fetchall()

    return render_template(
        "event_leader_home.html", user=user, stats=stats, recent_events=recent_events
    )


# ==================== MANAGE EVENTS ====================
@app.route("/event_leader/events")
@login_required
@role_required("event_leader")
def manage_events():
    """View and manage all events created by this leader."""
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.*, z.zone_name,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteer_count,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id AND attendance_status = 'attended') as attended_count
            FROM events e
            LEFT JOIN cleanup_zones z ON e.zone_id = z.zone_id
            WHERE e.created_by = %s
            ORDER BY e.event_date DESC;
        """,
            (session["user_id"],),
        )
        events = cursor.fetchall()

    return render_template("manage_events.html", events=events)


# ==================== CREATE EVENT ====================
@app.route("/event_leader/events/create", methods=["GET", "POST"])
@login_required
@role_required("event_leader")
def create_event():
    """Create a new cleanup event."""
    if request.method == "POST":
        # Get form data
        event_name = request.form.get("event_name")
        location = request.form.get("location")
        zone_id = request.form.get("zone_id")
        event_date = request.form.get("event_date")
        event_time = request.form.get("event_time")
        duration_hours = request.form.get("duration_hours")
        supplies = request.form.get("supplies")
        safety_instructions = request.form.get("safety_instructions")

        # Basic validation
        error = None
        if not all([event_name, location, event_date, event_time, duration_hours]):
            error = "Please fill in all required fields."
        elif datetime.strptime(event_date, "%Y-%m-%d").date() < datetime.now().date():
            error = "Event date must be in the future."

        if error:
            flash(error, "error")
        else:
            with db.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO events (event_name, location, zone_id, event_date, event_time, 
                                       duration_hours, supplies, safety_instructions, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING event_id;
                """,
                    (
                        event_name,
                        location,
                        zone_id or None,
                        event_date,
                        event_time,
                        duration_hours,
                        supplies,
                        safety_instructions,
                        session["user_id"],
                    ),
                )
                new_event = cursor.fetchone()
                flash(f"Event '{event_name}' created successfully!", "success")
                return redirect(url_for("manage_events"))

    # Get zones for dropdown
    with db.get_cursor() as cursor:
        cursor.execute(
            "SELECT zone_id, zone_name FROM cleanup_zones ORDER BY zone_name;"
        )
        zones = cursor.fetchall()

    current_date = datetime.now().date()

    return render_template("create_event.html", zones=zones, current_date=current_date)


# ==================== EDIT EVENT ====================
@app.route("/event_leader/events/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
@role_required("event_leader")
def edit_event(event_id):
    """Edit an existing event."""
    # Verify event belongs to this leader
    with db.get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM events WHERE event_id = %s AND created_by = %s;",
            (event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you don't have permission to edit it.", "error")
            return redirect(url_for("manage_events"))

    if request.method == "POST":
        # Get form data
        event_name = request.form.get("event_name")
        location = request.form.get("location")
        zone_id = request.form.get("zone_id")
        event_date = request.form.get("event_date")
        event_time = request.form.get("event_time")
        duration_hours = request.form.get("duration_hours")
        supplies = request.form.get("supplies")
        safety_instructions = request.form.get("safety_instructions")
        status = request.form.get("status")

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE events 
                SET event_name = %s, location = %s, zone_id = %s, event_date = %s,
                    event_time = %s, duration_hours = %s, supplies = %s,
                    safety_instructions = %s, status = %s
                WHERE event_id = %s;
            """,
                (
                    event_name,
                    location,
                    zone_id or None,
                    event_date,
                    event_time,
                    duration_hours,
                    supplies,
                    safety_instructions,
                    status,
                    event_id,
                ),
            )
            flash("Event updated successfully!", "success")
            return redirect(url_for("manage_events"))

    # Get zones for dropdown
    with db.get_cursor() as cursor:
        cursor.execute(
            "SELECT zone_id, zone_name FROM cleanup_zones ORDER BY zone_name;"
        )
        zones = cursor.fetchall()

    current_date = datetime.now().date()

    return render_template(
        "edit_event.html", event=event, zones=zones, current_date=current_date
    )


# ==================== VIEW EVENT VOLUNTEERS ====================
@app.route("/event_leader/events/<int:event_id>/volunteers")
@login_required
@role_required("event_leader")
def view_event_volunteers(event_id):
    """View list of volunteers registered for an event."""
    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute(
            """
            SELECT e.*, z.zone_name 
            FROM events e
            LEFT JOIN cleanup_zones z ON e.zone_id = z.zone_id
            WHERE e.event_id = %s AND e.created_by = %s;
        """,
            (event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you don't have permission to view it.", "error")
            return redirect(url_for("manage_events"))

        # Get registered volunteers
        cursor.execute(
            """
            SELECT u.user_id, u.username, u.full_name, u.email, u.contact_number,
                   er.registration_date, er.attendance_status,
                   er.bags_collected, er.recyclables_sorted
            FROM event_registrations er
            JOIN users u ON er.volunteer_id = u.user_id
            WHERE er.event_id = %s
            ORDER BY er.registration_date;
        """,
            (event_id,),
        )
        volunteers = cursor.fetchall()

    current_date = datetime.now().date()

    return render_template(
        "event_volunteers.html",
        event=event,
        volunteers=volunteers,
        current_date=current_date,
    )


@app.route("/event_leader/volunteers/<int:volunteer_id>/history")
@login_required
@role_required("event_leader")
def event_leader_view_volunteer_history(volunteer_id):
    """View volunteer's event history."""
    with db.get_cursor() as cursor:
        # Get volunteer details
        cursor.execute(
            "SELECT user_id, username, full_name FROM users WHERE user_id = %s;",
            (volunteer_id,),
        )
        volunteer = cursor.fetchone()

        if not volunteer:
            flash("Volunteer not found.", "error")
            return redirect(url_for("manage_events"))

        # Get volunteer's event history
        cursor.execute(
            """
            SELECT e.event_name, e.event_date, e.location, z.zone_name,
                   er.attendance_status, er.bags_collected, er.recyclables_sorted,
                   f.rating, f.comments as feedback
            FROM event_registrations er
            JOIN events e ON er.event_id = e.event_id
            LEFT JOIN cleanup_zones z ON e.zone_id = z.zone_id
            LEFT JOIN feedback f ON er.event_id = f.event_id AND er.volunteer_id = f.volunteer_id
            WHERE er.volunteer_id = %s
            AND e.created_by = %s
            ORDER BY e.event_date DESC;
        """,
            (volunteer_id, session["user_id"]),
        )
        history = cursor.fetchall()

    return render_template(
        "volunteer_history.html", volunteer=volunteer, history=history
    )


# ==================== REMOVE VOLUNTEER ====================
@app.route(
    "/event_leader/events/<int:event_id>/remove/<int:volunteer_id>", methods=["POST"]
)
@login_required
@role_required("event_leader")
def remove_volunteer(event_id, volunteer_id):
    """Remove a volunteer from an event."""
    with db.get_cursor() as cursor:
        # Verify event belongs to this leader
        cursor.execute(
            "SELECT event_name FROM events WHERE event_id = %s AND created_by = %s;",
            (event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you don't have permission.", "error")
            return redirect(url_for("manage_events"))

        # Remove volunteer
        cursor.execute(
            """
            DELETE FROM event_registrations
            WHERE event_id = %s AND volunteer_id = %s;
        """,
            (event_id, volunteer_id),
        )

        flash("Volunteer removed from event.", "success")

    return redirect(url_for("view_event_volunteers", event_id=event_id))


# ==================== TRACK ATTENDANCE ====================
@app.route("/event_leader/events/<int:event_id>/attendance", methods=["POST"])
@login_required
@role_required("event_leader")
def track_attendance(event_id):
    """Mark volunteer attendance for an event."""
    volunteer_id = request.form.get("volunteer_id")
    attendance_status = request.form.get("attendance_status")
    bags_collected = request.form.get("bags_collected", 0)
    recyclables_sorted = request.form.get("recyclables_sorted", 0)

    with db.get_cursor() as cursor:
        cursor.execute(
            """
            UPDATE event_registrations
            SET attendance_status = %s, bags_collected = %s, recyclables_sorted = %s
            WHERE event_id = %s AND volunteer_id = %s;
        """,
            (
                attendance_status,
                bags_collected,
                recyclables_sorted,
                event_id,
                volunteer_id,
            ),
        )

    flash("Attendance updated successfully!", "success")
    return redirect(url_for("view_event_volunteers", event_id=event_id))


# ==================== SEND REMINDER ====================
@app.route("/event_leader/events/<int:event_id>/remind", methods=["POST"])
@login_required
@role_required("event_leader")
def send_event_reminder(event_id):
    """Send reminder to all volunteers for an event."""
    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute(
            """
            SELECT event_name, event_date FROM events 
            WHERE event_id = %s AND created_by = %s;
        """,
            (event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found.", "error")
            return redirect(url_for("manage_events"))

        # Get all registered volunteers
        cursor.execute(
            """
            SELECT volunteer_id FROM event_registrations
            WHERE event_id = %s AND attendance_status = 'registered';
        """,
            (event_id,),
        )
        volunteers = cursor.fetchall()

        # Create notification for each volunteer
        message = f"Reminder: {event['event_name']} is on {event['event_date'].strftime('%B %d, %Y')}"

        for volunteer in volunteers:
            cursor.execute(
                """
                INSERT INTO notifications (user_id, event_id, message, notification_type)
                VALUES (%s, %s, %s, 'reminder');
            """,
                (volunteer["volunteer_id"], event_id, message),
            )

        flash(f"Reminder sent to {len(volunteers)} volunteers!", "success")

    return redirect(url_for("view_event_volunteers", event_id=event_id))


@app.route("/event_leader/events/<int:event_id>/cancel", methods=["POST"])
@login_required
@role_required("event_leader")
def event_leader_cancel_event(event_id):
    """cancel an event."""
    with db.get_cursor() as cursor:
        cursor.execute(
            "UPDATE events SET status = 'cancelled' WHERE event_id = %s;", (event_id,)
        )
        flash("Event has been cancelled.", "success")

    return redirect(url_for("manage_events"))


# ==================== EVENT REPORTS ====================
@app.route("/event_leader/reports")
@login_required
@role_required("event_leader")
def event_reports():
    """View reports for all events created by this leader."""
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                e.event_id, e.event_name, e.event_date, e.location,
                COUNT(DISTINCT er.volunteer_id) as total_registered,
                SUM(CASE WHEN er.attendance_status = 'attended' THEN 1 ELSE 0 END) as attended,
                COALESCE(SUM(er.bags_collected), 0) as total_bags,
                COALESCE(SUM(er.recyclables_sorted), 0) as total_recyclables,
                COALESCE(AVG(f.rating), 0) as avg_rating
            FROM events e
            LEFT JOIN event_registrations er ON e.event_id = er.event_id
            LEFT JOIN feedback f ON e.event_id = f.event_id
            WHERE e.created_by = %s
            GROUP BY e.event_id, e.event_name, e.event_date, e.location
            ORDER BY e.event_date DESC;
        """,
            (session["user_id"],),
        )
        reports = cursor.fetchall()

    return render_template("event_reports.html", reports=reports)
