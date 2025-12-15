-- ====================================================================
-- PostgreSQL Database Population Script
-- Database: school_db
-- This script will:
-- 1. Remove all existing data from tables
-- 2. Insert sample data for Students, Teachers, Courses, Management
-- 3. Create relationships (TaughtCourse, StudentCourse)
-- ====================================================================

-- ====================================================================
-- SECTION 1: DELETE ALL EXISTING DATA
-- Execute these commands in order to clear all tables
-- ====================================================================

-- Delete from tables with foreign key dependencies first
DELETE FROM core_attendancerecord;
DELETE FROM core_attendancesession;
DELETE FROM core_updateattendancerequest;
DELETE FROM core_studentcourse;
DELETE FROM core_taughtcourse;
DELETE FROM core_student;
DELETE FROM core_teacher;
DELETE FROM core_management;
DELETE FROM core_course;
DELETE FROM core_class;

-- Delete from auth_user table (Django's built-in User model)
DELETE FROM auth_user;

-- Reset sequences to start from 1
ALTER SEQUENCE core_student_student_id_seq RESTART WITH 1;
ALTER SEQUENCE core_teacher_teacher_id_seq RESTART WITH 1;
ALTER SEQUENCE core_course_course_id_seq RESTART WITH 1;
ALTER SEQUENCE "core_management_Management_id_seq" RESTART WITH 1;
ALTER SEQUENCE core_taughtcourse_id_seq RESTART WITH 1;
ALTER SEQUENCE core_studentcourse_id_seq RESTART WITH 1;
ALTER SEQUENCE core_class_classroom_id_seq RESTART WITH 1;
ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;

-- ====================================================================
-- SECTION 2: INSERT USER ACCOUNTS
-- Create Django User accounts for authentication
-- Password for all users: "password123" (hashed)
-- ====================================================================

-- Insert Users for Students (5 users)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(1, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'student1', 'Ahmed', 'Khan', 'ahmed.khan@university.edu', FALSE, TRUE, NOW()),
(2, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'student2', 'Fatima', 'Ali', 'fatima.ali@university.edu', FALSE, TRUE, NOW()),
(3, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'student3', 'Hassan', 'Malik', 'hassan.malik@university.edu', FALSE, TRUE, NOW()),
(4, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'student4', 'Ayesha', 'Raza', 'ayesha.raza@university.edu', FALSE, TRUE, NOW()),
(5, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'student5', 'Usman', 'Sheikh', 'usman.sheikh@university.edu', FALSE, TRUE, NOW());

-- Insert Users for Teachers (6 users)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(6, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher1', 'Dr. Sarah', 'Ahmed', 'sarah.ahmed@university.edu', TRUE, TRUE, NOW()),
(7, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher2', 'Prof. Muhammad', 'Hussain', 'muhammad.hussain@university.edu', TRUE, TRUE, NOW()),
(8, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher3', 'Dr. Zainab', 'Farooq', 'zainab.farooq@university.edu', TRUE, TRUE, NOW()),
(9, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher4', 'Prof. Ali', 'Haider', 'ali.haider@university.edu', TRUE, TRUE, NOW()),
(10, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher5', 'Dr. Mariam', 'Nasir', 'mariam.nasir@university.edu', TRUE, TRUE, NOW()),
(11, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, FALSE, 'teacher6', 'Prof. Imran', 'Siddiqui', 'imran.siddiqui@university.edu', TRUE, TRUE, NOW());

-- Insert Users for Management (2 users)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(12, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, TRUE, 'management1', 'Dean', 'Rashid', 'dean.rashid@university.edu', TRUE, TRUE, NOW()),
(13, 'pbkdf2_sha256$1000000$7BRaWqhmQOqohPELg8GhZK$AYmrbt3rCUv4XvLqzxhBB+ZhQUwwVr6Ko4oJwPkCS44=', NULL, TRUE, 'management2', 'HOD', 'Kamran', 'hod.kamran@university.edu', TRUE, TRUE, NOW());

-- Reset the auth_user sequence
ALTER SEQUENCE auth_user_id_seq RESTART WITH 14;

-- ====================================================================
-- SECTION 3: INSERT COURSES
-- Insert 8 courses
-- ====================================================================

INSERT INTO core_course (course_id, course_name)
VALUES
(1, 'Database Systems'),
(2, 'Data Structures and Algorithms'),
(3, 'Operating Systems'),
(4, 'Computer Networks'),
(5, 'Software Engineering'),
(6, 'Artificial Intelligence'),
(7, 'Web Development'),
(8, 'Mobile Application Development');

-- ====================================================================
-- SECTION 4: INSERT STUDENTS
-- Insert 5 students with varying years, departments, and sections
-- ====================================================================

INSERT INTO core_student (student_id, user_id, student_name, email, rfid, overall_attendance, year, dept, section)
VALUES
(1, 1, 'Ahmed Khan', 'ahmed.khan@university.edu', 'RFID-STD-001', 85.5, 3, 'CS', 'A'),
(2, 2, 'Fatima Ali', 'fatima.ali@university.edu', 'RFID-STD-002', 92.3, 3, 'CS', 'A'),
(3, 3, 'Hassan Malik', 'hassan.malik@university.edu', 'RFID-STD-003', 78.9, 3, 'CS', 'B'),
(4, 4, 'Ayesha Raza', 'ayesha.raza@university.edu', 'RFID-STD-004', 88.7, 2, 'IT', 'A'),
(5, 5, 'Usman Sheikh', 'usman.sheikh@university.edu', 'RFID-STD-005', 81.2, 3, 'CS', 'A');

-- ====================================================================
-- SECTION 5: INSERT TEACHERS
-- Insert 6 teachers
-- ====================================================================

INSERT INTO core_teacher (teacher_id, user_id, teacher_name, email, rfid)
VALUES
(1, 6, 'Dr. Sarah Ahmed', 'sarah.ahmed@university.edu', 'RFID-TCH-001'),
(2, 7, 'Prof. Muhammad Hussain', 'muhammad.hussain@university.edu', 'RFID-TCH-002'),
(3, 8, 'Dr. Zainab Farooq', 'zainab.farooq@university.edu', 'RFID-TCH-003'),
(4, 9, 'Prof. Ali Haider', 'ali.haider@university.edu', 'RFID-TCH-004'),
(5, 10, 'Dr. Mariam Nasir', 'mariam.nasir@university.edu', 'RFID-TCH-005'),
(6, 11, 'Prof. Imran Siddiqui', 'imran.siddiqui@university.edu', 'RFID-TCH-006');

-- ====================================================================
-- SECTION 6: INSERT MANAGEMENT
-- Insert 2 management users
-- ====================================================================

INSERT INTO core_management ("Management_id", user_id, "Management_name", email)
VALUES
(1, 12, 'Dean Rashid', 'dean.rashid@university.edu'),
(2, 13, 'HOD Kamran', 'hod.kamran@university.edu');

-- ====================================================================
-- SECTION 7: INSERT TAUGHT COURSES
-- Assign courses to teachers with section and year information
-- ====================================================================

-- Teacher 1 (Dr. Sarah Ahmed) teaches Database Systems and Software Engineering
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(1, 1, 1, '', 'A', 3),
(2, 5, 1, '', 'B', 3);

-- Teacher 2 (Prof. Muhammad Hussain) teaches Data Structures and Algorithms
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(3, 2, 2, '', 'A', 3),
(4, 2, 2, '', 'B', 3);

-- Teacher 3 (Dr. Zainab Farooq) teaches Operating Systems and Computer Networks
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(5, 3, 3, '', 'A', 3),
(6, 4, 3, '', 'A', 2);

-- Teacher 4 (Prof. Ali Haider) teaches Artificial Intelligence
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(7, 6, 4, '', 'A', 3);

-- Teacher 5 (Dr. Mariam Nasir) teaches Web Development
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(8, 7, 5, '', 'A', 2);

-- Teacher 6 (Prof. Imran Siddiqui) teaches Mobile Application Development
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year)
VALUES
(9, 8, 6, '', 'A', 3);

-- ====================================================================
-- SECTION 8: INSERT STUDENT COURSES (ENROLLMENTS)
-- Enroll students in courses taught by teachers
-- ====================================================================

-- Ahmed Khan (Student 1) - Year 3, CS, Section A
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended)
VALUES
(1, 1, 1, 1, ''),  -- Database Systems with Dr. Sarah Ahmed
(2, 1, 2, 2, ''),  -- Data Structures with Prof. Muhammad Hussain
(3, 1, 3, 3, ''),  -- Operating Systems with Dr. Zainab Farooq
(4, 1, 6, 4, '');  -- Artificial Intelligence with Prof. Ali Haider

-- Fatima Ali (Student 2) - Year 3, CS, Section A
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended)
VALUES
(5, 2, 1, 1, ''),  -- Database Systems with Dr. Sarah Ahmed
(6, 2, 2, 2, ''),  -- Data Structures with Prof. Muhammad Hussain
(7, 2, 6, 4, ''),  -- Artificial Intelligence with Prof. Ali Haider
(8, 2, 8, 6, '');  -- Mobile App Development with Prof. Imran Siddiqui

-- Hassan Malik (Student 3) - Year 3, CS, Section B
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended)
VALUES
(9, 3, 2, 2, ''),  -- Data Structures with Prof. Muhammad Hussain (Section B)
(10, 3, 5, 1, ''),  -- Software Engineering with Dr. Sarah Ahmed
(11, 3, 8, 6, '');  -- Mobile App Development with Prof. Imran Siddiqui

-- Ayesha Raza (Student 4) - Year 2, IT, Section A
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended)
VALUES
(12, 4, 4, 3, ''),  -- Computer Networks with Dr. Zainab Farooq
(13, 4, 7, 5, '');  -- Web Development with Dr. Mariam Nasir

-- Usman Sheikh (Student 5) - Year 3, CS, Section A
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended)
VALUES
(14, 5, 1, 1, ''),  -- Database Systems with Dr. Sarah Ahmed
(15, 5, 2, 2, ''),  -- Data Structures with Prof. Muhammad Hussain
(16, 5, 3, 3, ''),  -- Operating Systems with Dr. Zainab Farooq
(17, 5, 6, 4, '');  -- Artificial Intelligence with Prof. Ali Haider

