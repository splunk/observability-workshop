#!/usr/bin/env python3
import argparse
import shlex
import subprocess
from multiprocessing import Process
from pprint import pprint
from time import sleep



SERVICES = ("producer", "consumer")


# Get API Gateway URL from TF outputs
def get_url():
    return subprocess.run(
        shlex.split("terraform output -raw base_url"),
        stdout=subprocess.PIPE,
        text=True,
    ).stdout


# Get Log Group ARN from TF outputs
def get_log_group_arn(service):
    arn = [
        subprocess.run(
            shlex.split(f"terraform output -raw {service}_log_group_arn"),
            stdout=subprocess.PIPE,
            text=True,
        ).stdout
    ]

    return arn


# Run start_live_tail command on CloudWatchLogs client
# Save output to (producer|consumer).logs file
def start_live_tail(service):
    from botocore.session import Session

    cw_logs = Session().create_client("logs")
    lg_arn = get_log_group_arn(service)

    # Get response object using Log Group ARN
    response = cw_logs.start_live_tail(logGroupIdentifiers=lg_arn)

    # Get EventStream object from response
    event_stream = response["responseStream"]

    # Get and print events from `sessionResults` list
    with open(f"{service}.logs", "a") as logger:
        for event_grp in event_stream:
            if "sessionUpdate" in event_grp.keys():
                if len(event_grp["sessionUpdate"]["sessionResults"]) > 0:
                    for event in event_grp["sessionUpdate"]["sessionResults"]:
                        pprint(event, stream=logger)
                        print("\n", file=logger)


# Run start_live_tail in parallel in the background
# for both the producer and consumer functions
def run_in_parallel():
    processes = []
    for service in SERVICES:
        process = Process(target=start_live_tail, args=(service,), name=service)
        process.start()
        processes.append(process)

    return processes


def parse_args():
    # Define Argument Parser
    parser = argparse.ArgumentParser(
        prog="send_message",
        description="Sends a message to your Lambda Producer's endpoint",
    )

    # Add arguments
    parser.add_argument(
        "--name",
        help="Enter your name, e.g. John, Damian, Yussef",
        type=str,
    )
    parser.add_argument(
        "--superpower",
        help="Enter you superpower, e.g. flight, super-strength, observability",
        type=str,
    )

    return parser.parse_args()


def send_messages(name, superpower):
    # Get URL for curl command, and define curl command
    curl_target = get_url()

    # Define curl command
    payload = f'{{ "name": "{name}", "superpower": "{superpower}" }}'
    request = f"curl -d {shlex.quote(payload)} {curl_target}"

    # Curl message `count` times
    count = 1000
    while count > 0:
        count -= 1

        response = subprocess.run(
            shlex.split(request),
            stdout=subprocess.PIPE,
            text=True,
        ).stdout

        with open("response.logs", "a") as response_logger:
            print(response, file=response_logger)
            print(f"{count} calls left", file=response_logger)

        sleep(1)


def main():
    args = parse_args()
    processes = run_in_parallel()

    try:
        send_messages(args.name, args.superpower)
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
            process.join(timeout=5)


if __name__ == "__main__":
    main()
