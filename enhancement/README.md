# Cloud Platform Development (MHI324190)

## _Personal Protective Equipment (PPE) Detection & Notification System with AWS AI Services_

### Introduction
The purpose of this coursework is to demonstrate an understanding of cloud applications and software development on AWS cloud platform. The tasks are to design and implement an application to analyse an image to detect **Personal Protective Equipment (PPE)** using **AWS Rekognition**.

---
### Enhancement

This enhancement was attached to the main repository as a support to the Cloud Platform Development Report. 

This enhancement contains scripts to:
* Extract file names from the 'files' directory
* Store the file names in a JSON file using an array
* Split the JSON file into smaller files of less than 64KB
* Send every file less than 64KB as messages to the SQS Queue 

This attempt was made to lower the SQS costs where AWS bills for Receive, Send, and Delete requests. 


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

