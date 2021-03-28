#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

  • Checks if an S3 Bucket named 'cpd-s3-s1903342' exists
  • Checks if the bucket has private or public access
  • Creates an S3 Bucket if not already available

"""

# Import the required libraries
import boto3
import botocore

# Create the resource for S3
s3 = boto3.resource("s3")

# Set the bucket name
bucket_name = "cpd-s3-s1903342"
bucket = s3.Bucket(bucket_name)

# This function first checks whether a bucket with the name 'cpd-s3-s1903342' already exists
# It then checks whether the access is forbidden, hence throwin a 403 error
# If the error is 404, then the requested bucket is not available, hence create a new bucket
def check_bucket(bucket):
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        print(
            "\n\033[93m"
            + " ••• S3 BUCKET 'cpd-s3-1903342' ALREADY EXISTS. PLEASE CHECK S3 ON AWS CONSOLE\n"
            + "\033[0m"
        )
        return True

    except botocore.exceptions.ClientError as e:
        error_code = int(e.response["Error"]["Code"])

        if error_code == 403:

            print("\n\033[93m" + " ••• PRIVATE BUCKET, FORBIDDEN ACCESS\n" + "\033[0m")
            return True

        elif error_code == 404:

            s3.create_bucket(
                Bucket="cpd-s3-s1903342",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )

            print(
                "\n\033[96m"
                + " ••• S3 BUCKET 'cpd-s3-s1903342' HAS BEEN CREATED SUCCESSFULLY. PLEASE CHECK S3 ON AWS CONSOLE\n"
                + "\033[0m"
            )
            return False


check_bucket(bucket)
