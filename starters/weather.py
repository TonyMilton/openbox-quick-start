import asyncio
import uuid
from dotenv import load_dotenv
from temporalio.client import Client

load_dotenv()

async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        "WeatherWorkflow",
        ["Seattle", "London", "Tokyo"],
        id=f"weather-workflow-{uuid.uuid4()}",
        task_queue="weather-tasks",
    )

    print("\n📍 Weather Workflow Completed:")
    print(f"   Processed Cities: {result['processed_cities']}")
    print(f"   Results: {result['results']}")
    print()

if __name__ == "__main__":
    asyncio.run(main())
