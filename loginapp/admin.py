import os
import sys
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
from loginapp import app, db
from loginapp.decorators import login_required, role_required


# ==================== ADMIN HOME ====================
@app.route("/admin/home")
@login_required
@role_required("admin")
def admin_home():
    """Admin homepage with platform statistics."""
    with db.get_cursor() as cursor:
        # Get platform-wide statistics
        cursor.execute(
            """
            SELECT 
                (SELECT COUNT(*) FROM users WHERE role = 'volunteer') as total_volunteers,
                (SELECT COUNT(*) FROM users WHERE role = 'event_leader') as total_event_leaders,
                (SELECT COUNT(*) FROM users WHERE role = 'admin') as total_admins,
                (SELECT COUNT(*) FROM events) as total_events,
                (SELECT COUNT(*) FROM events WHERE event_date >= CURRENT_DATE) as upcoming_events,
                (SELECT COUNT(*) FROM event_registrations) as total_registrations,
                (SELECT COUNT(*) FROM feedback) as total_feedback,
                (SELECT COALESCE(AVG(rating), 0) FROM feedback) as avg_rating,
                (SELECT COALESCE(SUM(bags_collected), 0) FROM event_outcomes) as total_bags,
                (SELECT COALESCE(SUM(recyclables_sorted), 0) FROM event_outcomes) as total_recyclables
            """
        )
        stats = cursor.fetchone()

        # Get recent activity
        cursor.execute(
            """
            (SELECT 'New User' as type, username as description, created_at 
             FROM users 
             ORDER BY created_at DESC LIMIT 5)
            UNION ALL
            (SELECT 'New Event', event_name, created_at 
             FROM events 
             ORDER BY created_at DESC LIMIT 5)
            ORDER BY created_at DESC LIMIT 10;
            """
        )
        recent_activity = cursor.fetchall()

    return render_template(
        "admin_home.html", stats=stats, recent_activity=recent_activity
    )


# ==================== MANAGE USERS ====================
@app.route("/admin/users")
@login_required
@role_required("admin")
def manage_users():
    """View and manage all users."""
    search = request.args.get("search", "")
    role_filter = request.args.get("role", "")
    status_filter = request.args.get("status", "")

    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if search:
        query += " AND (username ILIKE %s OR full_name ILIKE %s OR email ILIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])

    if role_filter:
        query += " AND role = %s"
        params.append(role_filter)

    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)

    query += " ORDER BY created_at DESC;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params))
        users = cursor.fetchall()

    return render_template(
        "manage_users.html",
        users=users,
        search=search,
        role_filter=role_filter,
        status_filter=status_filter,
    )


@app.route("/admin/events")
@login_required
@role_required("admin")
def admin_manage_events():
    """Admin view and manage all events."""
    # Get filter parameter (default to 'upcoming')
    filter_status = request.args.get("status", "upcoming")

    with db.get_cursor() as cursor:
        # Base query
        query = """
            SELECT e.*, u.username as event_leader_username, u.full_name as event_leader_name,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteer_count,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count,
                   eo.bags_collected,
                   eo.recyclables_sorted,
                   eo.number_attendees
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            LEFT JOIN event_outcomes eo ON e.event_id = eo.event_id
        """

        params = []

        # Add status filter if not 'all'
        if filter_status != "all":
            query += " WHERE e.status = %s"
            params.append(filter_status)

        query += " ORDER BY e.event_date DESC, e.created_at DESC;"

        cursor.execute(query, tuple(params) if params else None)
        events = cursor.fetchall()

        # Get counts for each status
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'upcoming' THEN 1 END) as upcoming_count,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
                COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_count
            FROM events;
            """
        )
        counts = cursor.fetchone()

    current_date = datetime.now().date()
    return render_template(
        "admin_manage_events.html",
        events=events,
        current_date=current_date,
        filter_status=filter_status,
        counts=counts,
    )


@app.route("/admin/volunteers/<int:volunteer_id>/history")
@login_required
@role_required("admin")
def admin_view_volunteer_history(volunteer_id):
    """Admin view volunteer's event history."""
    with db.get_cursor() as cursor:
        # Get volunteer details
        cursor.execute(
            "SELECT user_id, username, full_name, email, contact_number, profile_image FROM users WHERE user_id = %s AND role = 'volunteer';",
            (volunteer_id,),
        )
        volunteer = cursor.fetchone()

        if not volunteer:
            flash("Volunteer not found.", "error")
            return redirect(url_for("manage_users"))

        # Get volunteer's event history
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
            ORDER BY e.event_date DESC;
            """,
            (volunteer_id,),
        )
        history = cursor.fetchall()

    return render_template(
        "admin_volunteer_history.html", volunteer=volunteer, history=history
    )


@app.route("/admin/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_edit_event(event_id):
    """Admin edit any event."""
    if request.method == "POST":
        # Update event
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
            return redirect(url_for("admin_manage_events"))

    # GET request - show edit form with event leader info
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.*, u.username as event_leader_username, u.full_name as event_leader_name
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s;
            """,
            (event_id,),
        )
        event = cursor.fetchone()

        cursor.execute("SELECT DISTINCT event_type FROM events ORDER BY event_type;")
        event_types = cursor.fetchall()

    current_date = datetime.now().date()

    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("admin_manage_events"))

    return render_template(
        "edit_event.html",
        event=event,
        event_types=event_types,
        current_date=current_date,
    )


