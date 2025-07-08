#!/usr/bin/env python3
import argparse
import shlex
import subprocess
from botocore.session import Session
from multiprocessing import Process
from pprint import pprint
from time import sleep


# Create CloudWatchLogs client
cw_logs = Session().create_client('logs')

# Define Argument Parser
parser = argparse.ArgumentParser(
    prog='send_message',
    description='Sends a message to your Lambda Producer\'s endpoint'
)

# Add arguments
parser.add_argument(
    "--name",
    help="Enter your name, e.g. John, Damian, Yussef",
    type=str)
parser.add_argument(
    "--superpower",
    help="Enter you superpower, e.g. flight, super-strength, observability",
    type=str)

# Get user arguments
args = parser.parse_args()
name = args.name
superpower = args.superpower


# Get API Gateway URL from TF outputs
def get_url():
    return subprocess.run(
        shlex.split(
            "terraform output -raw base_url"),
        stdout=subprocess.PIPE,
        text=True
    ).stdout

# Get Log Group ARN from TF outputs
def get_log_group_arn(service):
    arn = [subprocess.run(
        shlex.split(
            f"terraform output -raw {service}_log_group_arn"),
        stdout=subprocess.PIPE,
        text=True
    ).stdout]
    
    return arn

# Run start_live_tail command on CloudWatchLogs client
# Save output to (producer|consumer).logs file
def start_live_tail(service):
    lg_arn = get_log_group_arn(service)
    
    # Get response object using Log Group ARN
    response = cw_logs.start_live_tail(logGroupIdentifiers=lg_arn)

    # Get EventStream object from response
    event_stream = response['responseStream']

    # Get and print events from `sessionResults` list
    with open(f'{service}.logs', 'a') as logger:
        for event_grp in event_stream:
            if 'sessionUpdate' in event_grp.keys():
                if len(event_grp['sessionUpdate']['sessionResults']) > 0:
                    for event in event_grp['sessionUpdate']['sessionResults']:
                        pprint(event, stream=logger)
                        print('\n', file=logger)

# Run start_live_tail in parallel in the background
# for both the producer and consumer functions
def runInParallel():
    proc = []
    for service in ['producer', 'consumer']:
        p = Process(target=start_live_tail, args=(service,), name=service)
        p.start()
        proc.append(p)


# Get URL for curl command, and defind curl command
curl_target = get_url()

# Define curl command
request = f"curl -d '{{ \"name\": \"{ name }\", \"superpower\": \"{ superpower }\" }}' { curl_target }"

# Start background processes
runInParallel()

# Curl message `count` times
count = 1000
while count > 0:
    count -= 1
    
    response = subprocess.run(
        shlex.split(request),
        stdout=subprocess.PIPE,
        text=True
    ).stdout

    with open('response.logs', 'a') as response_logger:
        print(response, file=response_logger)
        print(f"{ count } calls left", file=response_logger)

    sleep(1)
