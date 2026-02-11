import asyncio
import uuid
from dotenv import load_dotenv
from temporalio.client import Client

# Load environment variables from .env file
load_dotenv()

async def main():
    client = await Client.connect("localhost:7233")

    # Execute WeatherWorkflow with unique ID
    result = await client.execute_workflow(
        "WeatherWorkflow",
        id=f"weather-workflow-{uuid.uuid4()}",
        task_queue="my-task-queue",
    )

    # Print formatted result
    print("\n📍 Weather Data Retrieved:")
    print(f"   Location: {result['location']}")
    print(f"   Status: {result['weather_status']}")
    print(f"   Temperature: {result['temperature']}°C")
    print(f"   Humidity: {result['humidity']}%")
    print(f"   Description: {result['description']}")
    print(f"   Timestamp: {result['timestamp']}")
    print(f"   Database ID: {result['id']}")
    print()

if __name__ == "__main__":
    asyncio.run(main())
