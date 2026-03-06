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
        cursor.execute(
            "SELECT * FROM users WHERE user_id = %s;",
            (session["user_id"],),
        )
        user = cursor.fetchone()

        # Get stats for events created by this leader
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_events,
                SUM(CASE WHEN event_date >= CURRENT_DATE THEN 1 ELSE 0 END) as upcoming_events,
                COUNT(DISTINCT er.volunteer_id) as total_volunteers,
                COALESCE(SUM(eo.bags_collected), 0) as total_bags,
                COALESCE(SUM(eo.recyclables_sorted), 0) as total_recyclables
            FROM events e
            LEFT JOIN event_registrations er ON e.event_id = er.event_id
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            WHERE e.event_leader_id = %s;
            """,
            (session["user_id"],),
        )
        stats = cursor.fetchone()

        # Get recent events
        cursor.execute(
            """
            SELECT e.event_id, e.event_name, e.location, e.event_date, e.status,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteers,
                   eo.bags_collected, eo.recyclables_sorted
            FROM events e
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            WHERE e.event_leader_id = %s
            AND e.event_date >= CURRENT_DATE
            AND e.status != 'cancelled'
            ORDER BY e.event_date ASC
            LIMIT 5;
            """,
            (session["user_id"],),
        )
        recent_events = cursor.fetchall()

    return render_template(
        "event_leader_home.html", user=user, stats=stats, recent_events=recent_events
    )


# ==================== MANAGE EVENTS ====================
# ==================== MANAGE EVENTS ====================
@app.route("/event_leader/events")
@login_required
@role_required("event_leader")
def manage_events():
    """View and manage all events created by this leader."""
    # Get filter parameter (default to 'upcoming')
    filter_status = request.args.get("status", "upcoming")

    with db.get_cursor() as cursor:
        # Base query
        query = """
            SELECT e.*,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteer_count,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count,
                   eo.bags_collected,
                   eo.recyclables_sorted,
                   eo.number_attendees
            FROM events e
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            WHERE e.event_leader_id = %s
        """

        params = [session["user_id"]]

        # Add status filter if not 'all'
        if filter_status != "all":
            query += " AND e.status = %s"
            params.append(filter_status)

        query += " ORDER BY e.event_date DESC;"

        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        # Get counts for each status (for the tabs)
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'upcoming' THEN 1 END) as upcoming_count,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
                COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_count
            FROM events
            WHERE event_leader_id = %s;
            """,
            (session["user_id"],),
        )
        counts = cursor.fetchone()

    current_date = datetime.now().date()
    return render_template(
        "manage_events.html",
        events=events,
        current_date=current_date,
        filter_status=filter_status,
        counts=counts,
    )


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
        event_type = request.form.get("event_type")
        event_date = request.form.get("event_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        duration = request.form.get("duration")
        description = request.form.get("description")
        supplies = request.form.get("supplies")
        safety_instructions = request.form.get("safety_instructions")

        # Basic validation
        error = None
        if not all(
            [
                event_name,
                location,
                event_type,
                event_date,
                start_time,
                end_time,
                duration,
            ]
        ):
            error = "Please fill in all required fields."
        elif (
            event_date
            and datetime.strptime(event_date, "%Y-%m-%d").date() < datetime.now().date()
        ):
            error = "Event date must be in the future."

        if error:
            flash(error, "error")
        else:
            with db.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO events 
                    (event_name, event_leader_id, location, event_type, event_date, 
                     start_time, end_time, duration, description, supplies, safety_instructions)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING event_id;
                    """,
                    (
                        event_name,
                        session["user_id"],
                        location,
                        event_type,
                        event_date,
                        start_time,
                        end_time,
                        duration,
                        description,
                        supplies,
                        safety_instructions,
                    ),
                )
                new_event = cursor.fetchone()
                flash(f"Event '{event_name}' created successfully!", "success")
                return redirect(url_for("manage_events"))

    # Get event types for dropdown
    with db.get_cursor() as cursor:
        cursor.execute("SELECT DISTINCT event_type FROM events ORDER BY event_type;")
        event_types = cursor.fetchall()

    current_date = datetime.now().date()
    return render_template(
        "create_event.html", event_types=event_types, current_date=current_date
    )


# ==================== EDIT EVENT ====================
@app.route("/event_leader/events/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
@role_required("event_leader")
def edit_event(event_id):
    """Edit an existing event."""
    # Verify event belongs to this leader
    with db.get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM events WHERE event_id = %s AND event_leader_id = %s;",
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
        event_type = request.form.get("event_type")
        event_date = request.form.get("event_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        duration = request.form.get("duration")
        description = request.form.get("description")
        supplies = request.form.get("supplies")
        safety_instructions = request.form.get("safety_instructions")
        status = request.form.get("status")

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE events 
                SET event_name = %s, location = %s, event_type = %s, event_date = %s,
                    start_time = %s, end_time = %s, duration = %s, description = %s,
                    supplies = %s, safety_instructions = %s, status = %s
                WHERE event_id = %s;
                """,
                (
                    event_name,
                    location,
                    event_type,
                    event_date,
                    start_time,
                    end_time,
                    duration,
                    description,
                    supplies,
                    safety_instructions,
                    status,
                    event_id,
                ),
            )
            flash("Event updated successfully!", "success")
            return redirect(url_for("manage_events"))

    # Get event types for dropdown
    with db.get_cursor() as cursor:
        cursor.execute("SELECT DISTINCT event_type FROM events ORDER BY event_type;")
        event_types = cursor.fetchall()

    current_date = datetime.now().date()

    return render_template(
        "edit_event.html",
        event=event,
        event_types=event_types,
        current_date=current_date,
    )


