from project_database.db import init_db

if __name__ == "__main__":
    try:
        init_db()
        print("Database tables are ready.")
    except Exception as e:
        print(f"Failed to prepare database tables: {e}")
        raise
