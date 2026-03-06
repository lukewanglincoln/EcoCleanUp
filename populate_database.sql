-- ============================================
-- POPULATE DATABASE FOR ECOCLEANUP HUB
-- ============================================

-- First, insert users (volunteers, event leaders, admins)
-- Note: All passwords are 'Password123!' for demo purposes
-- Hash: $2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG

-- Insert volunteers (20)
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('sarah_wilson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Sarah Wilson', 'sarah.wilson@email.com', '021-555-0123', '42 Beach Road, North Beach', 'default_profile.jpg', 'Beach cleanups, Recycling, Marine conservation', 'volunteer', 'active'),
('mike_thompson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Mike Thompson', 'mike.thompson@email.com', '022-555-0124', '15 Valley Road, Western Hills', 'default_profile.jpg', 'Tree planting, Native bush restoration', 'volunteer', 'active'),
('emma_chen', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Emma Chen', 'emma.chen@email.com', '027-555-0125', '78 Park Lane, Central City', 'default_profile.jpg', 'Urban gardening, Recycling education', 'volunteer', 'active'),
('james_kumar', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'James Kumar', 'james.kumar@email.com', '021-555-0126', '23 River Terrace, Eastside', 'default_profile.jpg', 'River cleanups, Plastic reduction', 'volunteer', 'active'),
('lisa_rodriguez', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Lisa Rodriguez', 'lisa.rodriguez@email.com', '022-555-0127', '56 Lakeview Drive, South Lakeside', 'default_profile.jpg', 'Lake conservation, Wildlife protection', 'volunteer', 'active'),
('david_park', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'David Park', 'david.park@email.com', '027-555-0128', '89 Central Avenue, Downtown', 'default_profile.jpg', 'Community gardening, Composting', 'volunteer', 'active'),
('rachel_smith', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Rachel Smith', 'rachel.smith@email.com', '021-555-0129', '34 North Shore Road', 'default_profile.jpg', 'Beach cleanups, Marine biology', 'volunteer', 'active'),
('tom_williams', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Tom Williams', 'tom.williams@email.com', '022-555-0130', '67 Forest Hill Road', 'default_profile.jpg', 'Native planting, Weed control', 'volunteer', 'active'),
('anita_patel', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Anita Patel', 'anita.patel@email.com', '027-555-0131', '12 Riverside Drive', 'default_profile.jpg', 'Water conservation, River cleanups', 'volunteer', 'active'),
('kevin_brown', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Kevin Brown', 'kevin.brown@email.com', '021-555-0132', '45 Mountain View Road', 'default_profile.jpg', 'Trail maintenance, Litter collection', 'volunteer', 'active'),
('olivia_taylor', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Olivia Taylor', 'olivia.taylor@email.com', '022-555-0133', '23 Beach Road, North Beach', 'default_profile.jpg', 'Beach cleanups, Marine conservation', 'volunteer', 'active'),
('william_anderson', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'William Anderson', 'william.anderson@email.com', '027-555-0134', '78 Valley Road', 'default_profile.jpg', 'Native bush restoration', 'volunteer', 'active'),
('sophie_martin', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Sophie Martin', 'sophie.martin@email.com', '021-555-0135', '34 Park Avenue', 'default_profile.jpg', 'Urban gardening', 'volunteer', 'active'),
('liam_white', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Liam White', 'liam.white@email.com', '022-555-0136', '56 River Road', 'default_profile.jpg', 'River cleanups', 'volunteer', 'active'),
('chloe_harris', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Chloe Harris', 'chloe.harris@email.com', '027-555-0137', '89 Lake Terrace', 'default_profile.jpg', 'Lake conservation', 'volunteer', 'active'),
('jack_clark', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Jack Clark', 'jack.clark@email.com', '021-555-0138', '12 Mountain Road', 'default_profile.jpg', 'Trail maintenance', 'volunteer', 'active'),
('emily_lewis', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Emily Lewis', 'emily.lewis@email.com', '022-555-0139', '45 Forest Lane', 'default_profile.jpg', 'Tree planting', 'volunteer', 'active'),
('thomas_walker', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Thomas Walker', 'thomas.walker@email.com', '027-555-0140', '67 Beach Parade', 'default_profile.jpg', 'Beach cleanups', 'volunteer', 'active'),
('grace_hall', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Grace Hall', 'grace.hall@email.com', '021-555-0141', '23 Valley View', 'default_profile.jpg', 'Recycling education', 'volunteer', 'active'),
('benjamin_young', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Benjamin Young', 'benjamin.young@email.com', '022-555-0142', '78 Riverside Drive', 'default_profile.jpg', 'Plastic reduction', 'volunteer', 'active');

-- Insert event leaders (5)
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('helen_cooper', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Helen Cooper', 'helen.cooper@email.com', '027-555-0201', '234 Beach Parade, North Beach', 'default_profile.jpg', 'Coastal conservation, Event coordination', 'event_leader', 'active'),
('robert_foster', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Robert Foster', 'robert.foster@email.com', '022-555-0202', '156 Park Road, Central City', 'default_profile.jpg', 'Park maintenance, Volunteer management', 'event_leader', 'active'),
('maria_santos', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Maria Santos', 'maria.santos@email.com', '021-555-0203', '89 Valley View, Western Hills', 'default_profile.jpg', 'Bush regeneration, Community engagement', 'event_leader', 'active'),
('peter_nguyen', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Peter Nguyen', 'peter.nguyen@email.com', '027-555-0204', '45 Lake Road, South Lakeside', 'default_profile.jpg', 'Lake conservation, Environmental education', 'event_leader', 'active'),
('julia_adams', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Julia Adams', 'julia.adams@email.com', '022-555-0205', '67 River Terrace, Eastside', 'default_profile.jpg', 'River restoration, Youth programs', 'event_leader', 'active');

-- Insert admins (2)
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('admin_sarah', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Sarah Johnson', 'sarah.admin@ecocleanup.org', '021-555-0301', '1 Admin Plaza, Central City', 'default_profile.jpg', 'Sustainability strategy, Community development', 'admin', 'active'),
('admin_mark', '$2b$12$AZ6UeeeJKOQLsx8It1LFsO9Z4PhOXMgnRwiPywAFPE65NHBAakiSG', 'Mark Williams', 'mark.admin@ecocleanup.org', '022-555-0302', '2 Admin Plaza, Central City', 'default_profile.jpg', 'Environmental policy, Data analysis', 'admin', 'active');


-- Insert events (both past and upcoming)
-- Note: event_leader_id references users with role 'event_leader' (IDs 21-25)

-- PAST EVENTS (2025 data) - All should be 'completed'
INSERT INTO events (event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions, status) VALUES
('North Beach Spring Clean 2025', 21, 'North Beach Main Access', 'Beach Cleanup', '2025-03-15', '09:00', '12:00', 3.0, 'Annual spring cleanup of North Beach', 'Gloves, bags, litter pickers', 'Wear sunscreen, closed shoes, bring water', 'completed'),
('Riverside Litter Collection', 22, 'Riverside Park', 'River Cleanup', '2025-03-20', '10:00', '13:00', 3.0, 'Cleaning up the riverbank area', 'Bags, gloves, grabbers', 'Stay away from water edge, wear sturdy boots', 'completed'),
('City Park Beautification', 22, 'Central Park', 'Park Cleanup', '2025-04-05', '13:00', '16:00', 3.0, 'Spring cleanup of Central Park', 'Tools, gloves, bags', 'Watch for uneven ground, bring hat', 'completed'),
('Green Valley Weed Control', 23, 'Valley Trail Head', 'Weed Control', '2025-04-12', '09:30', '13:30', 4.0, 'Removing invasive weeds from native bush', 'Tools, gloves, bags', 'Long pants recommended, check for ticks', 'completed'),
('Lakeview Cleanup', 23, 'Lakeview Boat Ramp', 'Lake Cleanup', '2025-05-02', '14:00', '16:00', 2.0, 'Cleaning up around the lake shore', 'Bags, gloves, grabbers', 'Life jackets available if needed', 'completed'),
('Beach Microplastics Survey', 24, 'North Beach South End', 'Beach Cleanup', '2025-05-18', '10:00', '13:00', 3.0, 'Collecting microplastics for research', 'Sieves, containers, gloves', 'Bring sun protection', 'completed'),
('Riverside Planting Day', 24, 'Riverside Reserve', 'Tree Planting', '2025-06-08', '09:00', '13:00', 4.0, 'Planting native trees along the river', 'Plants, tools, mulch', 'Wear gardening gloves', 'completed'),
('Park Litter Blitz', 25, 'City Park East', 'Park Cleanup', '2025-06-22', '13:30', '16:00', 2.5, 'Earth Day cleanup event', 'All equipment provided', 'Bring water and sunscreen', 'completed'),
('Valley Trail Maintenance', 21, 'Green Valley Trail', 'Trail Maintenance', '2025-07-05', '09:00', '12:30', 3.5, 'Clearing and maintaining walking trails', 'Tools, gloves, safety vests', 'Stay on marked trails', 'completed'),
('Lake Weed Collection', 22, 'Lakeview East', 'Lake Cleanup', '2025-07-19', '10:30', '13:30', 3.0, 'Removing invasive aquatic weeds', 'Nets, bags, gloves', 'Waterproof boots recommended', 'completed'),
('North Beach Evening Cleanup', 23, 'North Beach Main Access', 'Beach Cleanup', '2025-08-08', '17:00', '19:00', 2.0, 'Evening cleanup session', 'Gloves, bags, torches', 'Bring torch, wear reflective gear', 'completed'),
('Riverside Education Day', 24, 'Riverside Park', 'Educational', '2025-08-23', '13:00', '16:00', 3.0, 'Learning about river ecosystems', 'Educational materials', 'Family friendly event', 'completed'),
('City Park Tree Planting', 25, 'Central Park', 'Tree Planting', '2025-09-06', '09:30', '13:30', 4.0, 'Planting new trees in the park', 'Trees, tools, mulch', 'Sturdy boots required', 'completed'),
('Green Valley Bird Habitat', 21, 'Valley Reserve', 'Habitat Restoration', '2025-09-20', '10:00', '13:00', 3.0, 'Creating bird habitats', 'Nest boxes, tools', 'Quiet event', 'completed'),
('Lake Shore Cleanup', 22, 'Lakeview South', 'Lake Cleanup', '2025-10-04', '14:00', '16:30', 2.5, 'Cleaning the southern shoreline', 'Bags, gloves', 'Sun protection recommended', 'completed'),
('Beach Dune Restoration', 23, 'North Beach Dunes', 'Dune Restoration', '2025-10-18', '09:00', '13:00', 4.0, 'Restoring sand dunes with native plants', 'Plants, sand, tools', 'Bring water and sunscreen', 'completed'),
('Riverside Water Quality', 24, 'Riverside Bridge', 'Water Testing', '2025-11-01', '13:00', '15:00', 2.0, 'Testing river water quality', 'Testing kits, gloves', 'Water contact possible', 'completed'),
('Park Waste Audit', 25, 'City Park Depot', 'Waste Audit', '2025-11-15', '10:00', '13:00', 3.0, 'Sorting and auditing collected waste', 'Sorting equipment', 'Gloves required', 'completed'),
('Valley Pest Control', 21, 'Green Valley', 'Pest Control', '2025-11-29', '08:30', '13:30', 5.0, 'Controlling pest animals', 'Traps, bait, gloves', 'Training provided', 'completed'),
('Lake Native Planting', 22, 'Lakeview North', 'Tree Planting', '2025-12-06', '09:30', '13:00', 3.5, 'Planting native plants around the lake', 'Native plants, tools', 'Waterfront planting', 'completed');

-- UPCOMING EVENTS (2026) - All should be 'upcoming'
INSERT INTO events (event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions, status) VALUES
('North Beach Spring Clean 2026', 21, 'North Beach Main Access', 'Beach Cleanup', '2026-04-15', '09:00', '12:00', 3.0, 'Annual spring cleanup of North Beach', 'Gloves, bags, litter pickers', 'Wear sunscreen, closed shoes, bring water', 'upcoming'),
('Riverside Litter Collection', 22, 'Riverside Park', 'River Cleanup', '2026-04-16', '10:00', '12:30', 2.5, 'Cleaning up the riverbank area', 'Bags and gloves available', 'Stay away from water edge, wear sturdy boots', 'upcoming'),
('City Park Beautification', 22, 'Central Park', 'Park Cleanup', '2026-04-17', '13:00', '16:00', 3.0, 'Spring cleanup of Central Park', 'Tools provided, bring own gloves', 'Watch for uneven ground, bring hat', 'upcoming'),
('Green Valley Weed Control', 23, 'Valley Trail Head', 'Weed Control', '2026-04-18', '09:30', '13:30', 4.0, 'Removing invasive weeds from native bush', 'Tools and gloves provided', 'Long pants recommended, check for ticks', 'upcoming'),
('Lakeview Cleanup', 23, 'Lakeview Boat Ramp', 'Lake Cleanup', '2026-04-19', '14:00', '16:00', 2.0, 'Cleaning up around the lake shore', 'Bags, gloves, grabbers', 'Life jackets available if needed', 'upcoming'),
('Beach Microplastics Survey', 24, 'North Beach South End', 'Beach Cleanup', '2026-04-20', '10:00', '13:00', 3.0, 'Collecting microplastics for research', 'Sieves, containers, gloves', 'Bring sun protection', 'upcoming'),
('Riverside Planting Day', 24, 'Riverside Reserve', 'Tree Planting', '2026-04-21', '09:00', '13:00', 4.0, 'Planting native trees along the river', 'Plants, tools, mulch', 'Wear gardening gloves', 'upcoming'),
('Park Litter Blitz', 25, 'City Park East', 'Park Cleanup', '2026-04-22', '13:30', '16:00', 2.5, 'Earth Day cleanup event', 'All equipment provided', 'Bring water and sunscreen', 'upcoming'),
('Valley Trail Maintenance', 21, 'Green Valley Trail', 'Trail Maintenance', '2026-04-23', '09:00', '12:30', 3.5, 'Clearing and maintaining walking trails', 'Tools, gloves, safety vests', 'Stay on marked trails', 'upcoming'),
('Lake Weed Collection', 22, 'Lakeview East', 'Lake Cleanup', '2026-04-24', '10:30', '13:30', 3.0, 'Removing invasive aquatic weeds', 'Nets, bags, gloves', 'Waterproof boots recommended', 'upcoming'),
('North Beach Evening Cleanup', 23, 'North Beach Main Access', 'Beach Cleanup', '2026-04-25', '17:00', '19:00', 2.0, 'Evening cleanup session', 'Gloves, bags, torches', 'Bring torch, wear reflective gear', 'upcoming'),
('Riverside Education Day', 24, 'Riverside Park', 'Educational', '2026-04-26', '13:00', '16:00', 3.0, 'Learning about river ecosystems', 'Educational materials', 'Family friendly event', 'upcoming'),
('City Park Tree Planting', 25, 'Central Park', 'Tree Planting', '2026-04-27', '09:30', '13:30', 4.0, 'Planting new trees in the park', 'Trees, tools, mulch', 'Sturdy boots required', 'upcoming'),
('Green Valley Bird Habitat', 21, 'Valley Reserve', 'Habitat Restoration', '2026-04-28', '10:00', '13:00', 3.0, 'Creating bird habitats', 'Nest boxes, tools', 'Quiet event', 'upcoming'),
('Lake Shore Cleanup', 22, 'Lakeview South', 'Lake Cleanup', '2026-04-29', '14:00', '16:30', 2.5, 'Cleaning the southern shoreline', 'Bags, gloves', 'Sun protection recommended', 'upcoming'),
('Beach Dune Restoration', 23, 'North Beach Dunes', 'Dune Restoration', '2026-04-30', '09:00', '13:00', 4.0, 'Restoring sand dunes with native plants', 'Plants, sand, tools', 'Bring water and sunscreen', 'upcoming'),
('Riverside Water Quality', 24, 'Riverside Bridge', 'Water Testing', '2026-05-01', '13:00', '15:00', 2.0, 'Testing river water quality', 'Testing kits, gloves', 'Water contact possible', 'upcoming'),
('Park Waste Audit', 25, 'City Park Depot', 'Waste Audit', '2026-05-02', '10:00', '13:00', 3.0, 'Sorting and auditing collected waste', 'Sorting equipment', 'Gloves required', 'upcoming'),
('Valley Pest Control', 21, 'Green Valley', 'Pest Control', '2026-05-03', '08:30', '13:30', 5.0, 'Controlling pest animals', 'Traps, bait, gloves', 'Training provided', 'upcoming'),
('Lake Native Planting', 22, 'Lakeview North', 'Tree Planting', '2026-05-04', '09:30', '13:00', 3.5, 'Planting native plants around the lake', 'Native plants, tools', 'Waterfront planting', 'upcoming');

-- Add a few cancelled events for testing
INSERT INTO events (event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions, status) VALUES
('City Park Cleanup (Cancelled)', 22, 'Central Park', 'Park Cleanup', '2025-11-20', '10:00', '13:00', 3.0, 'This event was cancelled due to weather', 'Gloves, bags', 'Stay on paths', 'cancelled'),
('Beach Cleanup (Cancelled)', 21, 'North Beach', 'Beach Cleanup', '2026-01-15', '09:00', '12:00', 3.0, 'Cancelled due to storm warning', 'All equipment', 'Check weather', 'cancelled');

-- Insert event registrations (for both past and upcoming events)
-- PAST EVENT REGISTRATIONS (with attendance data)
INSERT INTO event_registrations (event_id, volunteer_id, attendance, registration_date) VALUES
-- Event 1 (North Beach Spring Clean 2025)
(1, 1, 'attended', '2025-03-01 10:23:00'),
(1, 2, 'attended', '2025-03-02 14:15:00'),
(1, 3, 'attended', '2025-03-03 09:45:00'),
(1, 4, 'attended', '2025-03-05 11:30:00'),
(1, 5, 'attended', '2025-03-06 16:20:00'),
-- Event 2 (Riverside Litter Collection)
(2, 6, 'attended', '2025-03-10 08:50:00'),
(2, 7, 'attended', '2025-03-12 13:40:00'),
(2, 8, 'attended', '2025-03-15 10:15:00'),
(2, 9, 'absent', '2025-03-14 09:30:00'),
-- Event 3 (City Park Beautification)
(3, 10, 'attended', '2025-03-25 14:20:00'),
(3, 11, 'attended', '2025-03-28 11:10:00'),
(3, 12, 'attended', '2025-03-30 15:45:00'),
-- Event 4 (Green Valley Weed Control)
(4, 13, 'attended', '2025-04-01 09:15:00'),
(4, 14, 'attended', '2025-04-02 10:30:00'),
(4, 15, 'attended', '2025-04-03 08:20:00'),
-- Event 5 (Lakeview Cleanup)
(5, 16, 'attended', '2025-04-20 16:40:00'),
(5, 17, 'attended', '2025-04-22 12:15:00'),
(5, 18, 'attended', '2025-04-25 09:50:00'),
-- More registrations for other past events
(6, 1, 'attended', '2025-05-05 10:00:00'),
(6, 2, 'attended', '2025-05-06 11:30:00'),
(6, 3, 'attended', '2025-05-08 14:15:00'),
(7, 4, 'attended', '2025-05-25 09:45:00'),
(7, 5, 'attended', '2025-05-28 13:20:00'),
(8, 6, 'attended', '2025-06-10 10:30:00'),
(8, 7, 'attended', '2025-06-12 15:40:00'),
(9, 8, 'attended', '2025-06-20 08:15:00'),
(9, 9, 'attended', '2025-06-22 11:50:00'),
(10, 10, 'attended', '2025-07-05 14:30:00'),
(10, 11, 'attended', '2025-07-08 09:10:00');

-- UPCOMING EVENT REGISTRATIONS (registered but not yet attended)
INSERT INTO event_registrations (event_id, volunteer_id, attendance, registration_date) VALUES
-- Event 21 (North Beach Spring Clean 2026)
(21, 1, 'registered', '2026-03-01 10:30:00'),
(21, 2, 'registered', '2026-03-02 14:20:00'),
(21, 3, 'registered', '2026-03-03 09:15:00'),
(21, 4, 'registered', '2026-03-05 11:45:00'),
-- Event 22 (Riverside Litter Collection)
(22, 5, 'registered', '2026-03-10 08:30:00'),
(22, 6, 'registered', '2026-03-12 13:50:00'),
(22, 7, 'registered', '2026-03-14 10:25:00'),
-- Event 23 (City Park Beautification)
(23, 8, 'registered', '2026-03-20 15:30:00'),
(23, 9, 'registered', '2026-03-22 11:10:00'),
-- Event 24 (Green Valley Weed Control)
(24, 10, 'registered', '2026-03-25 09:45:00'),
(24, 11, 'registered', '2026-03-28 14:15:00'),
-- Event 25 (Lakeview Cleanup)
(25, 12, 'registered', '2026-04-01 16:20:00'),
(25, 13, 'registered', '2026-04-02 10:40:00'),
(25, 14, 'registered', '2026-04-03 08:50:00');

-- Insert event outcomes for past events
INSERT INTO event_outcomes (event_id, number_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by, recorded_at) VALUES
(1, 5, 24, 12, 'Removed 2 shopping carts from beach', 21, '2025-03-15 14:30:00'),
(2, 3, 15, 8, 'Found and removed 3 tyres from river', 22, '2025-03-20 15:15:00'),
(3, 3, 12, 6, 'Cleared 4 overgrown garden beds', 22, '2025-04-05 17:30:00'),
(4, 3, 8, 0, 'Removed extensive gorse infestation', 23, '2025-04-12 15:45:00'),
(5, 3, 10, 4, 'Cleaned 500m of shoreline', 23, '2025-05-02 17:00:00'),
(6, 3, 18, 9, 'Collected 500g of microplastics for research', 24, '2025-05-18 15:30:00'),
(7, 2, 0, 0, 'Planted 50 native trees', 24, '2025-06-08 15:45:00'),
(8, 2, 14, 7, 'Earth Day event - great participation', 25, '2025-06-22 17:15:00'),
(9, 2, 5, 0, 'Cleared 2km of walking tracks', 21, '2025-07-05 14:00:00'),
(10, 2, 20, 10, 'Removed large amount of aquatic weeds', 22, '2025-07-19 16:30:00');

-- Insert feedback for past events
INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at) VALUES
(1, 1, 5, 'Great event, well organized! Found lots of litter to clean up. The beach looks much better now.', '2025-03-16 09:23:00'),
(1, 2, 4, 'Good turnout, supplies were adequate. Would suggest more bags next time.', '2025-03-16 10:45:00'),
(1, 3, 5, 'Excellent organization and safety briefing. Will definitely join again!', '2025-03-16 11:30:00'),
(2, 6, 5, 'Beautiful location, felt great to help clean it up. The river area is much cleaner now.', '2025-03-21 08:15:00'),
(2, 7, 4, 'Productive morning, good team coordination.', '2025-03-21 09:30:00'),
(3, 10, 5, 'The park looks so much better now! Great team effort.', '2025-04-06 10:20:00'),
(4, 13, 4, 'Hard work but rewarding, good safety briefing.', '2025-04-13 14:45:00'),
(5, 16, 5, 'Beautiful lake area, collected lots of rubbish. Very satisfying!', '2025-05-03 11:10:00'),
(6, 1, 5, 'Interesting microplastics survey, learned a lot about marine pollution.', '2025-05-19 16:30:00'),
(7, 4, 5, 'Great planting day, the area looks transformed!', '2025-06-09 15:45:00'),
(8, 6, 4, 'Good event for Earth Day, well organized.', '2025-06-23 09:20:00');

-- Insert notifications for upcoming events
INSERT INTO notifications (user_id, event_id, message, notification_type, created_at) VALUES
(1, 21, 'Reminder: North Beach Spring Clean 2026 is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder', '2026-04-14 08:00:00'),
(2, 21, 'Reminder: North Beach Spring Clean 2026 is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder', '2026-04-14 08:00:00'),
(3, 21, 'Reminder: North Beach Spring Clean 2026 is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder', '2026-04-14 08:00:00'),
(4, 21, 'Reminder: North Beach Spring Clean 2026 is tomorrow at 9:00 AM. Please bring water and sun protection.', 'reminder', '2026-04-14 08:00:00'),
(5, 22, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder', '2026-04-15 09:00:00'),
(6, 22, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder', '2026-04-15 09:00:00'),
(7, 22, 'Reminder: Riverside Litter Collection is tomorrow at 10:00 AM. Wear sturdy boots.', 'reminder', '2026-04-15 09:00:00'),
(8, 23, 'Reminder: City Park Beautification is tomorrow at 1:00 PM. Bring hat and gloves.', 'reminder', '2026-04-16 10:00:00'),
(9, 23, 'Reminder: City Park Beautification is tomorrow at 1:00 PM. Bring hat and gloves.', 'reminder', '2026-04-16 10:00:00');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Show counts to verify data
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Events', COUNT(*) FROM events
UNION ALL
SELECT 'Event Registrations', COUNT(*) FROM event_registrations
UNION ALL
SELECT 'Event Outcomes', COUNT(*) FROM event_outcomes
UNION ALL
SELECT 'Feedback', COUNT(*) FROM feedback
UNION ALL
SELECT 'Notifications', COUNT(*) FROM notifications;

-- Show role distribution
SELECT role, COUNT(*) FROM users GROUP BY role;

-- Show event statistics
SELECT 
    CASE 
        WHEN event_date < CURRENT_DATE THEN 'Past Events'
        ELSE 'Upcoming Events'
    END as event_status,
    COUNT(*) as count
FROM events
GROUP BY event_status;
