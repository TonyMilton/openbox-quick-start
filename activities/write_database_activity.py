import os
from sqlalchemy import create_engine, text
from temporalio import activity

@activity.defn
async def write_database_activity(weather_data: dict) -> dict:
    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url)

    try:
        with engine.connect() as conn:
            stmt = text(
                """
                INSERT INTO weather (location, temperature, humidity, description, weather_status, timestamp)
                VALUES (:location, :temperature, :humidity, :description, :weather_status, :timestamp)
                """
            )
            result = conn.execute(
                stmt,
                {
                    "location": weather_data["location"],
                    "temperature": weather_data["temperature"],
                    "humidity": weather_data["humidity"],
                    "description": weather_data["description"],
                    "weather_status": weather_data["description"],
                    "timestamp": weather_data["timestamp"]
                }
            )
            conn.commit()

            return {
                "status": "success",
                "rows_inserted": result.rowcount,
                "location": weather_data["location"]
            }
    finally:
        engine.dispose()