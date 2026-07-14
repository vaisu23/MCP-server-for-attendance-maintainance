import os
from pathlib import Path

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

from app.db.connection import get_connection


# Load .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def initialize_database():
    db_name = os.getenv("DB_NAME")

    # Connect to the default postgres database
    conn = psycopg2.connect(
        dbname=db_name,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the target database exists
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s;",
        (db_name,),
    )

    exists = cursor.fetchone()

    if not exists:
        print(f"Creating database '{db_name}'...")

        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(db_name)
            )
        )

        print("Database created.")

    else:
        print(f"Database '{db_name}' already exists.")

    cursor.close()
    conn.close()

    # Connect to the target database
    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the users table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'users'
        );
    """)

    tables_exist = cursor.fetchone()[0]

    if not tables_exist:
        print("Running schema.sql...")

        schema_path = (
            Path(__file__).resolve().parent.parent / "schema.sql"
        )

        with open(schema_path, "r", encoding="utf-16") as f:
            cursor.execute(f.read())

        conn.commit()

        print("Schema initialized.")

    else:
        print("Schema already exists.")

    cursor.close()
    conn.close()