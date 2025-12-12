# 🗄️ Database Population Scripts - Quick Start

This repository now includes ready-to-use PostgreSQL commands to populate your database with sample data.

## 📁 Files Created

1. **`quick_populate.sql`** - Compact, copy-paste ready SQL commands
2. **`populate_database.sql`** - Detailed SQL with extensive comments and documentation
3. **`DATABASE_POPULATION_GUIDE.md`** - Complete guide with instructions and data summary

## 🚀 Quick Start (Choose One Method)

### Method 1: Execute SQL File Directly
```bash
psql -h localhost -p 5433 -U dbuser -d school_db -f quick_populate.sql
```

### Method 2: Connect and Paste
```bash
# Connect to database
psql -h localhost -p 5433 -U dbuser -d school_db

# Then copy-paste commands from quick_populate.sql
```

### Method 3: One-Line Command
```bash
psql -h localhost -p 5433 -U dbuser -d school_db < quick_populate.sql
```

## 📊 What Gets Created

| Entity | Count | Details |
|--------|-------|---------|
| **Students** | 5 | Ahmed, Fatima, Hassan, Ayesha, Usman |
| **Teachers** | 6 | Dr. Sarah, Prof. Muhammad, Dr. Zainab, Prof. Ali, Dr. Mariam, Prof. Imran |
| **Courses** | 8 | Database, DSA, OS, Networks, SE, AI, Web Dev, Mobile Dev |
| **Management** | 2 | Dean Rashid, HOD Kamran |
| **Enrollments** | 17 | Student-Course-Teacher relationships |
| **Assignments** | 9 | Teacher-Course assignments with sections |

## 🔑 Login Credentials

**All users** have the password: `password123`

### Student Logins
- `student1` through `student5`

### Teacher Logins
- `teacher1` through `teacher6`

### Management Logins
- `management1`, `management2`

## ⚠️ Important Notes

1. **Run migrations first** if this is a fresh database:
   ```bash
   python manage.py migrate
   ```

2. **Data will be cleared**: The script deletes all existing data before inserting new data

3. **Database must exist**: Ensure `school_db` database is created before running

4. **Sequences are reset**: All auto-increment IDs start from 1

## 🔍 Verify Data

After running the script, verify with:
```sql
SELECT COUNT(*) FROM core_student;      -- Should be 5
SELECT COUNT(*) FROM core_teacher;      -- Should be 6
SELECT COUNT(*) FROM core_course;       -- Should be 8
SELECT COUNT(*) FROM core_management;   -- Should be 2
```

## 📖 Full Documentation

For complete details, see: **`DATABASE_POPULATION_GUIDE.md`**

## 🎓 Sample Data Relationships

**Example**: Student "Ahmed Khan" is enrolled in:
- Database Systems (with Dr. Sarah Ahmed)
- Data Structures (with Prof. Muhammad Hussain)
- Operating Systems (with Dr. Zainab Farooq)
- Artificial Intelligence (with Prof. Ali Haider)

**Example**: Teacher "Dr. Sarah Ahmed" teaches:
- Database Systems (Year 3, Section A)
- Software Engineering (Year 3, Section B)

---

**Need help?** Check `DATABASE_POPULATION_GUIDE.md` for troubleshooting and detailed information.
