import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class SGScanner:
    def __init__(self, region="ap-south-1"):
        self.region = region
        self.ec2_client = boto3.client("ec2", region_name=self.region)

    def normalize_rule(self, protocol, from_port, to_port):
        """
        Normalize AWS SG rule values for consistent comparison.
        """
        if protocol == "-1":
            from_port = 0
            to_port = 0

        if from_port is None:
            from_port = 0

        if to_port is None:
            to_port = 0

        return protocol, from_port, to_port

    def normalize_rules(self, permissions):
        rules = []

        for permission in permissions:
            protocol = permission.get("IpProtocol")
            from_port = permission.get("FromPort")
            to_port = permission.get("ToPort")

            protocol, from_port, to_port = self.normalize_rule(
                protocol, from_port, to_port
            )

            for ip_range in permission.get("IpRanges", []):
                rules.append(
                    {
                        "protocol": protocol,
                        "from_port": from_port,
                        "to_port": to_port,
                        "cidr": ip_range.get("CidrIp"),
                    }
                )

        return sorted(
            rules,
            key=lambda x: (
                str(x["protocol"]),
                str(x["from_port"]),
                str(x["to_port"]),
                str(x["cidr"]),
            ),
        )

    def get_security_group_details(self, group_id):
        try:
            response = self.ec2_client.describe_security_groups(GroupIds=[group_id])

            security_groups = response.get("SecurityGroups", [])

            if not security_groups:
                return None

            sg = security_groups[0]

            tags = {tag["Key"]: tag["Value"] for tag in sg.get("Tags", [])}

            ingress_rules = self.normalize_rules(sg.get("IpPermissions", []))

            egress_rules = self.normalize_rules(sg.get("IpPermissionsEgress", []))

            return {
                "group_id": sg.get("GroupId"),
                "group_name": sg.get("GroupName"),
                "description": sg.get("Description"),
                "ingress_rules": ingress_rules,
                "egress_rules": egress_rules,
                "tags": tags,
            }

        except NoCredentialsError:
            print("[ERROR] AWS credentials not found.")
            return None

        except ClientError as error:
            error_code = error.response["Error"]["Code"]

            if error_code == "InvalidGroup.NotFound":
                print(f"[ERROR] Security Group not found: {group_id}")
                return None

            print(f"[ERROR] AWS API Error: {error}")
            return None
