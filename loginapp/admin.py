import os
import sys
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
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT e.*, u.username as event_leader_username, u.full_name as event_leader_name,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id) as volunteer_count,
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            ORDER BY e.event_date DESC, e.created_at DESC;
            """
        )
        events = cursor.fetchall()

    return render_template("admin_manage_events.html", events=events)


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
        event_date = request.form.get("event_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        duration = request.form.get("duration")
        supplies = request.form.get("supplies")
        safety_instructions = request.form.get("safety_instructions")
        status = request.form.get("status")

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE events 
                SET event_name = %s, location = %s, event_date = %s,
                    start_time = %s, end_time = %s, duration = %s, supplies = %s,
                    safety_instructions = %s, status = %s
                WHERE event_id = %s;
            """,
                (
                    event_name,
                    location,
                    event_date,
                    start_time,
                    end_time,
                    duration,
                    supplies,
                    safety_instructions,
                    status,
                    event_id,
                ),
            )
            flash("Event updated successfully!", "success")
            return redirect(url_for("admin_manage_events"))

    # GET request - show edit form
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE event_id = %s;", (event_id,))
        event = cursor.fetchone()

        cursor.execute(
            "SELECT zone_id, zone_name FROM cleanup_zones ORDER BY zone_name;"
        )
        zones = cursor.fetchall()

    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("admin_manage_events"))

    return render_template("admin_edit_event.html", event=event, zones=zones)


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
        if user["person_role"] == "volunteer":
            cursor.execute(
                """
                SELECT e.event_name, e.event_date, er.attendance_status, er.bags_collected
                FROM event_registrations er
                JOIN events e ON er.event_id = e.event_id
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
                WHERE created_by = %s
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
        flash(f"User {user['username']} status changed to {new_status}.", "success")

    return redirect(url_for("manage_users"))


# ==================== MANAGE CLEANUP ZONES ====================
@app.route("/admin/zones")
@login_required
@role_required("admin")
def manage_zones():
    """View and manage cleanup zones."""
    with db.get_cursor() as cursor:
        cursor.execute(
            """
            SELECT z.*, 
                   (SELECT COUNT(*) FROM events WHERE zone_id = z.zone_id) as event_count
            FROM cleanup_zones z
            ORDER BY zone_name;
        """
        )
        zones = cursor.fetchall()

    return render_template("manage_zones.html", zones=zones)


# ==================== CREATE ZONE ====================
@app.route("/admin/zones/create", methods=["POST"])
@login_required
@role_required("admin")
def create_zone():
    """Create a new cleanup zone."""
    zone_name = request.form.get("zone_name")
    zone_description = request.form.get("zone_description")
    location_area = request.form.get("location_area")

    with db.get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO cleanup_zones (zone_name, zone_description, location_area)
            VALUES (%s, %s, %s);
        """,
            (zone_name, zone_description, location_area),
        )
        flash(f"Zone '{zone_name}' created successfully!", "success")

    return redirect(url_for("manage_zones"))


# ==================== EDIT ZONE ====================
@app.route("/admin/zones/edit/<int:zone_id>", methods=["POST"])
@login_required
@role_required("admin")
def edit_zone(zone_id):
    """Edit an existing cleanup zone."""
    zone_name = request.form.get("zone_name")
    zone_description = request.form.get("zone_description")
    location_area = request.form.get("location_area")

    with db.get_cursor() as cursor:
        cursor.execute(
            """
            UPDATE cleanup_zones
            SET zone_name = %s, zone_description = %s, location_area = %s
            WHERE zone_id = %s;
        """,
            (zone_name, zone_description, location_area, zone_id),
        )
        flash("Zone updated successfully!", "success")

    return redirect(url_for("manage_zones"))


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
                   COUNT(DISTINCT created_by) as unique_leaders,
                   SUM((SELECT COUNT(*) FROM event_registrations WHERE event_id = e.event_id)) as total_volunteers
            FROM events e
            WHERE event_date >= CURRENT_DATE - INTERVAL '6 months'
            GROUP BY TO_CHAR(event_date, 'YYYY-MM')
            ORDER BY month DESC;
        """
        )
        monthly_stats = cursor.fetchall()

        # Top volunteers
        cursor.execute(
            """
            SELECT u.user_id, u.username, u.full_name,
                   COUNT(DISTINCT er.event_id) as events_attended,
                   SUM(er.bags_collected) as total_bags,
                   AVG(f.rating) as avg_rating
            FROM users u
            JOIN event_registrations er ON u.user_id = er.volunteer_id
            LEFT JOIN feedback f ON u.user_id = f.volunteer_id
            WHERE u.person_role = 'volunteer' AND er.attendance_status = 'attended'
            GROUP BY u.user_id, u.username, u.full_name
            HAVING COUNT(DISTINCT er.event_id) > 0
            ORDER BY total_bags DESC
            LIMIT 10;
        """
        )
        top_volunteers = cursor.fetchall()

        # Zone statistics
        cursor.execute(
            """
            SELECT z.zone_name,
                   COUNT(DISTINCT e.event_id) as events,
                   COUNT(DISTINCT er.volunteer_id) as unique_volunteers,
                   COALESCE(SUM(er.bags_collected), 0) as bags_collected
            FROM cleanup_zones z
            LEFT JOIN events e ON z.zone_id = e.zone_id
            LEFT JOIN event_registrations er ON e.event_id = er.event_id
            GROUP BY z.zone_id, z.zone_name
            ORDER BY bags_collected DESC;
        """
        )
        zone_stats = cursor.fetchall()

    return render_template(
        "admin_reports.html",
        monthly_stats=monthly_stats,
        top_volunteers=top_volunteers,
        zone_stats=zone_stats,
    )
