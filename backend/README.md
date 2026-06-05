# NEXUS Intelligence System (NIS) Backend

FastAPI backend for Sakinah matchmaking.

## Database Documentation

This backend uses **PostgreSQL**. **No Firebase or Firestore is used for backend operations.**

### Setup
Ensure you have a running PostgreSQL instance. 
Update your `.env` file with the correct credentials:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/zaryah_nis
```

### Running Migrations
We use Alembic for database migrations.
To run the migrations (once tables are fully defined):
```bash
alembic upgrade head
```

To autogenerate a new migration after modifying models:
```bash
alembic revision --autogenerate -m "migration message"
```

### Running Tests
To run tests safely without a live production database:
```bash
# Ensure you are in the virtual environment
venv\Scripts\activate

# Run pytest
python -m pytest
```
Note: Currently tests use mocking/dummy asserts to ensure CI pipelines run safely without a live connection.
