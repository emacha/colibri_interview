"""Convert the mock data into a SQLite database."""
import datetime
import json
import sqlite3

from loguru import logger

import src
from src.database import Column


def get_age(date_of_birth):
    """Calculate the age from the date of birth and a reference today date."""
    # Need this to be reproducible
    today = "2023-11-16"
    age_days = datetime.datetime.strptime(
        today, "%Y-%m-%d"
    ) - datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")
    return int(age_days.days / 365.25)


columns = [col.value for col in Column]
CREATE_TABLE = f"CREATE TABLE persons({','.join(columns)}, PRIMARY KEY (id))"
VALUES = ", ".join(f":{col}" for col in columns)
INSERT_INTO = f"INSERT INTO persons VALUES ({VALUES})"

config = src.config.get_config()

logger.info("Reading mock data")
data = json.loads(config.MOCK_PATH.read_text())
data = [row | {"age": get_age(row["date_of_birth"])} for row in data]


logger.info("Creating new DB with MOCK_DATA contents")
config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
if config.DB_PATH.exists():
    logger.warning(f"Overwriting {config.DB_PATH}")
    config.DB_PATH.unlink()

with sqlite3.connect(config.DB_PATH) as connection:
    cursor = connection.cursor()
    logger.info("Creating table")
    logger.debug(CREATE_TABLE)
    cursor.execute(CREATE_TABLE)

    logger.info("Inserting data")
    logger.debug(INSERT_INTO)
    cursor.executemany(INSERT_INTO, data)

    cursor.execute("select count(*) from persons")
    logger.info(f"Inserted {cursor.fetchone()[0]} rows")

logger.info("Done")
