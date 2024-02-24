This project is deprecated.

# Durable Serverless Starter (Preview)
Sample project implementing serverless durable function execution in python using **Durable**.
In case you don't know what the heck Durable is, read about it [here](https://github.com/danzilberdan/py-durable/blob/main/GETTING_STARTED.md).

This sample uses:
- [pydurable](https://github.com/danzilberdan/py-durable) SDK to interact with Durable's backend
- [temporalio](https://pypi.org/project/temporalio/) for definition of Workflows and Activities
- [Serverless Framework](https://www.serverless.com/) for AWS Lambda management

## Set Up
- Clone this repo
- Check out the [Setup Guide](./SETUP.md) to get up and running.
- Checkout the [Gettings Started](./GETTING_STARTED.md) guide for a more in-depth explanation.

### Example
Check [main.py](./main.py) for the full example.

First we import the definitions for Temporal Workflows and Activities. We also import the `run` function from pydurable.
```python
from temporalio import activity, workflow
from pydurable.worker import run
...
```
Then we create our handler that will run in AWS Lambda's context. Our handler registers workflow and activities and delegates it's runtime to pydurable's `run` function.
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
        
            await asyncio.sleep(60 * 60)
```
