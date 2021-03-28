#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

  • Checks if the created resources are still active
  • Attempts to delete the resources sequentially:
        - Empties the S3 Bucket 
        - Deletes the S3 Bucket 
        - Deletes the SQS Queue
        - Deletes the Event Source Mapping 
        - Deletes the Lambda Function
        - Deletes the DynamoDB Table
        - Deletes the CloudWatch Log Group 

"""

# Import the required libraries
import subprocess
import boto3
import botocore
import time
import json

# Create the required resources for each service
s3 = boto3.resource("s3")
sqs = boto3.client("sqs")
l_client = boto3.client("lambda")
t_client = boto3.client("dynamodb")


# Check if the S3 Bucket exists
# Attempt to empty the bucket by deleting the files recursively
try:
    s3.meta.client.head_bucket(Bucket="cpd-s3-s1903342")
    subprocess.call(["aws", "s3", "rm", "s3://cpd-s3-s1903342", "--recursive"])
    print(
        "\n\033[92m"
        + "\n\033[1m"
        + " ••• S3 BUCKET 'cpd-s3-s1903342' HAS BEEN EMPTIED\n"
        + "\033[0m"
    )
    time.sleep(3)

except botocore.exceptions.ClientError as e:
    error_code = int(e.response["Error"]["Code"])
    if error_code == 404:
        print(
            "\n\033[93m"
            + " ••• CANNOT EMPTY S3 BUCKET, IT DOES NOT EXIST, OPERATION ABORTED\n"
            + "\033[0m"
        )
        time.sleep(5)

# Check if the S3 Bucket exists
# Delete the empty S3 Bucket
try:
    s3.meta.client.head_bucket(Bucket="cpd-s3-s1903342")
    subprocess.call(["aws", "s3", "rb", "s3://cpd-s3-s1903342"])
    print(
        "\n\033[92m"
        + "\n\033[1m"
        + " ••• S3 BUCKET 'cpd-s3-s1903342' HAS BEEN DELETED\n"
        + "\033[0m"
    )
    time.sleep(3)

except botocore.exceptions.ClientError as e:
    error_code = int(e.response["Error"]["Code"])
    if error_code == 404:
        print(
            "\n\033[93m"
            + " ••• S3 BUCKET DOES NOT EXIST, OPERATION ABORTED\n"
            + "\033[0m"
        )
        time.sleep(5)

# Check if the SQS Queue exists
#  Delete the SQS Queue
try:
    queue_check = sqs.get_queue_url(
        QueueName="cpd-sqs-s1903342", QueueOwnerAWSAccountId="290644667118"
    )
    queue = queue_check["QueueUrl"]
    subprocess.call(["aws", "sqs", "delete-queue", "--queue-url", queue])
    print(
        "\n\033[92m"
        + "\n\033[1m"
        + " ••• SQS QUEUE 'cpd-sqs-s1903342' HAS BEEN DELETED\n"
        + "\033[0m"
    )
    time.sleep(3)

except botocore.exceptions.ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "AWS.SimpleQueueService.NonExistentQueue":
        print(
            "\n\033[93m"
            + " ••• NO SQS QUEUE AVAILABLE, OPERATION ABORTED\n"
            + "\033[0m"
        )
        time.sleep(3)

# Check if the DynamoDB Table exists
# Delete the table
try:
    table_check = t_client.list_tables(ExclusiveStartTableName="PPE", Limit=10)
    table_name = table_check["TableNames"]

    if len(table_name) == 0 or table_name != ["PPE_Detection"]:
        print(
            "\n\033[93m" + " ••• NO TABLES AVAILABLE, OPERATION ABORTED\n" + "\033[0m"
        )
        time.sleep(3)

    else:
        subprocess.call(
            ["aws", "dynamodb", "delete-table", "--table-name", "PPE_Detection"]
        )
        print(
            "\n\033[92m"
            + "\n\033[1m"
            + " ••• DYNAMODB TABLE 'PPE_DETECTION' HAS BEEN DELETED\n"
            + "\033[0m"
        )
        time.sleep(3)

except botocore.exceptions.ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "ResourceNotFoundException":
        print(
            "\n\033[93m"
            + " ••• NO DYNAMODB TABLES AVAILABLE, OPERATION ABORTED\n"
            + "\033[0m"
        )
        time.sleep(3)

# Delete CloudWatch Logs
subprocess.call(
    [
        "aws",
        "logs",
        "delete-log-group",
        "--log-group-name",
        "/aws/lambda/cpd-lambda-s1903342",
    ]
)
print(
    "\n\033[92m"
    + "\n\033[1m"
    + " ••• CLOUDWATCH LOG GROUP 'cpd-lambda-s1903342' HAS BEEN DELETED\n"
    + "\033[0m"
)
time.sleep(3)

# Check if an Event Source Mapping exists between the specified SQS Queue and Lambda function
# Delete the Event Source Mapping
event_source = l_client.list_event_source_mappings(
    FunctionName="cpd-lambda-s1903342",
)

mappings = event_source["EventSourceMappings"]

if len(mappings) == 0:
    print(
        "\n\033[93m" + " ••• NO EVENT SOURCE MAPPINGS, OPERATION ABORTED\n" + "\033[0m"
    )
    time.sleep(3)

else:
    uuid = event_source["EventSourceMappings"][0]["UUID"]
    subprocess.call(["aws", "lambda", "delete-event-source-mapping", "--uuid", uuid])
    print(
        "\n\033[92m"
        + "\n\033[1m"
        + " ••• EVENT SOURCE MAPPING WITH UUID: "
        + uuid
        + " HAS BEEN DELETED\n"
        + "\033[0m"
    )
    time.sleep(3)

# Check if the Lambda Function exists
# Delete the Lambda Function
try:
    lambda_check = l_client.get_function(FunctionName="cpd-lambda-s1903342")
    func_name = lambda_check["Configuration"]["FunctionName"]
    subprocess.call(
        ["aws", "lambda", "delete-function", "--function-name", "cpd-lambda-s1903342"]
    )
    print(
        "\n\033[92m"
        + "\n\033[1m"
        + " ••• LAMBDA FUNCTION 'cpd-lambda-s1903342' HAS BEEN DELETED\n"
        + "\033[0m"
    )
    time.sleep(3)

except botocore.exceptions.ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "botocore.errorfactory.ResourceNotFoundException":
        print(
            "\n\033[93m"
            + " ••• NO LAMBDA FUNCTIONS AVAILABLE, OPERATION ABORTED\n"
            + "\033[0m"
        )
        time.sleep(3)