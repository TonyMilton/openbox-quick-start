from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.fetch_weather_activity import fetch_weather_activity
    from activities.write_database_activity import write_database_activity

@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self, cities: list[str]):
        results = []

        for city in cities:
            # Step 1: Fetch weather data
            weather_data = await workflow.execute_activity(
                fetch_weather_activity,
                city,
                start_to_close_timeout=timedelta(seconds=60),
                task_queue="weather-tasks"
            )

            # Step 2: Write to database
            write_result = await workflow.execute_activity(
                write_database_activity,
                weather_data,
                start_to_close_timeout=timedelta(seconds=30),
                task_queue="weather-tasks"
            )

            results.append(write_result)

        return {
            "processed_cities": len(cities),
            "results": results
        }