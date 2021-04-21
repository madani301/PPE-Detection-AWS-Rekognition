#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

  • Checks if a table with a name starting with 'PPE' already exists
  • If it does not exist, a table named 'PPE_Detection' is created

"""

# Import the required libraries
import boto3

# Create the resource for dynamoDB
dynamodb = boto3.client("dynamodb")

# Get a list of tables with names starting with 'PPE'
# If there are no tables or no tables with names starting with 'PPE', a new table is created
table_check = dynamodb.list_tables(ExclusiveStartTableName="PPE", Limit=10)

table_name = table_check["TableNames"]

if len(table_name) == 0 or table_name != ["PPE_Detection"]:

    # KeySchema is the schema for the table, where KeyType 'HASH' is the partition key
    # AttributeDefinitions is where the data type is set, for e.g, Strings, Numbers, Booleans, etc.
    # ProvisionedThroughput is where the capacity for reading/writing is set for the dynamoDB table
    table = dynamodb.create_table(
        TableName="PPE_Detection",
        KeySchema=[{"AttributeName": "Image_Name", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "Image_Name", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )

else:
    print(
        "\n\033[93m"
        + " ••• TABLE WITH NAME: "
        + str(table_name)
        + " ALREADY EXISTS"
        + "\n"
        + "\033[0m"
    )
