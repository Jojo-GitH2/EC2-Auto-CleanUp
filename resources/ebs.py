import boto3, config
from datetime import datetime, timezone


def cleanup_unattached_volumes():
    try:
        report = []
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for unattached volumes...")
        response = ec2_client.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )

        unattached_volumes = response["Volumes"]
        if not unattached_volumes:
            print("No unattached volumes found.")
            return report

        for volume in unattached_volumes:
            volume_id = volume["VolumeId"]
            size = volume["Size"]
            CreateTime = volume["CreateTime"]

            elasped_hours = int(
                (
                    datetime.now(timezone.utc) - CreateTime.replace(tzinfo=timezone.utc)
                ).total_seconds()
                / 3600
            )
            # if elasped_hours < config.STOPPED_HOURS_THRESHOLD:
            #     print(
            #         f"Skipping volume {volume_id} created at {CreateTime.strftime('%Y-%m-%d %H:%M:%S')}, within threshold."
            #     )
            #     continue

            message = (
                f"ACTION REQUIRED: Volume {volume_id} is unattached. Size: {size} GiB"
            )
            report.append(message)
            print(message)

            if config.DRY_RUN:
                action_message = (
                    f"DRY RUN: Would delete volume {volume_id} of size {size} GiB"
                )
                report.append(action_message)
                print(action_message)
            else:
                ec2_client.delete_volume(VolumeId=volume_id)
                action_message = f"Deleted volume {volume_id} of size {size} GiB"
                report.append(action_message)
                print(action_message)
    except Exception as e:
        error_message = f"Error cleaning up volumes: {e}"
        print(error_message)
        report.append(error_message)

    return report
