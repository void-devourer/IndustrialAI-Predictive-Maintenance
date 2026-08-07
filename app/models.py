from app.database import get_connection


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            request_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            machine_type TEXT NOT NULL,

            air_temp REAL,
            process_temp REAL,
            rotational_speed REAL,
            torque REAL,
            tool_wear REAL,

            power REAL,
            temp_difference REAL,
            wear_progression REAL,

            prediction TEXT,
            probability REAL,
            risk_level TEXT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()