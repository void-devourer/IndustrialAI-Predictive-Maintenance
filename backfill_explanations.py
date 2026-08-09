from app.database import get_connection
from app.rag import retrieve_knowledge
from app.llm import generate_maintenance_explanation


def backfill_explanations():

    conn = get_connection()
    cur = conn.cursor()

    # Find predictions without an AI explanation
    cur.execute(
        """
        SELECT
            id,
            machine_type,
            air_temp,
            process_temp,
            rotational_speed,
            torque,
            tool_wear,
            prediction,
            probability,
            risk_level
        FROM predictions
        WHERE ai_explanation IS NULL
           OR TRIM(ai_explanation) = ''
        ORDER BY id ASC
        """
    )

    predictions = cur.fetchall()

    print(f"\nFound {len(predictions)} predictions without explanations.\n")

    if not predictions:
        print("Nothing to backfill.")
        cur.close()
        conn.close()
        return

    successful = 0
    failed = 0

    for index, row in enumerate(predictions, start=1):

        (
            prediction_id,
            machine_type,
            air_temp,
            process_temp,
            rotational_speed,
            torque,
            tool_wear,
            prediction,
            probability,
            risk_level,
        ) = row

        print(
            f"[{index}/{len(predictions)}] "
            f"Generating explanation for prediction ID {prediction_id}..."
        )

        try:

            # Same query used by the live prediction endpoint
            query = (
                f"{prediction} "
                f"{risk_level} "
                f"torque "
                f"rotational speed "
                f"tool wear "
                f"temperature"
            )

            # Retrieve maintenance knowledge
            knowledge = retrieve_knowledge(query)

            # Reconstruct machine data
            machine_data = {
                "air_temp": air_temp,
                "process_temp": process_temp,
                "rotational_speed": rotational_speed,
                "torque": torque,
                "tool_wear": tool_wear,
                "machine_type": machine_type,
            }

            # Generate AI explanation
            ai_explanation = generate_maintenance_explanation(
                prediction=prediction,
                probability=probability,
                risk_level=risk_level,
                machine_data=machine_data,
                retrieved_knowledge=knowledge,
            )

            # Update existing database row
            cur.execute(
                """
                UPDATE predictions
                SET ai_explanation = %s
                WHERE id = %s
                """,
                (
                    ai_explanation,
                    prediction_id,
                )
            )

            conn.commit()

            successful += 1

            print(f"    ✓ Updated prediction ID {prediction_id}")

        except Exception as e:

            conn.rollback()

            failed += 1

            print(
                f"    ✗ Failed prediction ID {prediction_id}: {e}"
            )

    cur.close()
    conn.close()

    print("\n========================================")
    print("BACKFILL COMPLETE")
    print("========================================")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Total:      {len(predictions)}")
    print("========================================\n")


if __name__ == "__main__":
    backfill_explanations()