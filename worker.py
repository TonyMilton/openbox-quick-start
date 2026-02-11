import asyncio
import os
from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow
from openbox import create_openbox_worker
from db import init_db

# Load environment variables from .env file
load_dotenv()  # Add this line

with workflow.unsafe.imports_passed_through():
    from workflows import SayHelloWorkflow, WeatherWorkflow
    from activities import greet, fetch_weather

async def main():
    # Initialize database
    init_db()

    client = await Client.connect("localhost:7233")

    worker = create_openbox_worker(
        client=client,
        task_queue="my-task-queue",
        workflows=[SayHelloWorkflow, WeatherWorkflow],
        activities=[greet, fetch_weather],

        # Add OpenBox configuration
        openbox_url=os.getenv("OPENBOX_URL"),
        openbox_api_key=os.getenv("OPENBOX_API_KEY"),

        # Optional: Capture database operations
        instrument_databases=True,
        db_libraries={"psycopg2"},  # Or None for alls

        # Optional: Capture file I/O
        instrument_file_io=True,
    )

    print("Worker started with weather activity registered.")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())