-- Drop existing tables first (in correct order due to foreign keys)
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS event_registrations CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS cleanup_zones CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop existing enum types
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS attendance_status CASCADE;

-- Create enum types
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE attendance_status AS ENUM ('registered', 'attended', 'absent');

-- Create users table with all required fields
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email VARCHAR(320) NOT NULL,
    person_role user_role NOT NULL DEFAULT 'volunteer',
    status user_status NOT NULL DEFAULT 'active',
    full_name VARCHAR(100) NOT NULL,
    home_address TEXT NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    environmental_interests TEXT,
    profile_image VARCHAR(255) DEFAULT 'default_profile.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cleanup_zones table
CREATE TABLE cleanup_zones (
    zone_id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    zone_description TEXT,
    location_area VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create events table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(200) NOT NULL,
    location VARCHAR(255) NOT NULL,
    zone_id INTEGER REFERENCES cleanup_zones(zone_id),
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    duration_hours DECIMAL(3,1) NOT NULL,
    supplies TEXT,
    safety_instructions TEXT,
    created_by INTEGER NOT NULL REFERENCES users(user_id),
    status VARCHAR(20) DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_event_date CHECK (event_date >= CURRENT_DATE)
);

-- Create event_registrations table
CREATE TABLE event_registrations (
    registration_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attendance_status attendance_status DEFAULT 'registered',
    bags_collected INTEGER DEFAULT 0,
    recyclables_sorted INTEGER DEFAULT 0,
    UNIQUE(event_id, volunteer_id)
);

-- Create feedback table
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, volunteer_id)
);

-- Create notifications table for reminders
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notification_type VARCHAR(50) DEFAULT 'reminder'
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(person_role);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_zone ON events(zone_id);
CREATE INDEX idx_events_creator ON events(created_by);
CREATE INDEX idx_registrations_event ON event_registrations(event_id);
CREATE INDEX idx_registrations_volunteer ON event_registrations(volunteer_id);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
