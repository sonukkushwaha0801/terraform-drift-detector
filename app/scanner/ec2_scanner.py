import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class EC2Scanner:
    def __init__(self, region="ap-south-1"):
        self.region = region
        self.ec2_client = boto3.client("ec2", region_name=self.region)

    def get_instance_details(self, instance_id):
        """
        Fetch EC2 instance details from AWS.
        """
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])

            reservations = response.get("Reservations", [])

            if not reservations:
                return None

            instance = reservations[0]["Instances"][0]

            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}

            security_group_ids = [
                sg["GroupId"] for sg in instance.get("SecurityGroups", [])
            ]

            return {
                "instance_id": instance.get("InstanceId"),
                "instance_type": instance.get("InstanceType"),
                "state": instance.get("State", {}).get("Name"),
                "public_ip": instance.get("PublicIpAddress"),
                "security_group_ids": security_group_ids,
                "tags": tags,
            }

        except NoCredentialsError:
            print("[ERROR] AWS credentials not found.")
            return None

        except ClientError as error:
            error_code = error.response["Error"]["Code"]

            if error_code == "InvalidInstanceID.NotFound":
                print(f"[ERROR] Instance not found: {instance_id}")
                return None

            print(f"[ERROR] AWS API Error: {error}")
            return None
