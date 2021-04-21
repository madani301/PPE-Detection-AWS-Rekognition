#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

This script is the Lambda function which:

        • Extracts relevant details from the SQS messages 
        • Uses image names extracted to call AWS Rekognition PPE Detection to analyze
          the images with exact names in the S3 Bucket 
        • Manipulates the response from AWS Rekognition PPE Detection to handle only
          'FACE' and 'HEAD' as body parts
        • Stores the responses in the DynamoDB Table 'PPE_Detection'
        • Sends an SMS to a specified phone number for persons not wearing a 'FACE_COVER'

This script is zipped and unpacked on AWS for the Lambda function 'cpd-lambda-s1903342'

"""
# Import the required libraries
import json
import boto3


def lambda_handler(event, context):

    # Create the required resources
    ppe_client = boto3.client("rekognition")
    sns_client = boto3.client("sns")
    table = boto3.resource("dynamodb").Table("PPE_Detection")

    # Load the messages from the SQS Queue into JSON Objects
    for msg in event["Records"]:
        msg_payload = json.loads(msg["body"])

        # If there are 'Records' in the messages; the messages are not empty
        # Extract the bucket name and the image name
        # Request AWS Rekognition PPE Detection to analyze images in the S3 Bucket with the extracted image names
        # Set the Required Equipment Types to 'FACE_COVER' and 'HEAD_COVER'
        # Set the Minimum Confidence
        if "Records" in msg_payload:
            bucket = msg_payload["Records"][0]["s3"]["bucket"]["name"]
            image = msg_payload["Records"][0]["s3"]["object"]["key"].replace("+", " ")
            response = ppe_client.detect_protective_equipment(
                Image={"S3Object": {"Bucket": bucket, "Name": image}},
                SummarizationAttributes={
                    "MinConfidence": 75,
                    "RequiredEquipmentTypes": ["FACE_COVER", "HEAD_COVER"],
                },
            )

            # Create an empty dictionary which will be used later to append the manipulated data
            results = []

            # Access the body parts of all persons detected from AWS Rekognition PPE Detection
            # Create a dictionary 'result' where the data will be constantly appended
            for person in response["Persons"]:
                bp = person["BodyParts"]
                id = person["Id"]
                result = {"ID": id, "Details": []}

                # Access the Equipment Detected of the response
                for ed in bp:
                    name = ed["Name"]
                    ppe = ed["EquipmentDetections"]

                    # Check if the Body Part is 'FACE" or 'HEAD'
                    # Ignore other responses such as 'HAND'
                    # Execute this block of code only if PPE Equipment were detected
                    if name == "FACE" or name == "HEAD":
                        if len(ppe) != 0:

                            # Create variables for specific data required
                            for ppe_type in ppe:
                                types = ppe_type["Type"]
                                confidence = ppe_type["Confidence"]
                                covers_body_part_value = ppe_type["CoversBodyPart"]["Value"]
                                covers_body_part_confidence = str(ppe_type["CoversBodyPart"]["Confidence"])

                                # Set up the data format required to push into the DynamoDB Table
                                person_details = {
                                    "Body Part": name,
                                    "Cover Type": types,
                                    "Confidence": str(confidence),
                                    "Covers Body Part": {
                                        "Confidence": covers_body_part_confidence,
                                        "Value": covers_body_part_value,
                                    },
                                }

                                # Append the data for body parts where PPE Equipment were detected
                                result["Details"].append(person_details)

                        # If no PPE Equipment were detected for 'HEAD' or 'FACE',
                        # Set the value to 'False' and the other data as 0
                        # Append the data to the 'result' dictionary
                        else:

                            if name == "FACE":

                                person_details = {
                                    "Body Part": name,
                                    "Cover Type": "FACE_COVER",
                                    "Confidence": 0,
                                    "Covers Body Part": {
                                        "Confidence": 0,
                                        "Value": False,
                                    },
                                }

                            elif name == "HEAD":

                                person_details = {
                                    "Body Part": name,
                                    "Cover Type": "HEAD_COVER",
                                    "Confidence": 0,
                                    "Covers Body Part": {
                                        "Confidence": 0,
                                        "Value": False,
                                    },
                                }

                            result["Details"].append(person_details)

                # Append the data for all persons detected by AWS Rekognition PPE Detection
                if len(result["Details"]) > 0:
                    results.append(result)

                    # Create the resource for DynamoDB
                    # Insert the 'results' dictionary into the table
                    table.put_item(Item={"Image_Name": image, "Body": results})

                # If results is empty, it means the responses were below the confidence level
                # Or, the face nor head has been detected properly by AWS Rekognition PPE Detection
                # Set the data as 'indeterminate', for it cannot be classified
                # Append the data to the 'results' dictionary
                # Create the DynamoDB resource and insert the dictionary 'results' into the table
                if len(results) == 0:
                    person_details = {
                        "Body Part": "Indeterminate",
                        "Cover Type": "Indeterminate",
                        "Confidence": 0,
                        "Covers Body Part": {
                            "Confidence": 0,
                            "Value": "Indeterminate",
                        },
                    }

                    results.append({"ID": id, "Details": [person_details]})

                    table.put_item(Item={"Image_Name": image, "Body": results})

            # Create an empty dictionary which will contain only the data for persons without a 'FACE_COVER'
            res = []

            # Access the required Keys in the 'results' dictionary
            # Check if the body part is 'FACE' and the Equipment Detected is 'FACE_COVER'
            # Append the result to the 'res' dictionary
            # If the value 'CoversBodyPart' is 'False' or 'Indeterminate', send an SMS to the specified number
            for items in results:
                details = items["Details"]

                for covers in details:
                    ct = covers["Cover Type"]
                    fv = str(covers["Covers Body Part"]["Value"])

                    if ct == "FACE_COVER" and (
                        fv == "false" or fv == "False" or fv == False
                    ):
                        res.append(
                            {"Image_Name": image, "ID": id, "Type": ct, "Value": fv}
                        )

                        number = "+ZZ- ZZZZZZZZZZ"
                        message = "Image Name:", image, "ID:", id, "Value:", fv
                        message_attributes = {
                            "AWS.SNS.SMS.SMSType": {
                                "DataType": "String",
                                "StringValue": "Transactional",
                            }
                        }
                        sns_client.publish(
                            PhoneNumber=number,
                            Message=str(message),
                            MessageAttributes=message_attributes,
                        )

                    elif ct == "Indeterminate" and (fv == "Indeterminate"):
                        res.append(
                            {"Image_Name": image, "ID": id, "Type": ct, "Value": fv}
                        )

                        number = "+ZZ- ZZZZZZZZZZ"
                        message = "Image Name:", image, "Value: Indeterminate"
                        message_attributes = {
                            "AWS.SNS.SMS.SMSType": {
                                "DataType": "String",
                                "StringValue": "Transactional",
                            }
                        }
                        sns_client.publish(
                            PhoneNumber=number,
                            Message=str(message),
                            MessageAttributes=message_attributes,
                        )

            # print(res)

            # print(json.dumps(results))

    return {"statusCode": 200}
