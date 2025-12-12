import boto3, config
from datetime import datetime, timezone


def cleanup_unattached_volumes():
    try:
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for unattached volumes...")
        response = ec2_client.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )

        unattached_volumes = response["Volumes"]
        if not unattached_volumes:
            print("No unattached volumes found.")
            return

        for volume in unattached_volumes:
            volume_id = volume["VolumeId"]
            size = volume["Size"]
            CreateTime = volume["CreateTime"]
            # TEST = (
            #     datetime.now(timezone.utc) - CreateTime.replace(tzinfo=timezone.utc)
            # ).total_seconds() / 3600
            if (
                int(
                    (
                        datetime.now(timezone.utc)
                        - CreateTime.replace(tzinfo=timezone.utc)
                    ).total_seconds()
                    / 3600
                )
                < config.STOPPED_HOURS_THRESHOLD
            ):
                print(f"Skipping volume {volume_id} created at {CreateTime.strftime('%Y-%m-%d %H:%M:%S')}, within threshold.")
                continue

            print(
                f"ACTION REQUIRED: Volume {volume_id} is unattached. Size: {size} GiB"
            )

            if config.DRY_RUN:
                print(f"DRY RUN: Would delete volume {volume_id} of size {size} GiB")
            else:
                ec2_client.delete_volume(VolumeId=volume_id)
                print(f"Deleted volume {volume_id} of size {size} GiB")
    except Exception as e:
        print(f"Error cleaning up volumes: {e}")
