import os
import asyncio
from dotenv import load_dotenv
from temporalio.client import Client
from openbox import create_openbox_worker

load_dotenv()
from workflows.weather import WeatherWorkflow
from activities.fetch_weather_activity import fetch_weather_activity
from activities.write_database_activity import write_database_activity

async def main():
    """
    Set up and run the Temporal worker with OpenBox governance.
    HTTP and database operations are automatically instrumented.
    """
    # Create Temporal client
    temporal_client = await Client.connect("localhost:7233")

    # Create OpenBox-wrapped worker with HTTP and database instrumentation
    worker = create_openbox_worker(
        client=temporal_client,
        task_queue="weather-tasks",
        workflows=[WeatherWorkflow],
        activities=[fetch_weather_activity, write_database_activity],
        openbox_api_key=os.getenv("OPENBOX_API_KEY"),
        openbox_url=os.getenv("OPENBOX_URL"),
        governance_timeout=30.0,
        governance_policy="fail_open",
        hitl_enabled=True,
        send_start_event=True,
        send_activity_start_event=True,
        # Enable instrumentation
        instrument_databases=True,
        db_libraries={"sqlalchemy"},
        instrument_file_io=False
    )

    # Run the worker
    print("Weather agent started. Waiting for workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())