import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')

# SNS Topic ARN     
    sns_topic_arn = 'arn:aws:sns:ap-south-1:160885279989:snapshot-deletion-alerts:b7dba40c-ed04-4723-a802-9195d9052bbc'

    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active EC2 instance IDs
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Function to send SNS notification
    def send_sns_notification(message):
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject="EBS Snapshot Deletion Notification"
        )
        print(f"Notification sent: {message}")

    # Iterate through each snapshot and delete if it's not attached to any volume or the volume is not attached to a running instance
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Delete the snapshot if it's not attached to any volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            message = f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume."
            print(message)
            send_sns_notification(message)
        else:
            # Check if the volume still exists
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    message = f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance."
                    print(message)
                    send_sns_notification(message)
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    # The volume associated with the snapshot is not found (it might have been deleted)
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    message = f"Deleted EBS snapshot {snapshot_id} as its associated volume was not found."
                    print(message)
                    send_sns_notification(message)
