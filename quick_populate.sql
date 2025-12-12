-- ====================================================================
-- QUICK COPY-PASTE SQL COMMANDS
-- For PostgreSQL database: school_db
-- ====================================================================

-- STEP 1: DELETE ALL DATA
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
DELETE FROM auth_user;

-- STEP 2: RESET SEQUENCES
ALTER SEQUENCE core_student_student_id_seq RESTART WITH 1;
ALTER SEQUENCE core_teacher_teacher_id_seq RESTART WITH 1;
ALTER SEQUENCE core_course_course_id_seq RESTART WITH 1;
ALTER SEQUENCE core_management_management_id_seq RESTART WITH 1;
ALTER SEQUENCE core_taughtcourse_id_seq RESTART WITH 1;
ALTER SEQUENCE core_studentcourse_id_seq RESTART WITH 1;
ALTER SEQUENCE core_class_classroom_id_seq RESTART WITH 1;
ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;

-- STEP 3: INSERT USERS (Students, Teachers, Management)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'student1', 'Ahmed', 'Khan', 'ahmed.khan@university.edu', FALSE, TRUE, NOW()),
(2, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'student2', 'Fatima', 'Ali', 'fatima.ali@university.edu', FALSE, TRUE, NOW()),
(3, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'student3', 'Hassan', 'Malik', 'hassan.malik@university.edu', FALSE, TRUE, NOW()),
(4, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'student4', 'Ayesha', 'Raza', 'ayesha.raza@university.edu', FALSE, TRUE, NOW()),
(5, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'student5', 'Usman', 'Sheikh', 'usman.sheikh@university.edu', FALSE, TRUE, NOW()),
(6, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher1', 'Dr. Sarah', 'Ahmed', 'sarah.ahmed@university.edu', TRUE, TRUE, NOW()),
(7, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher2', 'Prof. Muhammad', 'Hussain', 'muhammad.hussain@university.edu', TRUE, TRUE, NOW()),
(8, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher3', 'Dr. Zainab', 'Farooq', 'zainab.farooq@university.edu', TRUE, TRUE, NOW()),
(9, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher4', 'Prof. Ali', 'Haider', 'ali.haider@university.edu', TRUE, TRUE, NOW()),
(10, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher5', 'Dr. Mariam', 'Nasir', 'mariam.nasir@university.edu', TRUE, TRUE, NOW()),
(11, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, FALSE, 'teacher6', 'Prof. Imran', 'Siddiqui', 'imran.siddiqui@university.edu', TRUE, TRUE, NOW()),
(12, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, TRUE, 'management1', 'Dean', 'Rashid', 'dean.rashid@university.edu', TRUE, TRUE, NOW()),
(13, 'pbkdf2_sha256$870000$1234567890abcdefghijklmnop$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH=', NULL, TRUE, 'management2', 'HOD', 'Kamran', 'hod.kamran@university.edu', TRUE, TRUE, NOW());

ALTER SEQUENCE auth_user_id_seq RESTART WITH 14;

-- STEP 4: INSERT COURSES
INSERT INTO core_course (course_id, course_name) VALUES
(1, 'Database Systems'),
(2, 'Data Structures and Algorithms'),
(3, 'Operating Systems'),
(4, 'Computer Networks'),
(5, 'Software Engineering'),
(6, 'Artificial Intelligence'),
(7, 'Web Development'),
(8, 'Mobile Application Development');

-- STEP 5: INSERT STUDENTS
INSERT INTO core_student (student_id, user_id, student_name, email, rfid, overall_attendance, year, dept, section) VALUES
(1, 1, 'Ahmed Khan', 'ahmed.khan@university.edu', 'RFID-STD-001', 85.5, 3, 'CS', 'A'),
(2, 2, 'Fatima Ali', 'fatima.ali@university.edu', 'RFID-STD-002', 92.3, 3, 'CS', 'A'),
(3, 3, 'Hassan Malik', 'hassan.malik@university.edu', 'RFID-STD-003', 78.9, 3, 'CS', 'B'),
(4, 4, 'Ayesha Raza', 'ayesha.raza@university.edu', 'RFID-STD-004', 88.7, 2, 'IT', 'A'),
(5, 5, 'Usman Sheikh', 'usman.sheikh@university.edu', 'RFID-STD-005', 81.2, 3, 'CS', 'A');

-- STEP 6: INSERT TEACHERS
INSERT INTO core_teacher (teacher_id, user_id, teacher_name, email, rfid) VALUES
(1, 6, 'Dr. Sarah Ahmed', 'sarah.ahmed@university.edu', 'RFID-TCH-001'),
(2, 7, 'Prof. Muhammad Hussain', 'muhammad.hussain@university.edu', 'RFID-TCH-002'),
(3, 8, 'Dr. Zainab Farooq', 'zainab.farooq@university.edu', 'RFID-TCH-003'),
(4, 9, 'Prof. Ali Haider', 'ali.haider@university.edu', 'RFID-TCH-004'),
(5, 10, 'Dr. Mariam Nasir', 'mariam.nasir@university.edu', 'RFID-TCH-005'),
(6, 11, 'Prof. Imran Siddiqui', 'imran.siddiqui@university.edu', 'RFID-TCH-006');

-- STEP 7: INSERT MANAGEMENT
INSERT INTO core_management (management_id, user_id, management_name, email) VALUES
(1, 12, 'Dean Rashid', 'dean.rashid@university.edu'),
(2, 13, 'HOD Kamran', 'hod.kamran@university.edu');

-- STEP 8: INSERT TAUGHT COURSES (Teacher-Course assignments)
INSERT INTO core_taughtcourse (id, course_id, teacher_id, classes_taken, section, year) VALUES
(1, 1, 1, '', 'A', 3),
(2, 5, 1, '', 'B', 3),
(3, 2, 2, '', 'A', 3),
(4, 2, 2, '', 'B', 3),
(5, 3, 3, '', 'A', 3),
(6, 4, 3, '', 'A', 2),
(7, 6, 4, '', 'A', 3),
(8, 7, 5, '', 'A', 2),
(9, 8, 6, '', 'A', 3);

-- STEP 9: INSERT STUDENT COURSES (Enrollments)
INSERT INTO core_studentcourse (id, student_id, course_id, teacher_id, classes_attended) VALUES
(1, 1, 1, 1, ''),
(2, 1, 2, 2, ''),
(3, 1, 3, 3, ''),
(4, 1, 6, 4, ''),
(5, 2, 1, 1, ''),
(6, 2, 2, 2, ''),
(7, 2, 6, 4, ''),
(8, 2, 8, 6, ''),
(9, 3, 2, 2, ''),
(10, 3, 5, 1, ''),
(11, 3, 8, 6, ''),
(12, 4, 4, 3, ''),
(13, 4, 7, 5, ''),
(14, 5, 1, 1, ''),
(15, 5, 2, 2, ''),
(16, 5, 3, 3, ''),
(17, 5, 6, 4, '');

-- VERIFICATION: Check the counts
SELECT COUNT(*) as student_count FROM core_student;
SELECT COUNT(*) as teacher_count FROM core_teacher;
SELECT COUNT(*) as course_count FROM core_course;
SELECT COUNT(*) as management_count FROM core_management;
SELECT COUNT(*) as taught_count FROM core_taughtcourse;
SELECT COUNT(*) as enrolled_count FROM core_studentcourse;
