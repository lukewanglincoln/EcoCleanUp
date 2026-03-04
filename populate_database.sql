-- First, insert cleanup zones (no dependencies)
INSERT INTO cleanup_zones (zone_name, zone_description, location_area) VALUES
('Beachfront Paradise', 'Coastal area with sandy beaches and rocky shores', 'North Beach District'),
('Riverside Walk', 'Riverbank area popular for walking and fishing', 'East River Park'),
('City Park', 'Central urban park with walking trails', 'Downtown'),
('Green Valley Reserve', 'Native bush reserve with walking tracks', 'Western Hills'),
('Lakeview Shores', 'Lakefront area with picnic spots', 'South Lakeside');

-- Insert volunteers (20)
-- Note: Password hashes are for demo purposes - use password_hash_generator.py for actual hashes
-- All passwords are 'Password123!' for demo purposes
INSERT INTO users (username, password_hash, email, person_role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('sarah_wilson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'sarah.wilson@email.com', 'volunteer', 'active', 'Sarah Wilson', '42 Beach Road, North Beach', '021-555-0123', 'Beach cleanups, Recycling, Marine conservation', 'sarah_wilson.jpg'),
('mike_thompson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'mike.thompson@email.com', 'volunteer', 'active', 'Mike Thompson', '15 Valley Road, Western Hills', '022-555-0124', 'Tree planting, Native bush restoration', 'mike_thompson.jpg'),
('emma_chen', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'emma.chen@email.com', 'volunteer', 'active', 'Emma Chen', '78 Park Lane, Central City', '027-555-0125', 'Urban gardening, Recycling education', 'emma_chen.jpg'),
('james_kumar', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'james.kumar@email.com', 'volunteer', 'active', 'James Kumar', '23 River Terrace, Eastside', '021-555-0126', 'River cleanups, Plastic reduction', 'james_kumar.jpg'),
('lisa_rodriguez', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'lisa.rodriguez@email.com', 'volunteer', 'active', 'Lisa Rodriguez', '56 Lakeview Drive, South Lakeside', '022-555-0127', 'Lake conservation, Wildlife protection', 'lisa_rodriguez.jpg'),
('david_park', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'david.park@email.com', 'volunteer', 'active', 'David Park', '89 Central Avenue, Downtown', '027-555-0128', 'Community gardening, Composting', 'david_park.jpg'),
('rachel_smith', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'rachel.smith@email.com', 'volunteer', 'active', 'Rachel Smith', '34 North Shore Road', '021-555-0129', 'Beach cleanups, Marine biology', 'rachel_smith.jpg'),
('tom_williams', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'tom.williams@email.com', 'volunteer', 'active', 'Tom Williams', '67 Forest Hill Road', '022-555-0130', 'Native planting, Weed control', 'tom_williams.jpg'),
('anita_patel', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'anita.patel@email.com', 'volunteer', 'active', 'Anita Patel', '12 Riverside Drive', '027-555-0131', 'Water conservation, River cleanups', 'anita_patel.jpg'),
('kevin_brown', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'kevin.brown@email.com', 'volunteer', 'active', 'Kevin Brown', '45 Mountain View Road', '021-555-0132', 'Trail maintenance, Litter collection', 'kevin_brown.jpg'),
('olivia_taylor', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'olivia.taylor@email.com', 'volunteer', 'active', 'Olivia Taylor', '23 Beach Road, North Beach', '022-555-0133', 'Beach cleanups, Marine conservation', 'olivia_taylor.jpg'),
('william_anderson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'william.anderson@email.com', 'volunteer', 'active', 'William Anderson', '78 Valley Road', '027-555-0134', 'Native bush restoration', 'william_anderson.jpg'),
('sophie_martin', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'sophie.martin@email.com', 'volunteer', 'active', 'Sophie Martin', '34 Park Avenue', '021-555-0135', 'Urban gardening', 'sophie_martin.jpg'),
('liam_white', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'liam.white@email.com', 'volunteer', 'active', 'Liam White', '56 River Road', '022-555-0136', 'River cleanups', 'liam_white.jpg'),
('chloe_harris', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'chloe.harris@email.com', 'volunteer', 'active', 'Chloe Harris', '89 Lake Terrace', '027-555-0137', 'Lake conservation', 'chloe_harris.jpg'),
('jack_clark', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'jack.clark@email.com', 'volunteer', 'active', 'Jack Clark', '12 Mountain Road', '021-555-0138', 'Trail maintenance', 'jack_clark.jpg'),
('emily_lewis', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'emily.lewis@email.com', 'volunteer', 'active', 'Emily Lewis', '45 Forest Lane', '022-555-0139', 'Tree planting', 'emily_lewis.jpg'),
('thomas_walker', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'thomas.walker@email.com', 'volunteer', 'active', 'Thomas Walker', '67 Beach Parade', '027-555-0140', 'Beach cleanups', 'thomas_walker.jpg'),
('grace_hall', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'grace.hall@email.com', 'volunteer', 'active', 'Grace Hall', '23 Valley View', '021-555-0141', 'Recycling education', 'grace_hall.jpg'),
('benjamin_young', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'benjamin.young@email.com', 'volunteer', 'active', 'Benjamin Young', '78 Riverside Drive', '022-555-0142', 'Plastic reduction', 'benjamin_young.jpg');

-- Insert event leaders (5)
INSERT INTO users (username, password_hash, email, person_role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('helen_cooper', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'helen.cooper@email.com', 'event_leader', 'active', 'Helen Cooper', '234 Beach Parade, North Beach', '027-555-0201', 'Coastal conservation, Event coordination', 'helen_cooper.jpg'),
('robert_foster', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'robert.foster@email.com', 'event_leader', 'active', 'Robert Foster', '156 Park Road, Central City', '022-555-0202', 'Park maintenance, Volunteer management', 'robert_foster.jpg'),
('maria_santos', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'maria.santos@email.com', 'event_leader', 'active', 'Maria Santos', '89 Valley View, Western Hills', '021-555-0203', 'Bush regeneration, Community engagement', 'maria_santos.jpg'),
('peter_nguyen', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'peter.nguyen@email.com', 'event_leader', 'active', 'Peter Nguyen', '45 Lake Road, South Lakeside', '027-555-0204', 'Lake conservation, Environmental education', 'peter_nguyen.jpg'),
('julia_adams', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'julia.adams@email.com', 'event_leader', 'active', 'Julia Adams', '67 River Terrace, Eastside', '022-555-0205', 'River restoration, Youth programs', 'julia_adams.jpg');

-- Insert admins (2)
INSERT INTO users (username, password_hash, email, person_role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('admin_sarah', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'sarah.admin@ecocleanup.org', 'admin', 'active', 'Sarah Johnson', '1 Admin Plaza, Central City', '021-555-0301', 'Sustainability strategy, Community development', 'admin_sarah.jpg'),
('admin_mark', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'mark.admin@ecocleanup.org', 'admin', 'active', 'Mark Williams', '2 Admin Plaza, Central City', '022-555-0302', 'Environmental policy, Data analysis', 'admin_mark.jpg');

-- Insert events (20+)
INSERT INTO events (event_name, location, zone_id, event_date, event_time, duration_hours, supplies, safety_instructions, created_by, status) VALUES
('North Beach Spring Clean', 'North Beach Main Access', 1, '2026-04-15', '09:00', 3.0, 'Gloves, bags, litter pickers provided', 'Wear sunscreen, closed shoes, bring water', 21, 'upcoming'),
('Riverside Litter Collection', 'Riverside Park Entry', 2, '2026-04-16', '10:00', 2.5, 'Bags and gloves available', 'Stay away from water edge, wear sturdy boots', 22, 'upcoming'),
('City Park Beautification', 'Central Park Pavilion', 3, '2026-04-17', '13:00', 3.0, 'Tools provided, bring own gloves', 'Watch for uneven ground, bring hat', 22, 'upcoming'),
('Green Valley Weed Control', 'Valley Trail Head', 4, '2026-04-18', '09:30', 4.0, 'Tools and gloves provided', 'Long pants recommended, check for ticks', 23, 'upcoming'),
('Lakeview Cleanup', 'Lakeview Boat Ramp', 5, '2026-04-19', '14:00', 2.0, 'Bags, gloves, grabbers', 'Life jackets available if needed', 23, 'upcoming'),
('Beach Microplastics Survey', 'North Beach South End', 1, '2026-04-20', '10:00', 3.0, 'Sieves, containers, gloves', 'Bring sun protection', 24, 'upcoming'),
('Riverside Planting Day', 'Riverside Reserve', 2, '2026-04-21', '09:00', 4.0, 'Plants, tools, mulch', 'Wear gardening gloves', 24, 'upcoming'),
('Park Litter Blitz', 'City Park East', 3, '2026-04-22', '13:30', 2.5, 'All equipment provided', 'Earth Day event', 25, 'upcoming'),
('Valley Trail Maintenance', 'Green Valley Trail', 4, '2026-04-23', '09:00', 3.5, 'Tools, gloves, safety vests', 'Stay on marked trails', 21, 'upcoming'),
('Lake Weed Collection', 'Lakeview East', 5, '2026-04-24', '10:30', 3.0, 'Nets, bags, gloves', 'Waterproof boots recommended', 22, 'upcoming'),
('North Beach Evening Cleanup', 'North Beach Main Access', 1, '2026-04-25', '17:00', 2.0, 'Gloves, bags, torches', 'Bring torch, wear reflective gear', 23, 'upcoming'),
('Riverside Education Day', 'Riverside Park', 2, '2026-04-26', '13:00', 3.0, 'Educational materials', 'Family friendly event', 24, 'upcoming'),
('City Park Tree Planting', 'Central Park', 3, '2026-04-27', '09:30', 4.0, 'Trees, tools, mulch', 'Sturdy boots required', 25, 'upcoming'),
('Green Valley Bird Habitat', 'Valley Reserve', 4, '2026-04-28', '10:00', 3.0, 'Nest boxes, tools', 'Quiet event', 21, 'upcoming'),
('Lake Shore Cleanup', 'Lakeview South', 5, '2026-04-29', '14:00', 2.5, 'Bags, gloves', 'Sun protection recommended', 22, 'upcoming'),
('Beach Dune Restoration', 'North Beach Dunes', 1, '2026-04-30', '09:00', 4.0, 'Plants, sand, tools', 'Bring water and sunscreen', 23, 'upcoming'),
('Riverside Water Quality', 'Riverside Bridge', 2, '2026-05-01', '13:00', 2.0, 'Testing kits, gloves', 'Water contact possible', 24, 'upcoming'),
('Park Waste Audit', 'City Park Depot', 3, '2026-05-02', '10:00', 3.0, 'Sorting equipment', 'Gloves required', 25, 'upcoming'),
('Valley Pest Control', 'Green Valley', 4, '2026-05-03', '08:30', 5.0, 'Traps, bait, gloves', 'Training provided', 21, 'upcoming'),
('Lake Native Planting', 'Lakeview North', 5, '2026-05-04', '09:30', 3.5, 'Native plants, tools', 'Waterfront planting', 22, 'upcoming');

-- Insert event registrations (20+)
INSERT INTO event_registrations (event_id, volunteer_id, attendance_status) VALUES
(1, 1, 'registered'),
(1, 2, 'registered'),
(1, 3, 'registered'),
(1, 4, 'registered'),
(1, 5, 'registered'),
(2, 6, 'registered'),
(2, 7, 'registered'),
(2, 8, 'registered'),
(3, 9, 'registered'),
(3, 10, 'registered'),
(4, 11, 'registered'),
(4, 12, 'registered'),
(5, 13, 'registered'),
(5, 14, 'registered'),
(6, 15, 'registered'),
(6, 16, 'registered'),
(7, 17, 'registered'),
(7, 18, 'registered'),
(8, 19, 'registered'),
(8, 20, 'registered'),
(9, 1, 'registered'),
(9, 3, 'registered'),
(10, 5, 'registered'),
(10, 7, 'registered');

-- Insert feedback samples
INSERT INTO feedback (event_id, volunteer_id, rating, comments) VALUES
(1, 1, 5, 'Great event, well organized! Found lots of litter to clean up. The beach looks much better now.'),
(1, 2, 4, 'Good turnout, supplies were adequate. Would suggest more bags next time.'),
(1, 3, 5, 'Excellent organization and safety briefing. Will definitely join again!'),
(2, 6, 5, 'Beautiful location, felt great to help clean it up. The river area is much cleaner now.'),
(2, 7, 4, 'Productive morning, good team coordination.'),
(3, 9, 5, 'The park looks so much better now! Great team effort.'),
(3, 10, 5, 'Very satisfying work, well organized event.'),
(4, 11, 4, 'Hard work but rewarding, good safety briefing.'),
(5, 13, 5, 'Beautiful lake area, collected lots of rubbish. Very satisfying!'),
(6, 15, 4, 'Interesting microplastics survey, learned a lot.'),
(7, 17, 5, 'Great planting day, the area looks transformed!');

-- Insert notifications for reminders
INSERT INTO notifications (user_id, event_id, message, notification_type) VALUES
(1, 1, 'Reminder: North Beach Spring Clean is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder'),
(2, 1, 'Reminder: North Beach Spring Clean is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder'),
(3, 1, 'Reminder: North Beach Spring Clean is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder'),
(4, 1, 'Reminder: North Beach Spring Clean is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder'),
(5, 1, 'Reminder: North Beach Spring Clean is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder'),
(6, 2, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder'),
(7, 2, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder'),
(8, 2, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder'),
(9, 3, 'Reminder: City Park Beautification is tomorrow at 1:00 PM. Bring hat and gloves.', 'reminder'),
(10, 3, 'Reminder: City Park Beautification is tomorrow at 1:00 PM. Bring hat and gloves.', 'reminder');
