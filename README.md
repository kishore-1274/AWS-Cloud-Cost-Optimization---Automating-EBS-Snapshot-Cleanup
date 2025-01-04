# AWS-Cloud-Cost-Optimization---Automating-EBS-Snapshot-Cleanup
Overview:
This project uses AWS Lambda to automatically identify and delete stale EBS snapshots not associated with any active EC2 instances, reducing unnecessary storage costs. Real-time notifications about the deletions are sent via Amazon SNS.

Description:
Lambda Function: Identifies EBS snapshots owned by the account and deletes those not linked to active EC2 instances.
SNS Integration: Sends real-time notifications when a snapshot is deleted, enhancing visibility.



Key Features:
Cost Savings: Automatically deletes unused EBS snapshots to save on storage costs.
Notifications: Uses SNS to notify users about deleted snapshots.
Automation: Automates the cleanup process, improving cloud resource management.



Key Technologies:
AWS Lambda, Amazon EC2, Amazon SNS, boto3 (Python SDK)



Benefits:
Automated Cleanup: Reduces manual intervention in managing cloud resources.
Improved Resource Management: Helps optimize cloud storage costs by removing stale snapshots.
Real-time Insights: Notifications ensure visibility into optimization efforts.
