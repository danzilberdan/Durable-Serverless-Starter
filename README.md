# Durable Serverless
Build serverless stateful applications in python with zero complexity.

Usually, building stateful applications comes with many challenges:
- Data persistence
- Serialization and deserialization
- Spawning background jobs
- Handling failure and retry policies
- Scaling resources

Many of these challanges arise from the fact that we don't trust in-memory state for more than a few seconds, and rightly so. Processes may be closed for many reasons which results in the lose of all the state that was not persisted to disk. But what if we had a solution which enabled us to write simple python code with built-in data structures and trust the state to persist? Combine that with serverless compute which allows to run code in the cloud without taking care of servers. This is Durable.

## Features
- **Stateful** - Use in-memory data structures and simple python functions instead of queues, databases and schedulers to handle complex stateful applications.
- **Durable Execution** - Achive reliability with [Temporal](https://temporal.io/)'s built-in event sourcing and function replay capabilities.
- **Serverless** - Deploy faster without the need to maintain servers.
- **Cost** - Pay-per-use model. Idle long-running functions incur no compute costs.

### Stack
- Serverless with [Serverless Framework](https://www.serverless.com/)
- Durable execution built on top of [Temporal](https://temporal.io/)

## Getting Started
Clone this repo to get started using serverless durable functions.

## Set Up
Check out the [Setup Guide](./SETUP.md) to get up and running.

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
