import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv('./data/.env')


# Specify the name of your Log Group and Log Stream
log_group_name = os.getenv('ANALYTICS_GROUP')
log_stream_name = os.getenv('ANALYTICS_STREAM')
aws_region = os.getenv('AWS_REGION')
aws_profile = os.getenv('AWS_PROFILE')

# Create a CloudWatch Logs client
session = boto3.Session(region_name=aws_region, profile_name=aws_profile)
client = session.client('logs')

# Ensure the Log Group exists
try:
    client.create_log_group(logGroupName=log_group_name)
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
        raise

# Ensure the Log Stream exists within the Log Group
try:
    client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
        raise

# Get the sequence token (required for existing log streams with events)
try:
    response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
    sequence_token = response['logStreams'][0].get('uploadSequenceToken')
except ClientError as e:
    print(f"Error fetching log stream information: {e}")
    sequence_token = None

# Prepare your log message
message = 'This is a test log message'
timestamp = int(round(time.time() * 1000))  # Current time in milliseconds

# Put the log event
put_event_args = {
    'logGroupName': log_group_name,
    'logStreamName': log_stream_name,
    'logEvents': [
        {
            'timestamp': timestamp,
            'message': message
        },
    ],
}

if sequence_token:
    put_event_args['sequenceToken'] = sequence_token

try:
    response = client.put_log_events(**put_event_args)
    print("Test Log event submitted successfully.")
except ClientError as e:
    print(f"Failed to submit test log event: {e}")
