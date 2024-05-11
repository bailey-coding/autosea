import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import time
import re
import socket

# Load environment variables
load_dotenv('./data/.env')


# Specify the name of your Log Group and Log Stream
log_group_name = os.getenv('ANALYTICS_GROUP')
log_stream_name = os.getenv('ANALYTICS_STREAM')
aws_region = os.getenv('AWS_REGION')
aws_profile = os.getenv('AWS_PROFILE')
get_user_arn = boto3.client('sts').get_caller_identity().get('Arn') 
get_username = re.search(r'/([^/]*)$', get_user_arn).group(1)
get_hostinfo = os.uname
log_string = f"User: {get_username} - Region: {aws_region} - Profile: {aws_profile}"
print(socket.gethostbyname(socket.gethostname()))

## Get the sequence token (required for existing log streams with events)
#try:
#    response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
#    sequence_token = response['logStreams'][0].get('uploadSequenceToken')
#except ClientError as e:
#    print(f"Error fetching log stream information: {e}")
#    sequence_token = None
#
## Prepare your log message
#message = "Message goes here"
#timestamp = int(round(time.time() * 1000))  # Current time in milliseconds
#
## Put the log event
#put_event_args = {
#    'logGroupName': log_group_name,
#    'logStreamName': log_stream_name,
#    'logEvents': [
#        {
#            'timestamp': timestamp,
#            'message': message
#        },
#    ],
#}
#
#if sequence_token:
#    put_event_args['sequenceToken'] = sequence_token
#    response = client.put_log_events(**put_event_args)