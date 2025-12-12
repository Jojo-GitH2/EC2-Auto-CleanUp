import boto3
import config
from datetime import datetime, timezone


def scan_stopped_instances():
    try:
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for stopped EC2 instances...")

        response = ec2_client.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
        )
        stopped_instances = response["Reservations"]
        if not stopped_instances:
            print("No stopped instances found.")
            return

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
                        print(
                            f"ACTION REQUIRED: Instance {instance_id} has been stopped for {hours_stopped:.2f} hours."
                        )
                        terminate_instance(instance_id)
                else:
                    stop_date = "N/A"
                # print(
                #     f"Instance ID: {instance_id}, Stop Date: {stop_date}, Current Time: {current_time}, Delta: {delta.days} days {delta.seconds // 3600} hours {delta.seconds // 60 % 60} minutes {delta.seconds % 60} seconds"
                # )

    except Exception as e:
        print(f"Error scanning instances: {e}")


def terminate_instance(instance_id):
    try:
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        if config.DRY_RUN:
            print(f"DRY RUN: Would Terminate instance {instance_id}")
        else:
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Terminated instance {instance_id}")
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {e}")
