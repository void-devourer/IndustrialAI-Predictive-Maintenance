from app.database import get_connection


def save_prediction(result, data, physics):

    print("========== SAVE PREDICTION CALLED ==========")
    print("AI EXPLANATION:", result.get("ai_explanation"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO predictions (
            request_id,
            timestamp,
            machine_type,
            air_temp,
            process_temp,
            rotational_speed,
            torque,
            tool_wear,
            power,
            temp_difference,
            wear_progression,
            prediction,
            probability,
            risk_level,
            ai_explanation
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """,
        (
            result["request_id"],
            result["timestamp"],
            data.machine_type,
            data.air_temp,
            data.process_temp,
            data.rotational_speed,
            data.torque,
            data.tool_wear,
            physics["power"],
            physics["temp_difference"],
            physics["wear_progression"],
            result["prediction"],
            result["failure_probability"],
            result["risk_level"],
            result.get("ai_explanation", "")
        )
    )

    conn.commit()

    print("========== PREDICTION SAVED ==========")

    cur.close()
    conn.close()


def get_all_predictions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            machine_type,
            prediction,
            probability,
            risk_level,
            ai_explanation
        FROM predictions
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
    {
        "timestamp": row[0],
        "machine_type": row[1],
        "prediction": row[2],
        "probability": row[3],
        "risk_level": row[4],
        "ai_explanation": row[5]
    }
    for row in rows
]