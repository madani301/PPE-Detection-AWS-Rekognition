import json
import boto3
from decimal import Decimal


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    ppe_client = boto3.client("rekognition")
    sns_client = boto3.client("sns")

    for msg in event["Records"]:
        msg_payload = json.loads(msg["body"])

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

            results = []

            for person in response["Persons"]:
                bp = person["BodyParts"]
                id = person["Id"]
                result = {"ID": id, "Details": []}

                for ed in bp:
                    name = ed["Name"]
                    ppe = ed["EquipmentDetections"]

                    if name == "FACE" or name == "HEAD":
                        if len(ppe) != 0:

                            for ppe_type in ppe:
                                types = ppe_type["Type"]
                                confidence = ppe_type["Confidence"]
                                covers_body_part_value = ppe_type["CoversBodyPart"][
                                    "Value"
                                ]
                                covers_body_part_confidence = str(
                                    ppe_type["CoversBodyPart"]["Confidence"]
                                )

                                person_details = {
                                    "Body Part": name,
                                    "Cover Type": types,
                                    "Confidence": str(confidence),
                                    "Covers Body Part": {
                                        "Confidence": covers_body_part_confidence,
                                        "Value": covers_body_part_value,
                                    },
                                }

                                result["Details"].append(person_details)

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

                if len(result["Details"]) > 0:
                    results.append(result)

                    table = boto3.resource("dynamodb").Table("PPE_Detection")
                    table.put_item(Item={"Image_Name": image, "Body": results})

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

                    table = boto3.resource("dynamodb").Table("PPE_Detection")
                    table.put_item(Item={"Image_Name": image, "Body": results})

            res = []

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

                        number = "+23052510301"
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

                        number = "+23052510301"
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

            print(res)

            # print(json.dumps(results))

    return {"statusCode": 200}
