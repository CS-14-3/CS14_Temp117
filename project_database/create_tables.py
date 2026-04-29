from project_database.db import ensure_database_exists, init_db

if __name__ == "__main__":
    try:
        ensure_database_exists()
        init_db()
        print("Database and tables are ready.")
    except Exception as e:
        print(f"Failed to prepare database: {e}")
        raise