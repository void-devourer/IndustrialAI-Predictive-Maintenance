import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        "postgresql://industrial:industrial_password"
        "@localhost:5432/predictive_maintenance"
    )


def get_connection():
    return psycopg2.connect(DATABASE_URL)