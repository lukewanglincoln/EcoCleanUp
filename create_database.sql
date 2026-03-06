-- Drop existing tables first (in correct order due to foreign keys)
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS event_registrations CASCADE;
DROP TABLE IF EXISTS event_outcomes CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop existing enum types
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS event_status CASCADE;
DROP TYPE IF EXISTS attendance_status CASCADE;

-- Create enum types
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE event_status AS ENUM ('upcoming', 'completed', 'cancelled');
CREATE TYPE attendance_status AS ENUM ('registered', 'attended', 'absent');

-- Create users table with all required fields
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(320) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    home_address TEXT NOT NULL,
    profile_image VARCHAR(255) DEFAULT 'default_profile.jpg',
    environmental_interests TEXT,
    role user_role NOT NULL DEFAULT 'volunteer',
    status user_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create events table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(200) NOT NULL,
    event_leader_id INTEGER NOT NULL REFERENCES users(user_id),
    location VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration DECIMAL(3,1) NOT NULL,
    description TEXT,
    supplies TEXT,
    safety_instructions TEXT,
    status event_status NOT NULL DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- CONSTRAINT valid_event_date CHECK (event_date >= CURRENT_DATE)
);

-- Create event_registrations table
CREATE TABLE event_registrations (
    registration_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attendance attendance_status DEFAULT 'registered',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, volunteer_id)
);

-- Create event_outcomes table
CREATE TABLE event_outcomes (
    outcome_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    number_attendees INTEGER NOT NULL,
    bags_collected INTEGER NOT NULL,
    recyclables_sorted INTEGER NOT NULL,
    other_achievements TEXT,
    recorded_by INTEGER NOT NULL REFERENCES users(user_id),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_creator ON events(event_leader_id);
CREATE INDEX idx_registrations_event ON event_registrations(event_id);
CREATE INDEX idx_registrations_volunteer ON event_registrations(volunteer_id);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
