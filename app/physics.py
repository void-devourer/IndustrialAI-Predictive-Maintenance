import numpy as np


def calculate_physics_features(
    air_temp,
    process_temp,
    rotational_speed,
    torque,
    tool_wear
):
    power = torque * rotational_speed * (np.pi / 30)

    temp_difference = process_temp - air_temp

    wear_progression = tool_wear * torque

    return {
        "power": power,
        "temp_difference": temp_difference,
        "wear_progression": wear_progression
    }