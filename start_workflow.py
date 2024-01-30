from datetime import datetime, timedelta
import dotenv; dotenv.load_dotenv()
import asyncio
from pydurable.worker.client import get_client


async def main():
    client = await get_client()
    await client.execute_workflow(
        id="execution-id",
        task_queue="myproject-dev-durablefunc",
        workflow="GreetingWorkflow",
        arg="Dan",
        task_timeout=timedelta(seconds=10)
    )

if __name__ == '__main__':
    asyncio.run(main())
