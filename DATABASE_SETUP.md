# Database Setup Guide

## Common Issue: Migration Errors

If you encounter errors like `no such column: core_taughtcourse.section`, it means your database schema is out of sync with the code.

### Solution

Run the following commands to update your database:

```bash
python manage.py migrate
```

### Starting Fresh

If you need to start with a fresh database:

```bash
# Delete the existing database (SQLite)
rm db.sqlite3

# Run migrations to create the database with the latest schema
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

### Verifying Migrations

To check which migrations have been applied:

```bash
python manage.py showmigrations
```

All migrations should show `[X]` if they've been applied successfully.

## Important Note

Always run `python manage.py migrate` after pulling new code changes that include model updates.
