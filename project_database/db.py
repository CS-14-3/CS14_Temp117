import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
from sqlalchemy.orm import declarative_base, sessionmaker

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "capstone5703")
DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")
MAINTENANCE_DB = "postgres"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"
)

MAINTENANCE_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{MAINTENANCE_DB}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

Base = declarative_base()


def ensure_database_exists():
    maintenance_engine = create_engine(
        MAINTENANCE_DATABASE_URL,
        isolation_level="AUTOCOMMIT",
        future=True,
    )

    with maintenance_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": DB_NAME},
        ).scalar()

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))

    maintenance_engine.dispose()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import project_database.database_structure.auth_models
    import project_database.database_structure.survey_models
    import project_database.database_structure.participant_models
    import project_database.database_structure.gaze_models

    Base.metadata.create_all(bind=engine)


def drop_db():
    import project_database.database_structure.auth_models
    import project_database.database_structure.survey_models
    import project_database.database_structure.participant_models
    import project_database.database_structure.gaze_models

    Base.metadata.drop_all(bind=engine)
