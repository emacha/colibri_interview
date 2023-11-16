"""Handle database operations."""
import sqlite3
from enum import Enum

import src

config = src.config.get_config()


class Column(str, Enum):
    """Enum for the columns in the database."""

    id = "id"
    first_name = "first_name"
    last_name = "last_name"
    email = "email"
    gender = "gender"
    date_of_birth = "date_of_birth"
    industry = "industry"
    salary = "salary"
    years_of_experience = "years_of_experience"
    age = "age"


def dict_to_prepared_statement(d: dict) -> str:
    """Format a string into the prepared statement format."""
    return (f"{key} = :{key}" for key in d.keys())


def select_all(
    connection: sqlite3.Connection,
    sort_by: Column | None = None,
    page_size: int = 1000,
    offset: int = 0,
    filters: dict = {},
    ascending: bool = True,
) -> list[tuple]:
    """Return all persons."""
    cursor = connection.cursor()
    query = "SELECT * FROM persons"
    where = ""
    if filters:
        where = " WHERE " + " AND ".join(dict_to_prepared_statement(filters))
    order_by = ""
    if sort_by is not None:
        order_by = f" ORDER BY {sort_by.value} {'ASC' if ascending else 'DESC'}"

    query += where + order_by + " LIMIT :page_size OFFSET :offset"

    values = {
        "page_size": page_size,
        "offset": offset,
    } | filters

    cursor.execute(query, values)
    results = cursor.fetchall()
    return results


def select_one(connection: sqlite3.Connection, id: int) -> tuple | None:
    """Return a single person."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM persons where id = :id", {"id": id})
    person = cursor.fetchone()
    return person


def update_one(connection: sqlite3.Connection, id: int, values: dict) -> None:
    """Update a single person."""
    set_vals = ", ".join(dict_to_prepared_statement(values))
    update_query = f"UPDATE persons SET {set_vals} WHERE id = :id"
    cursor = connection.cursor()
    cursor.execute(update_query, values | {"id": id})


def delete_one(connection: sqlite3.Connection, id: int) -> None:
    """Delete a single person."""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM persons where id = :id", {"id": id})


def get_average(
    connection: sqlite3.Connection, column: Column, per: Column | None = None
) -> [float]:
    """Return the average of a column grouped by `per`."""
    cursor = connection.cursor()
    if per is not None:
        query = (
            f"SELECT {per.value}, AVG({column.value}) FROM persons GROUP BY {per.value}"
        )
    else:
        query = f"SELECT AVG({column.value}) FROM persons"
    cursor.execute(query)
    results = cursor.fetchall()
    return results
