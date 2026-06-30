import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class EC2Scanner:
    def __init__(self, region="ap-south-1"):
        self.region = region
        self.ec2_client = boto3.client("ec2", region_name=self.region)

    def get_disable_api_termination(self, instance_id):
        """
        Fetch termination protection status.
        """
        try:
            response = self.ec2_client.describe_instance_attribute(
                InstanceId=instance_id, Attribute="disableApiTermination"
            )
            return response["DisableApiTermination"]["Value"]

        except Exception:
            return None

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

            # Tags
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}

            # Security Groups
            security_group_ids = [
                sg["GroupId"] for sg in instance.get("SecurityGroups", [])
            ]

            # IAM Role
            iam_role = None
            if "IamInstanceProfile" in instance:
                iam_role = instance["IamInstanceProfile"].get("Arn")

            # Root Block Device
            root_block_device = None
            block_devices = instance.get("BlockDeviceMappings", [])

            if block_devices:
                root_device = block_devices[0]

                device_name = root_device.get("DeviceName")
                volume_id = root_device.get("Ebs", {}).get("VolumeId")

                volume_details = self.get_volume_details(volume_id)

                root_block_device = {
                    "device_name": device_name,
                    **(volume_details if volume_details else {}),
                }

            # Metadata Options
            metadata_options = instance.get("MetadataOptions", {})

            # Termination Protection
            disable_api_termination = self.get_disable_api_termination(instance_id)

            return {
                # Compute
                "instance_id": instance.get("InstanceId"),
                "instance_type": instance.get("InstanceType"),
                "ami": instance.get("ImageId"),
                "state": instance.get("State", {}).get("Name"),
                # Security
                "security_group_ids": security_group_ids,
                "iam_role": iam_role,
                "key_name": instance.get("KeyName"),
                "metadata_options": metadata_options,
                "disable_api_termination": disable_api_termination,
                # Storage
                "root_block_device": root_block_device,
                # Networking
                "subnet_id": instance.get("SubnetId"),
                "public_ip": instance.get("PublicIpAddress"),
                "private_ip": instance.get("PrivateIpAddress"),
                "source_dest_check": instance.get("SourceDestCheck"),
                # Config
                "monitoring": instance.get("Monitoring", {}).get("State"),
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

    def get_volume_details(self, volume_id):
        """
        Fetch EBS volume details.
        """
        try:
            response = self.ec2_client.describe_volumes(VolumeIds=[volume_id])

            volumes = response.get("Volumes", [])

            if not volumes:
                return None

            volume = volumes[0]

            return {
                "volume_id": volume.get("VolumeId"),
                "volume_size": volume.get("Size"),
                "volume_type": volume.get("VolumeType"),
                "encrypted": volume.get("Encrypted"),
                "iops": volume.get("Iops"),
                "throughput": volume.get("Throughput"),
            }

        except Exception:
            return None


if __name__ == "__main__":
    import json

    with open("main.tfstate", "r") as f:
        data = json.load(f)

    print(data["resources"])
    contain = EC2Scanner().get_instance_details(data)
    print(contain)
