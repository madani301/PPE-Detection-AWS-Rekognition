#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

  • Checks if an SQS Queue with name 'cpd-sqs-s1903342' already exists
  • If it does not exist, attempt to create the SQS Queue
  • Check if a queue with the same name has been deleted within 60 seconds
  • If yes, catch the error and start a 60-second timer 
  • If no error is thrown while creating the queue, exit
  • Attach the required access policy after its creation for 'SendMessage' access

"""

# Import the required libraries
import boto3
import json
import botocore
import time
import sys

# Create the resource for sqs
sqs = boto3.client("sqs")

# Set the SQS Queue Name
sqs_name = "cpd-sqs-s1903342"

# Open the 'sqs_policy.json' file and load it to return a JSON object
with open("/Users/madani/Desktop/CPD_Coursework/sqs_policy.json") as json_file:
    policy = json.load(json_file)

# This function verifies if the SQS Queue already exists
# If the queue exists, an error is thrown and printed in the console
# If a queue with the same name has been deleted within 60 seconds, an error is thrown
# A timer is launched an the queue creation proceeds after 60 seconds has passed
# After the creation of the queue, the required access policy for 'SendMessage' is attached
def get_queues(sqs):
    try:
        sqs.get_queue_url(QueueName="cpd-sqs-s1903342")
        print(
            "\n\033[93m"
            + " ••• SQS QUEUE 'cpd-sqs-s1903342' ALREADY EXISTS\n"
            + "\033[0m"
        )
        return True

    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]

    try:

        if error_code == "AWS.SimpleQueueService.NonExistentQueue":
            sqs.create_queue(QueueName=sqs_name)
            print(
                "\n\033[96m"
                + " ••• CREATING SQS QUEUE 'cpd-sqs-s1903342'\n"
                + "\033[0m"
            )
            time.sleep(5)
            print(
                "\n\033[96m" + " ••• ATTACHING REQUIRED ACCESS POLICIES'\n" + "\033[0m"
            )
            time.sleep(5)
            result = sqs.get_queue_url(QueueName="cpd-sqs-s1903342")
            sqs.set_queue_attributes(
                QueueUrl=result["QueueUrl"], Attributes={"Policy": json.dumps(policy)}
            )
            print(
                "\n\033[96m"
                + " ••• SQS QUEUE 'cpd-sqs-s1903342' HAS BEEN CREATED\n"
                + "\033[0m"
            )

    except botocore.exceptions.ClientError as x:
        error_code_ = x.response["Error"]["Code"]

        if error_code_ == "AWS.SimpleQueueService.QueueDeletedRecently":
            print(
                "\n\033[93m"
                + " ••• ANOTHER SQS QUEUE WITH THE SAME NAME CAN BE CREATED 60 SECONDS AFTER DELETION, PLEASE WAIT\n"
                + "\033[0m"
            )

            for remaining in range(60, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(
                    "\033[96m" + " ••• {:2d} SECONDS REMAINING".format(remaining)
                )
                sys.stdout.flush()
                time.sleep(1)

            sys.stdout.write("\r ••• SQS QUEUE SCRIPT LAUNCHED                  \n")

            sqs.create_queue(QueueName=sqs_name)
            print(
                "\n\033[96m"
                + " ••• CREATING SQS QUEUE 'cpd-sqs-s1903342'\n"
                + "\033[0m"
            )

            time.sleep(5)

            print(
                "\n\033[96m" + " ••• ATTACHING REQUIRED ACCESS POLICIES\n" + "\033[0m"
            )

            time.sleep(5)

            print(
                "\n\033[96m"
                + " ••• SQS QUEUE 'cpd-sqs-s1903342' HAS BEEN CREATED\n"
                + "\033[0m"
            )

            result = sqs.get_queue_url(QueueName="cpd-sqs-s1903342")
            sqs.set_queue_attributes(
                QueueUrl=result["QueueUrl"], Attributes={"Policy": json.dumps(policy)}
            )

            return False


get_queues(sqs)
