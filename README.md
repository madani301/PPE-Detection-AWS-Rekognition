# Cloud Platform Development (MHI324190)

## _Personal Protective Equipment (PPE) Detection & Notification System with AWS AI Services_

### Introduction
The purpose of this coursework is to demonstrate an understanding of cloud applications and software development on AWS cloud platform. The tasks are to design and implement an application to analyse an image to detect **Personal Protective Equipment (PPE)** using **AWS Rekognition**.

---
### Specifications

##### 1) Resource Creation with Boto3
- Create an S3 Bucket and SQS Queue using Python (Boto3)

##### 2) Image Upload and Lambda Trigger from SQS
- Upload images from local directory to **S3 Bucket** every 10 seconds 
- Send a message to **SQS Queue** when an image is uploaded in the S3 Bucket
- Create a **Lambda** function which will be triggered by **SQS (Event Source Mapping)**

##### 3) PPE Detection with AWS Rekognition
- Extract relevant details from the SQS message when the Lambda function is triggered 
- Make a call to **AWS Rekognition PPE Detection** through the Lambda function using the image details extracted 
- AWS Rekognition PPE Detection will detect **'FACE_COVER'** and **'HEAD_COVER'**

##### 4) Database Updates and SMS Notification
- Store the PPE Detection responses in a **DynamoDB** table (Single Partition) with the image name as primary key 
- Extract relevant details such as **true/false values** and **confidence level** to be stored in the table 
- For responses indicating the absence of a **face mask**, send an SMS to a phone number using **AWS Simple Notification System (SNS)**

---
### Installation 
##### 1) Create an AWS Account
Read more about creating and activating an [AWS Account]. Download your **Access Key ID** and **Secret Key**. 

##### 2) Identity and Access Management (IAM)
Ensure the following policies are attached to specific roles and users:
- AmazonS3FullAccess
- AmazonSQSFullAccess
- AWSLambdaBasicExecutionRole 
- AWSLambdaSNSPublishPolicyExecutionRole (SNS: Publish)
- AmazonRekognitionReadOnlyAccess 
- AWSDynamoDBFullAccess

##### 3) Installing the AWS CLI
For the latest version of the AWS CLI, use the following command block: 
```sh
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

To verify that the shell can find and run the aws command in your **$PATH**, use the following commands:
```sh
which aws
aws --version
```

##### 4) AWS SDK for Python

Assuming that you have Python and virtualenv installed, set up your environment and install the required dependencies using **pip**:
```sh
python -m pip install boto3
```
After installing **boto3**, set up credentials (in e.g. `~/.aws/credentials`):
```sh
nano ~/.aws/credentials
```
```sh
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

Then, set up a default region (in e.g. `~/.aws/config`):
```sh
nano ~/.aws/config
```
```sh
[default]
region = eu-west-2
```
---

### Usage

**The following needs to be adjusted according to your AWS Account setup in the scripts:**
- Account ID 
- Role Names
- User Names 
- Region

Ensure they are updated before launching the scripts. The scripts make use of **Non-ASCII** characters **without encoding**, ensure you are running the scripts using **Python3**.

Launch the main script `root.py`:

``` sh
python3 root.py
```

---

### License

MIT License

Copyright (c) 2021 Madani Napaul

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.



   [AWS Account]: <https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/>

