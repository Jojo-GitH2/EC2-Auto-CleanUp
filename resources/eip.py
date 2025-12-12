import boto3, config

def check_unattached_ips():
    try:
        ec2_client = boto3.client("ec2", region_name=config.AWS_REGION)
        print("Scanning for unattached Elastic IPs...")
        response = ec2_client.describe_addresses()

        print("Response:", response["Addresses"])  # Debugging line to inspect the response structure

        unattached_ips = [ address for address in response["Addresses"] if "AssociationId" not in address ]

        # unattached_ips = [
        #     address for address in response["Addresses"] if "InstanceId" not in address
        # ]
        if not unattached_ips:
            print("No unattached Elastic IPs found.")
            return

        for address in unattached_ips:
            allocation_id = address["AllocationId"]
            public_ip = address["PublicIp"]
            print(f"ACTION REQUIRED: Elastic IP {public_ip} is unattached.")

            if config.DRY_RUN:
                print(f"DRY RUN: Would release Elastic IP {public_ip} (AllocationId: {allocation_id})")
            else:
                ec2_client.release_address(AllocationId=allocation_id)
                print(f"Released Elastic IP {public_ip} (AllocationId: {allocation_id})")
    except Exception as e:
        print(f"Error checking unattached Elastic IPs: {e}")