-- ====================================================================
-- VERIFICATION QUERIES
-- Run these to verify data was inserted correctly
-- ====================================================================

-- Check counts
-- SELECT COUNT(*) as student_count FROM core_student;      -- Should be 5
-- SELECT COUNT(*) as teacher_count FROM core_teacher;      -- Should be 6
-- SELECT COUNT(*) as course_count FROM core_course;        -- Should be 8
-- SELECT COUNT(*) as management_count FROM core_management; -- Should be 2
-- SELECT COUNT(*) as taught_count FROM core_taughtcourse;  -- Should be 9
-- SELECT COUNT(*) as enrolled_count FROM core_studentcourse; -- Should be 17

-- View all students with their courses
-- SELECT 
--     s.student_name, 
--     c.course_name, 
--     t.teacher_name,
--     s.year,
--     s.section
-- FROM core_studentcourse sc
-- JOIN core_student s ON sc.student_id = s.student_id
-- JOIN core_course c ON sc.course_id = c.course_id
-- JOIN core_teacher t ON sc.teacher_id = t.teacher_id
-- ORDER BY s.student_name, c.course_name;

-- View all teachers with their courses
-- SELECT 
--     t.teacher_name,
--     c.course_name,
--     tc.section,
--     tc.year
-- FROM core_taughtcourse tc
-- JOIN core_teacher t ON tc.teacher_id = t.teacher_id
-- JOIN core_course c ON tc.course_id = c.course_id
-- ORDER BY t.teacher_name, c.course_name;