# ==================== VIEW EVENT VOLUNTEERS ====================
@app.route("/event_leader/events/<int:event_id>/volunteers")
@login_required
@role_required("event_leader")
def view_event_volunteers(event_id):
    """View list of volunteers registered for an event."""
    with db.get_cursor() as cursor:
        # Get event details including outcomes
        cursor.execute(
            """
            SELECT e.*, u.full_name as event_leader_name,
                   eo.bags_collected, eo.recyclables_sorted, eo.number_attendees,
                   eo.other_achievements
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            WHERE e.event_id = %s AND e.event_leader_id = %s;
            """,
            (event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you don't have permission to view it.", "error")
            return redirect(url_for("manage_events"))

        # Get registered volunteers (without bags/recyclables per volunteer)
        cursor.execute(
            """
            SELECT u.user_id, u.username, u.full_name, u.email, u.contact_number,
                   u.profile_image,
                   er.registration_date, er.attendance
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


# ==================== VIEW VOLUNTEER HISTORY ====================
@app.route("/event_leader/volunteers/<int:volunteer_id>/history")
@login_required
@role_required("event_leader")
def event_leader_view_volunteer_history(volunteer_id):
    """View volunteer's event history for events created by this leader."""
    with db.get_cursor() as cursor:
        # Get volunteer details
        cursor.execute(
            "SELECT user_id, username, full_name, email, contact_number, profile_image FROM users WHERE user_id = %s;",
            (volunteer_id,),
        )
        volunteer = cursor.fetchone()

        if not volunteer:
            flash("Volunteer not found.", "error")
            return redirect(url_for("manage_events"))

        # Get volunteer's event history for events created by this leader
        # Note: bags and recyclables are at event level, not per volunteer
        cursor.execute(
            """
            SELECT e.event_name, e.event_date, e.location, e.event_type,
                   er.attendance,
                   eo.bags_collected, eo.recyclables_sorted,
                   f.rating, f.comments as feedback
            FROM event_registrations er
            JOIN events e ON er.event_id = e.event_id
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            LEFT JOIN feedback f ON er.event_id = f.event_id AND er.volunteer_id = f.volunteer_id
            WHERE er.volunteer_id = %s
            AND e.event_leader_id = %s
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
            "SELECT event_name FROM events WHERE event_id = %s AND event_leader_id = %s;",
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

    with db.get_cursor() as cursor:
        # Update attendance status for this volunteer
        cursor.execute(
            """
            UPDATE event_registrations
            SET attendance = %s
            WHERE event_id = %s AND volunteer_id = %s;
            """,
            (attendance_status, event_id, volunteer_id),
        )

    flash(f"Attendance status updated for volunteer.", "success")
    return redirect(url_for("view_event_volunteers", event_id=event_id))


# ==================== RECORD EVENT OUTCOMES ====================
# ==================== RECORD EVENT OUTCOMES ====================
@app.route("/event_leader/events/<int:event_id>/outcomes", methods=["GET", "POST"])
@login_required
@role_required("event_leader")
def record_event_outcomes(event_id):
    """Record overall outcomes for an event (bags, recyclables, etc.)."""

    # Verify event belongs to this leader
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.*, 
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = %s) as total_registered,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = %s AND attendance = 'attended') as attended_count
            FROM events e
            WHERE e.event_id = %s AND e.event_leader_id = %s;
            """,
            (event_id, event_id, event_id, session["user_id"]),
        )
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you don't have permission.", "error")
            return redirect(url_for("manage_events"))

    if request.method == "POST":
        # Get form data
        bags_collected = request.form.get("bags_collected", 0)
        recyclables_sorted = request.form.get("recyclables_sorted", 0)
        other_achievements = request.form.get("other_achievements", "")

        # Convert to integers (handle empty strings)
        try:
            bags_collected = int(bags_collected) if bags_collected else 0
            recyclables_sorted = int(recyclables_sorted) if recyclables_sorted else 0
        except ValueError:
            flash("Please enter valid numbers for bags and recyclables.", "error")
            return redirect(url_for("record_event_outcomes", event_id=event_id))

        # Validate non-negative numbers
        if bags_collected < 0 or recyclables_sorted < 0:
            flash("Bags and recyclables cannot be negative.", "error")
            return redirect(url_for("record_event_outcomes", event_id=event_id))

        with db.get_cursor() as cursor:
            # Get the actual number of attendees (count from registrations)
            cursor.execute(
                """
                SELECT COUNT(*) as attended_count 
                FROM event_registrations 
                WHERE event_id = %s AND attendance = 'attended';
                """,
                (event_id,),
            )
            result = cursor.fetchone()
            attended_count = result["attended_count"] if result else 0

            # Check if outcome record already exists
            cursor.execute(
                "SELECT outcome_id FROM event_outcomes WHERE event_id = %s;",
                (event_id,),
            )
            outcome = cursor.fetchone()

            if outcome:
                # Update existing outcome
                cursor.execute(
                    """
                    UPDATE event_outcomes
                    SET bags_collected = %s, 
                        recyclables_sorted = %s,
                        number_attendees = %s,
                        other_achievements = %s,
                        recorded_by = %s,
                        recorded_at = CURRENT_TIMESTAMP
                    WHERE event_id = %s;
                    """,
                    (
                        bags_collected,
                        recyclables_sorted,
                        attended_count,
                        other_achievements,
                        session["user_id"],
                        event_id,
                    ),
                )
                flash("Event outcomes updated successfully!", "success")
            else:
                # Create new outcome
                cursor.execute(
                    """
                    INSERT INTO event_outcomes 
                    (event_id, number_attendees, bags_collected, recyclables_sorted, 
                     other_achievements, recorded_by)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        event_id,
                        attended_count,
                        bags_collected,
                        recyclables_sorted,
                        other_achievements,
                        session["user_id"],
                    ),
                )
                flash("Event outcomes recorded successfully!", "success")

        return redirect(url_for("view_event_volunteers", event_id=event_id))

    # GET request - show form with current values if they exist
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT eo.*
            FROM event_outcomes eo
            WHERE eo.event_id = %s;
            """,
            (event_id,),
        )
        existing_outcomes = cursor.fetchone()

    return render_template(
        "record_outcomes.html", event=event, outcomes=existing_outcomes
    )


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
            WHERE event_id = %s AND event_leader_id = %s;
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
            WHERE event_id = %s AND attendance = 'registered';
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


# ==================== CANCEL EVENT ====================
@app.route("/event_leader/events/<int:event_id>/cancel", methods=["POST"])
@login_required
@role_required("event_leader")
def cancel_event(event_id):
    """Cancel an event."""
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
                e.event_id, 
                e.event_name, 
                e.event_date, 
                e.location,
                e.event_type,
                COUNT(DISTINCT er.volunteer_id) as total_registered,
                COUNT(CASE WHEN er.attendance = 'attended' THEN 1 END) as attended,
                COALESCE(eo.bags_collected, 0) as total_bags,
                COALESCE(eo.recyclables_sorted, 0) as total_recyclables,
                COALESCE(eo.number_attendees, 0) as number_attendees,
                COALESCE(AVG(f.rating), 0) as avg_rating,
                COUNT(DISTINCT f.feedback_id) as feedback_count
            FROM events e
            LEFT JOIN event_registrations er ON e.event_id = er.event_id
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
            LEFT JOIN feedback f ON e.event_id = f.event_id
            WHERE e.event_leader_id = %s
            GROUP BY e.event_id, e.event_name, e.event_date, e.location, e.event_type, 
                     eo.bags_collected, eo.recyclables_sorted, eo.number_attendees
            ORDER BY e.event_date DESC;
            """,
            (session["user_id"],),
        )
        reports = cursor.fetchall()

    return render_template("event_reports.html", reports=reports)
