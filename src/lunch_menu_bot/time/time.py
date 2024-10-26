from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Day(Enum):
    MONDAY = "Mandag"
    TUESDAY = "Tirsdag"
    WEDNESDAY = "Onsdag"
    THURSDAY = "Torsdag"
    FRIDAY = "Fredag"
    SATURDAY = "Lørdag"
    SUNDAY = "Søndag"


def get_week_and_day():
    # Get current week number
    week_number = datetime.now().isocalendar()[1]
    # Get the current day of the week
    day_of_week = datetime.now().weekday()
    day = Day(list(Day)[day_of_week])

    logging.debug(f"Current week number: {week_number}")
    logging.debug(f"Current day: {day}")

    return week_number, day
