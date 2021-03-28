#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

This script makes use of the subprocess library to run an AWS CLI command to
add an 'Event Notification' under 'Properties' for the S3 Bucket 'cpd-s3-s1903342'.

The 'PUT' event notification will send a message to the SQS Queue every time a file
is uploaded in the S3 Bucket. 

"""
# Import the required libraries
import subprocess

# Run the AWS CLI command to add the event notification to the S3 Bucket
# The notification configuration is in the 'notification.json' file
subprocess.call(
    [
        "aws",
        "s3api",
        "put-bucket-notification",
        "--bucket",
        "cpd-s3-s1903342",
        "--notification-configuration" "=file://notification.json",
    ]
)
