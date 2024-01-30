# Durable-Serverless-Starter (Preview)
Deploy durable workflows using serverless compute.
## Features
- **Durable Execution** - Develop reliable, long-running functions without the usual complexity (state management, queues, schedulers, etc.).
- **Serverless** - Deploy faster without the need to maintain servers.
- **Cost** - Pay-per-use model. Idle long-running functions incur no compute costs.

## Getting Started
Clone this repo to get started using Serverless Durable Workflows built on top of *Temporal*.

## Set Up
Check out the [Setup Guide](./SETUP.md) to get up and running.

### Stack
- Serverless with [Serverless Framework](https://www.serverless.com/)
- Durable execution built on top of [Temporal](https://temporal.io/)

### Example
Check [main.py](./main.py) for the full example.

First we import the definitions for Temporal Workflows and Activities. We also import the `run` function from pydurable.
```python
from temporalio import activity, workflow
from pydurable.worker import run
...
```
Then we create our handler that will run in AWS Lambda's context. Our handler registers workflow and activities and delegates it's runtime to [pydurable](https://pypi.org/project/pydurable/)'s `run` function.
```python
async def handler(event, context):
    return asyncio.run(
        run(workflows=[
            GreetingWorkflow
        ], activities=[
            compose_greeting
        ], context=context)
    )
```
Workflows and Activities are defined in temporal fasion.

```python
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
```