@app.route("/admin/events/<int:event_id>/cancel", methods=["POST"])
@login_required
@role_required("admin")
def admin_cancel_event(event_id):
    """Admin cancel an event."""
    with db.get_cursor() as cursor:
        cursor.execute(
            "UPDATE events SET status = 'cancelled' WHERE event_id = %s;", (event_id,)
        )
        flash("Event has been cancelled.", "success")

    return redirect(url_for("admin_manage_events"))


# ==================== VIEW USER DETAILS ====================
@app.route("/admin/users/<int:user_id>")
@login_required
@role_required("admin")
def view_user(user_id):
    """View detailed user information."""
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.", "error")
            return redirect(url_for("manage_users"))

        # Get user's event registrations
        if user["role"] == "volunteer":
            cursor.execute(
                """
                SELECT e.event_name, e.event_date, er.attendance, eo.bags_collected, eo.recyclables_sorted
                FROM event_registrations er
                JOIN events e ON er.event_id = e.event_id
                left JOIN event_outcomes eo ON e.event_id = eo.event_id
                WHERE er.volunteer_id = %s
                ORDER BY e.event_date DESC
                LIMIT 10;
            """,
                (user_id,),
            )
            events = cursor.fetchall()
        else:
            # Get events created by this user
            cursor.execute(
                """
                SELECT event_name, event_date, 
                       (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteers
                FROM events e
                WHERE event_leader_id = %s
                ORDER BY event_date DESC
                LIMIT 10;
            """,
                (user_id,),
            )
            events = cursor.fetchall()

    return render_template("view_user.html", user=user, events=events)


# ==================== CHANGE USER STATUS ====================
@app.route("/admin/users/<int:user_id>/toggle-status", methods=["POST"])
@login_required
@role_required("admin")
def toggle_user_status(user_id):
    """Activate or deactivate a user account."""
    new_status = request.form.get("status")

    with db.get_cursor() as cursor:
        cursor.execute(
            "UPDATE users SET status = %s WHERE user_id = %s RETURNING username;",
            (new_status, user_id),
        )
        user = cursor.fetchone()
        if user:
            flash(f"User {user['username']} status changed to {new_status}.", "success")

    return redirect(url_for("manage_users"))


# ==================== ADMIN REPORTS ====================
@app.route("/admin/reports")
@login_required
@role_required("admin")
def admin_reports():
    """View platform-wide reports."""
    with db.get_cursor() as cursor:
        # Events by month
        cursor.execute(
            """
            SELECT TO_CHAR(event_date, 'YYYY-MM') as month,
                   COUNT(*) as event_count,
                   COUNT(DISTINCT event_leader_id) as unique_leaders,
                   SUM((SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id)) as total_volunteers
            FROM events e
            WHERE event_date >= CURRENT_DATE - INTERVAL '6 months'
            GROUP BY TO_CHAR(event_date, 'YYYY-MM')
            ORDER BY month DESC;
        """
        )
        monthly_stats = cursor.fetchall()

        # Top volunteers
        # order by sum of total bags collected and recyclables sorted to get overall impact score
        cursor.execute(
            """
            SELECT *
                FROM (
                    SELECT u.user_id, u.username, u.full_name,
                        COUNT(DISTINCT er.event_id) as events_attended,
                        SUM(eo.bags_collected) as total_bags,
                        SUM(eo.recyclables_sorted) as total_recyclables,
                        AVG(f.rating) as avg_rating
                    FROM users u
                    JOIN event_registrations er ON u.user_id = er.volunteer_id
                    LEFT JOIN event_outcomes eo ON er.event_id = eo.event_id
                    LEFT JOIN feedback f ON u.user_id = f.volunteer_id
                    WHERE u.role = 'volunteer' AND er.attendance = 'attended'
                    GROUP BY u.user_id, u.username, u.full_name
                ) v
            ORDER BY (total_bags + total_recyclables) DESC, avg_rating DESC
            LIMIT 10;
        """
        )
        top_volunteers = cursor.fetchall()

    return render_template(
        "admin_reports.html", monthly_stats=monthly_stats, top_volunteers=top_volunteers
    )
