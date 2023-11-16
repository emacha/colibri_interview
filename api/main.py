"""The main module for the API."""
import sqlite3

from fastapi import FastAPI, HTTPException
from loguru import logger

import src
from src.database import Column

app = FastAPI()
config = src.config.get_config()


@app.get("/")
async def root():
    """Return a message to show that the API is working."""
    return {"message": "I'm working!"}


def get_persons(
    sort_by: Column | None = None,
    page_size: int = 1000,
    offset: int = 0,
    filters: dict[str, str] = {},
    ascending: bool = True,
) -> dict[str, list[tuple]]:
    """Return all persons."""
    with sqlite3.connect(config.DB_PATH) as connection:
        return {
            "persons": src.database.select_all(
                connection, sort_by, page_size, offset, filters, ascending
            )
        }


get_persons_get = app.get("/v1/persons")(get_persons)
# We need post to be able to send a body for the filters
get_persons_post = app.post("/v1/persons")(get_persons)


@app.get("/v1/persons/{id}")
def get_person(id: int) -> dict[str, tuple | None]:
    """Return a single person."""
    with sqlite3.connect(config.DB_PATH) as connection:
        return {"person": src.database.select_one(connection, id)}


@app.patch("/v1/persons/{id}")
def update_person(id: int, values: dict) -> dict:
    """Update a single person."""
    with sqlite3.connect(config.DB_PATH) as connection:
        try:
            src.database.update_one(connection, id, values)
        except Exception as exc:
            logger.exception(exc)
            raise HTTPException(status_code=500, detail="Failed to update") from exc
        else:
            return {"message": "Success"}


@app.delete("/v1/persons/{id}")
def delete_person(id: int) -> dict:
    """Delete a single person."""
    with sqlite3.connect(config.DB_PATH) as connection:
        try:
            src.database.delete_one(connection, id)
        except Exception as exc:
            logger.exception(exc)
            raise HTTPException(status_code=500, detail="Failed to delete") from exc
        else:
            return {"message": "Success"}


@app.get("/v1/average")
def get_average(column: Column, per: Column | None = None) -> dict:
    """Return the average of a column grouped by `per`."""
    with sqlite3.connect(config.DB_PATH) as connection:
        return {"average": src.database.get_average(connection, column, per)}
