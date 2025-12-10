import boto3
import config

def scan_stopped_instances():
    try:
        ec2_client = boto3.client('ec2', region_name=config.AWS_REGION)
        print("Scanning for stopped EC2 instances...")

        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name':  'instance-state-name',
                    'Values': ['stopped']
                }
            ],
            MaxResults = 50,
            NextToken = ''
        )
        stopped_instances =response['Reservations']

        for reservation in stopped_instances:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                StateTransition = instance['StateTransitionReason'] if 'StateTransitionReason' in instance else 'N/A'
                print(f"Instance ID: {instance_id}, StateTransition: {StateTransition}")


    except Exception as e:
        print(f"Error scanning instances: {e}")

