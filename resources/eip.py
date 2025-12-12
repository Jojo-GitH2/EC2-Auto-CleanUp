import boto3, config


def release_unused_ips():
    try:
        report = []
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for unattached Elastic IPs...")
        response = ec2_client.describe_addresses()

        unattached_ips = [
            address
            for address in response["Addresses"]
            if "AssociationId" not in address
        ]

        if not unattached_ips:
            print("No unattached Elastic IPs found.")
            return

        for address in unattached_ips:
            allocation_id = address["AllocationId"]
            public_ip = address["PublicIp"]
            message = f"ACTION REQUIRED: Elastic IP {public_ip} is unattached."
            report.append(message)
            print(message)

            if config.DRY_RUN:
                action_message = f"DRY RUN: Would release Elastic IP {public_ip} (AllocationId: {allocation_id})"
                report.append(action_message)
                print(action_message)
            else:
                ec2_client.release_address(AllocationId=allocation_id)
                action_message = f"Released Elastic IP {public_ip})"
                report.append(action_message)
                print(action_message)
    except Exception as e:
        error_message = f"Error releasing unattached Elastic IPs: {e}"
        print(error_message)
        report.append(error_message)

    return report
