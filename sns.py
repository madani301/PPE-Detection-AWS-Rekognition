import json
import boto3

sns_client = boto3.client("sns")

number = "+23052510301"
message = "test"
message_attributes = {
    "AWS.SNS.SMS.SMSType": {"DataType": "String", "StringValue": "Transactional"}
}
sns_client.publish(
    PhoneNumber=number, Message=str(message), MessageAttributes=message_attributes
)
