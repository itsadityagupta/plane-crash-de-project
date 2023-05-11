import re

import config
import numpy as np


def validate_missing(value):
    """
    Returns the value if its not '?', else returns NAN.
    :param value: given value
    :return: validated value
    """
    if value.strip() != "?":
        return value.strip()
    else:
        return np.nan


def get_count_details(value):
    """
    Extracts the total, passenger and the crew count from the given column value.
    :param value: column value
    :return: count of total, passengers and crew
    """
    if value.strip() == "?":
        return None

    total_match = re.search(config.total_format, value)
    passenger_match = re.search(config.passenger_format, value)
    crew_match = re.search(config.crew_format, value)

    total_passengers = int(total_match.group(1)) if total_match else np.nan
    passengers = int(passenger_match.group(1)) if passenger_match else np.nan
    crew = int(crew_match.group(1)) if crew_match else np.nan

    return [total_passengers, passengers, crew]
