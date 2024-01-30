from collections import namedtuple
import os
import sys; sys.path.insert(0, 'vendor')
import asyncio
from datetime import timedelta
from dataclasses import dataclass

from temporalio import activity, workflow
from pydurable.worker import run


@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


@activity.defn
async def compose_greeting(input: ComposeGreetingInput) -> str:
    print("Running activity with parameter %s" % input)
    return f"{input.greeting}, {input.name}!"


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        for _ in range(5):
            print("Running workflow with parameter %s" % name)
            await workflow.execute_activity(
                compose_greeting,
                ComposeGreetingInput("Hello", name),
                start_to_close_timeout=timedelta(seconds=10),
            )
        
            await asyncio.sleep(30)


async def handler(event, context):
    asyncio.run(
        run(workflows=[
            GreetingWorkflow
        ], activities=[
            compose_greeting
        ], context=context)
    )

    return {"statusCode": 200, "body": "Completed"}
