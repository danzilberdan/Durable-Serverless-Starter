# Installation Guide
- Clone this project
- Install Serverless Framework
```bash
npm install -g serverless
```bash
- Install Durable's cli
```bash
pip install pydurable[cli]
```
- Sign in to Durable
```bash
durable login
```
- Configure your AWS account id. [Don't know your account id?](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html#ViewYourAWSId)
```bash
durable aws update-account <AWS_ACCOUNT_ID>
```
- Take note of your external_id and role_name by running:
```bash
durable aws info
# OUTPUT: {'account_id': '<your account id>', 'external_id': 'your external id', 'role_name': '<your role name>'}
```
## In AWS console &rarr; IAM
- Click `Create role`
- Choose `Custom trust policy`
- Paste the following policy (Replace external_id according to previous step). Click **Next**.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::035921462565:user/durable"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "<external_id>"
                }
            }
        }
    ]
}
```
- In **Add permissions** search for `AWSLambdaRole` and choose it.  Click **Next**. (This role let's Durable invoke Lambda Functions on your account on demand)
- Set the **Role name** according to the output of `durable aws info` (If you would like to change to a different role_name, you can but also need to run `durable aws update-role <role_name>`)
- Click on **Create role**
## API Keys
- In order to authenticate to Durable, create an API key.
```bash
durable keys create
# Output:
# Your new API KEY is: <api_key>.
durable keys list
# Output:
# API KEYS:
#  0. "<api_key>"
```
- Create a `.env` file at the root folder of this repo
- Add the following to the `.env` (Replace with your API key)
```toml
API_KEY=<api_key>
```
## Deploy to Lambda
- Set up [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- In project root -
```bash
pip install -t vendor -r aws_requirements.txt
```
- Then deploy
```bash
sls deploy
# Output:
# Deploying myproject to stage dev (us-east-1)

# ✔ Service deployed to stack myproject-dev (105s)

# functions:
#   durablefunc: myproject-dev-durablefunc (11 kB)
```
- Copy the **full** Lambda function name, in the examples case `myproject-dev-durablefunc`.
- Register the function to Durable
```bash
durable func register <function_name>
# Output:
# Registered <function_name>.
```
- Modify `start_workflow.py` to call your function (Replace function_name in task_queue) -
```python
async def main():
    client = await get_client()
    await client.execute_workflow(
        id="execution-id",
        task_queue="<function_name>",
        workflow="GreetingWorkflow",
        arg="Dan",
        task_timeout=timedelta(seconds=10)
    )
```
- Install local dependencies -
```bash
poetry install
```
- Start the workflow!
```bash
poetry run python start_workflow.py
```
