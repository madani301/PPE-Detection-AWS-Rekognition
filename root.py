#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

This script calls all the required scripts and executes them in order.
A table of content is displayed for a period of time to explain the 
different scripts, and then the scripts are called one by one. 

The scripts imported are responsible for:
    • Creating the S3 Bucket 
    • Creating the SQS Queue
    • Attaching the access policy to the SQS Queue
    • Adding an Event Notification to the S3 Bucket 
    • Creating the DynamoDB Table 
    • Zipping the Lambda function and Upload it 
    • Creating an Event Source Mapping 
    • Uploading images to the S3 Bucket every 10 seconds 
    • Saving AWS Rekognition PPE Detection responses to the DynamoDB Table
    • Sending an SMS via the SNS service for responses indicating a false value for face covers 
    • Deleting all created resources sequentially after testing by prompting the user 

"""

# Import the required libraries
import time
import sys
import os

os.system("clear")

print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)
print("\033[1m" + "\033[96m" + " STUDENT NAME :   MADANI NAPAUL" + "\033[0m")
print("\033[1m" + "\033[96m" + " STUDENT ID   :   S1903342" + "\033[0m")
print("\033[1m" + "\033[96m" + " REGION       :   EU-WEST-2 (LONDON)" + "\033[0m")

print("\n\033[1m" + "\033[96m" + " THIS SCRIPT WILL: " + "\033[0m")

print("\n\033[96m" + " 1) CREATE AN S3 BUCKET" + "\033[0m")
print("\033[96m" + "     a) CHECK IF THE BUCKET EXISTS" + "\033[0m")
print(
    "\033[96m"
    + "     b) CREATE THE BUCKET IF IT DOES NOT EXIST, OTHERWISE SKIP"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 2) CREATE AN SQS QUEUE" + "\033[0m")
print("\033[96m" + "     a) CHECK IF THE SQS QUEUE EXISTS" + "\033[0m")
print(
    "\033[96m"
    + "     b) CHECK IF AN SQS QUEUE WITH A SIMILAR NAME HAS BEEN DELETED WITHIN 60 SECONDS"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 3) ATTACH ACCESS POLICY TO SQS QUEUE" + "\033[0m")
print("\033[96m" + "     a) ADD THE SEND MESSAGE POLICY TO THE SQS QUEUE" + "\033[0m")

time.sleep(2.5)

print("\n\033[96m" + " 4) CREATE AN S3 EVENT NOTIFICATION (PUT)" + "\033[0m")
print(
    "\033[96m"
    + "     a) ADD THE EVENT NOTIFICATION WHICH WILL SEND A MESSAGE TO SQS"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 5) CREATE A DYNAMODB TABLE" + "\033[0m")
print("\033[96m" + "     a) CHECK IF THE TABLE ALREADY EXISTS" + "\033[0m")
print(
    "\033[96m"
    + "     b) CREATE TABLE PPE_DETECTION WITH PRIMARY KEY 'IMAGE_NAME'"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 6) CREATE A LAMBDA FUNCTION" + "\033[0m")
print("\033[96m" + "     a) CHECK IF THE LAMBDA FUNCTION EXISTS" + "\033[0m")
print("\033[96m" + "     b) ZIP LAMBDA FUNCTION AND UPLOAD FUNCTION" + "\033[0m")

time.sleep(2.5)

print("\n\033[96m" + " 7) CREATE AN SQS TRIGGER FOR THE LAMBDA FUNCTION" + "\033[0m")
print(
    "\033[96m" + "     a) CHECK IF THE EVENT SOURCE MAPPING EXISTS (UUID)" + "\033[0m"
)
print("\033[96m" + "     b) CREATE THE EVENT SOURCE MAPPING" + "\033[0m")

time.sleep(2.5)

print("\n\033[96m" + " 8) UPLOAD IMAGES TO S3 BUCKET EVERY 10 SECONDS" + "\033[0m")
print(
    "\033[96m"
    + "     a) UPLOAD IMAGES ONE BY ONE, OVERWRITE IMAGE IF ALREADY IN BUCKET"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 9) STORE PPE DETECTION RESPONSE IN DYNAMODB TABLE" + "\033[0m")
print("\033[96m" + "     a) FILTER OUT KEY DATA REQUIRED" + "\033[0m")

time.sleep(2.5)

print(
    "\n\033[96m"
    + " 10) SEND SMS VIA SNS FOR RESPONSE INDICATING 'NO FACE MASK'"
    + "\033[0m"
)
print(
    "\033[96m"
    + "     a) FOR ALL RESPONSES INDICATING NO MASKS, SEND AN SMS"
    + "\033[0m"
)

time.sleep(2.5)

print("\n\033[96m" + " 11) DELETE ALL RESOURCES CREATED ON AWS" + "\033[0m")
print(
    "\033[96m"
    + "     a) PERFORM APPROPRIATE CHECKS BEFORE DELETING RESOURCES"
    + "\033[0m"
)
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

for remaining in range(15, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("\033[96m" + " ••• {:2d} SECONDS REMAINING".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\r ••• LAUNCHING SCRIPTS                  \n")

time.sleep(2.5)


def create_bucket():
    import s3


def create_sqs():
    import sqs


def s3_event():
    import event_notification


def create_table():
    import table


def deploy_lambda():
    import deploy


def upload():
    from upload import upload_files

    upload_files("/Users/madani/Desktop/CPD_Coursework/images")


create_bucket()
time.sleep(5)
print("\n\033[1m" + "\033[92m" + " ••• S3 BUCKET CREATION COMPLETED\n" + "\033[0m")
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

create_sqs()
time.sleep(5)
print("\n\033[1m" + "\033[92m" + " ••• SQS QUEUE CREATION COMPLETED\n" + "\033[0m")
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

s3_event()
time.sleep(5)
print("\n\033[96m" + " ••• ADDING S3 EVENT NOTIFICATION (PUT)\n" + "\033[0m")
time.sleep(2.5)
print("\n\033[1m" + "\033[92m" + " ••• S3 'PUT' EVENT NOTIFICATION ADDED\n" + "\033[0m")
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

create_table()
print("\n\033[96m" + " ••• CREATING DYNAMODB TABLE 'PPE_DETECTION'\n" + "\033[0m")
time.sleep(5)
print(
    "\n\033[1m"
    + "\033[92m"
    + " ••• DYNAMODB TABLE 'PPE_DETECTION' CREATION COMPLETED\n"
    + "\033[0m"
)
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

deploy_lambda()
time.sleep(5)
print(
    "\n\033[1m" + "\033[92m" + " ••• LAMBDA FUNCTION DEPLOYMENT COMPLETED\n" + "\033[0m"
)
print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

for remaining in range(5, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write(
        "\033[96m" + " ••• {:2d} SETTING UP LAMBDA FUNCTION".format(remaining)
    )
    sys.stdout.flush()
    time.sleep(2)

sys.stdout.write(
    "\033[1m"
    + "\033[92m"
    + "\r ••• LAMBDA FUNCTION IS NOW ACTIVE                          \n"
    + "\033[0m"
)

time.sleep(3)

upload()
time.sleep(5)
print("\n\033[1m" + "\033[92m" + " ••• IMAGE UPLOAD COMPLETED\n" + "\033[0m")

print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

for remaining in range(10, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write(
        "\033[96m"
        + " ••• {:2d} STORING PPE DETECTION RESPONSES TO DYNAMODB TABLE".format(
            remaining
        )
    )
    sys.stdout.flush()
    time.sleep(2)

sys.stdout.write(
    "\033[1m"
    + "\033[92m"
    + "\r ••• RESPONSES SAVED TO DYNAMODB TABLE                                         \n"
    + "\033[0m"
)

print(
    "\n\033[1m"
    + "\033[96m"
    + " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n"
    + "\033[0m"
)

print(
    "\n\033[1m"
    + "\033[92m"
    + " ••• DEPLOYMENT COMPLETED, CHECK AWS CONSOLE\n"
    + "\033[0m"
)

while True:

    prompt = input(
        "\n\033[1m"
        + "\033[96m"
        + " ••• CLEAN UP RESOURCES CREATED ON AWS? [Y/N]:\n\n     ANSWER: "
        + "\033[0m"
    )

    if prompt == "Y" or prompt == "y":
        import clean

        print(
            "\n\033[1m"
            + "\033[92m"
            + " ••• RESOURCES DELETED, CHECK AWS CONSOLE\n"
            + "\033[0m"
        )
        break

    elif prompt == "N" or prompt == "n":
        print("\n\033[1m" + "\033[92m" + " ••• PROGRAM TERMINATED\n" + "\033[0m")
        break

    else:
        print(
            "\n\033[93m" + "     PLEASE ENTER A VALID CHARACTER [Y/y/N/n]" + "\033[0m"
        )
        continue