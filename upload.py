#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

  • Identifies the directory containing the files to be uploaded
  • Uploads one file every 10 seconds 

"""

# Import the required libraries
import boto3
import os
import time
import botocore

# Remove all files not having the .jpg extension
dir_name = "/Users/madani/Desktop/CPD_Coursework/images"
main_dir = os.listdir(dir_name)

for item in main_dir:
    if item.endswith(".jpg") == False:
        os.remove(os.path.join(dir_name, item))

# This function uploads all files in the specified directory to the S3 Bucket 'cpd-s3-s1903342
def upload_files(path):
    session = boto3.Session()
    s3 = session.resource("s3")
    bucket = s3.Bucket("cpd-s3-s1903342")

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, "rb") as data:
                print(
                    "\n\033[96m"
                    + " ••• UPLOADING "
                    + file
                    + " INTO S3 BUCKET (cpd-s3-s1903342). PLEASE WAIT..."
                    + "\033[0m"
                )
                bucket.put_object(
                    Key=full_path[len(path) + 1 : time.sleep(1)],
                    Body=data,
                )
                print(
                    "\033[1m"
                    + "\033[96m"
                    + "     "
                    + file
                    + " UPLOADED SUCCESSFULLY\n"
                    + "\033[0m"
                )

    print("\n\033[96m" + " ••• FILES UPLOADED SUCCESSFULLY\n" + "\033[0m")


if __name__ == "__main__":
    upload_files("/Users/madani/Desktop/CPD_Coursework/images")
