import boto3
import config
from datetime import datetime, timezone


def scan_stopped_instances():
    try:
        report = []
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for stopped EC2 instances...")

        response = ec2_client.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
        )
        stopped_instances = response["Reservations"]
        if not stopped_instances:
            print("No stopped instances found.")
            return report

        for reservation in stopped_instances:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                state_transition = (
                    instance["StateTransitionReason"]
                    if "StateTransitionReason" in instance
                    else "N/A"
                )
                date_info = state_transition.split("(")
                if len(date_info) > 1:
                    date_info = date_info[1].split(")")[0]
                    stop_date = datetime.strptime(
                        date_info, "%Y-%m-%d %H:%M:%S %Z"
                    ).replace(tzinfo=timezone.utc)
                    current_time = datetime.now(timezone.utc)
                    delta = current_time - stop_date
                    hours_stopped = delta.total_seconds() / 3600
                    if hours_stopped > config.STOPPED_HOURS_THRESHOLD:

                        message = f"ACTION REQUIRED: Instance {instance_id} has been stopped for {hours_stopped:.2f} hours."
                        report.append(message)

                        action_message = terminate_instance(instance_id)
                        report.append(action_message)
                else:
                    stop_date = "N/A"

    except Exception as e:
        error_message = f"Error scanning instances: {e}"
        print(error_message)
        report.append(error_message)

    return report


def terminate_instance(instance_id):
    try:
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        if config.DRY_RUN:
            message = f"DRY RUN: Would Terminate instance {instance_id}"
            print(message)
            return message
        else:
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            message = f"Terminated instance {instance_id}"
            print(message)
            return message
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {e}")
