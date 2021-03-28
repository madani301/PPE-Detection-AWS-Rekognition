#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

The 'deploy.py' script zips the 'lambda_function.py' and attaches the code to
the function's (cpd-lambda-s1903342) 'lambda_handler' function.

The script uses the subprocess library which allows Python to run CLI commands. 

"""
# Import the required libraries
import subprocess
import time
import botocore
import boto3

# Create the lambda resource
client = boto3.client("lambda")

# Checks if the function 'cpd-lambda-s1903342' already exists
try:
    lambda_check = client.get_function(FunctionName="cpd-lambda-s1903342")
    print(
        "\n\033[93m"
        + " ••• LAMBDA FUNCTION 'cpd-lambda-s1903342' ALREADY EXISTS\n"
        + "\033[0m"
    )

# Catch the error and create the function
# Zip the 'lambda_function' and attach it to the 'lambda_handler' default function
# Deploy the lambda function
except botocore.exceptions.ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "ResourceNotFoundException":
        print("\n\033[96m" + " ••• ZIPPING LAMBDA FUNCTION\n" + "\033[0m")
        time.sleep(2)
        print("\n\033[96m" + " ••• UPLOADING LAMBDA FUNCTION\n")
        subprocess.call(["zip", "cpd-lambda-s1903342.zip", "lambda_function.py"])
        subprocess.call(
            [
                "aws",
                "lambda",
                "create-function",
                "--function-name",
                "cpd-lambda-s1903342",
                "--zip-file",
                "fileb://cpd-lambda-s1903342.zip",
                "--handler",
                "lambda_function.lambda_handler",
                "--runtime",
                "python3.7",
                "--role",
                "arn:aws:iam::290644667118:role/service-role/admin",
            ]
        )
        time.sleep(5)

        print(
            "\n\033[96m" + " ••• CREATING EVENT SOURCE MAPPING BETWEEN SQS AND LAMBDA\n"
        )

        # Check if there is an existing event source mapping
        # If there are no event source mappings, create one between SQS and Lambda
        # If the lambda has not been created yet, print an error message to alert the user
        event_source = client.list_event_source_mappings(
            FunctionName="cpd-lambda-s1903342",
        )
        mappings = event_source["EventSourceMappings"]

        if len(mappings) == 0:
            try:
                subprocess.call(
                    [
                        "aws",
                        "lambda",
                        "create-event-source-mapping",
                        "--function-name",
                        "cpd-lambda-s1903342",
                        "--batch-size",
                        "10",
                        "--event-source-arn",
                        "arn:aws:sqs:eu-west-2:290644667118:cpd-sqs-s1903342",
                    ]
                )
                time.sleep(5)

            except botocore.exceptions.ClientError as e:
                error_code = e.response["Error"]["Code"]

                if error_code == "InvalidParameterValueException":
                    print(
                        "\n\033[93m"
                        + " ••• LAMBDA FUNCTION HAS NOT BEEN CREATED YET\n"
                        + "\033[0m"
                    )

                else:
                    uuid = event_source["EventSourceMappings"][0]["UUID"]
                    print(
                        "\n\033[93m"
                        + " ••• EVENT SOURCE MAPPING EXISTS WITH UUID: "
                        + uuid
                        + " \n"
                        + "\033[0m"
                    )
