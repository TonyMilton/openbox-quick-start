from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import fetch_weather

@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self) -> dict:
        return await workflow.execute_activity(
            fetch_weather,
            schedule_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                backoff_coefficient=2.0,
                maximum_interval=timedelta(seconds=10),
                maximum_attempts=3,
            ),
        )