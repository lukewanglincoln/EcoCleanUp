# EcoCleanUp Hub - Community Cleanup Management System
A web-based platform for managing community cleanup events, built with Python Flask and PostgreSQL. This system enables volunteers to discover and register for cleanup events, event leaders to organize and track events, and administrators to oversee the entire platform.

## Live Demo
[EcoCleanUp Hub](https://lukewang639.pythonanywhere.com)

## System Login
EcoCleanUp Hub addresses the challenges faced by community cleanup initiatives by providing:

For Volunteers: A centralized platform to discover local cleanup events, register participation, track personal impact, and provide feedback

For Event Leaders: Tools to create and manage events, coordinate volunteers, record cleanup outcomes, and generate reports

For Administrators: Comprehensive oversight of users, events, and platform-wide analytics

The application features role-based access control, responsive design for mobile and desktop use, and a sustainability-focused theme.

### Test Accounts
use the following username and password Password123! to log in as different roles:
- Volunteer: 
    sarah_wilson, mike_thompson, emma_chen, james_kumar, lisa_rodriguez, david_park, rachel_smith, tom_williams, anita_patel, kevin_brown, olivia_taylor, william_anderson, sophie_martin, liam_white, chloe_harris, jack_clark, emily_lewis, thomas_walker, grace_hall, benjamin_young
- Event Leader:
    helen_cooper, robert_foster, maria_santos, peter_nguyen, julia_adams
- Administrator:
    admin_sarah, admin_mark

## Technology Stack
Backend: Python, Flask
Database: PostgreSQL
Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
Authentication: Flask-Bcrypt for password hashing
Session Management: Flask sessions
Icons: Bootstrap Icons

## Local Setup
1. Setup Database
```
export PGPASSWORD='password'
psql -h localhost -p 5432 -U username -d 'echocleanup' -f ./create_database.sql
psql -h localhost -p 5432 -U username -d 'echocleanup' -f ./populate_database.sql
```
Remember to complete loginapp/connect.py with the same credential.
```
dbuser = 'username'
dbpass = 'password'
dbhost = 'localhost'
dbport = 5432
dbname = 'ecocleanup'
```
2. Clone the repository
```
git clone https://github.com/lukewanglincoln/EcoCleanUp
cd EcoCleanUp
python -m venv ./venv
source venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Open your browser and navigate to http://localhost:8004


## GenAI Acknowledgement
The following tools and prompts were used in the development of this project:
1. Microsoft Copilot
    Copilot was used for inline code suggestions and auto-completion while writing the Flask application, database interactions, and frontend templates. 
2. Deepseek
    The following prompts were used:
    - Create a PostgreSQL database schema based on the following ERD. This should include the table users, events, events_registrations, event_outcomes, and feedback.
    - Generate some test data according to the database schema that you have created. This should include at least 20 volunteers, 5 event leaders, 2 administrators, 20 events (including past and upcoming events), 20 registrations, and some feedbacks.
    - read the requirements of my assignment and generate a list of features that I need to implement in my web application.
    - Generate a baseline Flask application by using the database schema and the list of features that I have provided. This should include the necessary routes, templates, and database interactions to support the features of my web application.
    - Show the number if the feedbacks for each events, and I can click the feedback to see the details of the feedbacks.
    - Improve the code so the volunteers' attendance should consider the completed events only, but not the upcoming events.
    - Add a new feature to allow volunteers to cancel their registration for an event, and update the event's available slots accordingly.
    - Both event leaders and administrators should be able to edit the details of an event.
    - improve the report page to include a summary of the each event leader. 
    - Split the events into a few parts including upcoming, completed, cancelled, and all events. Each part should be shown on their own tab. 
    - bags collected and recyclables sorted should be only shown for completed events. 
    - write a sketch of the README file containing the GenAI acknowledgement section, including the tools and prompts that I have used in the development of this project.
    - improve my improve admin_view_volunteer_history so I can use volunteer_history.html for both event leaders and administrators.
