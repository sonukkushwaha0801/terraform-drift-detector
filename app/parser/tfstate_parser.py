import json


class TFStateParser:
    RESOURCE_MAP = {
        "ec2": "aws_instance",
        "security_group": "aws_security_group",
        "s3": "aws_s3_bucket",
    }

    def __init__(self, tfstate_path, selected_resource):
        self.tfstate_path = tfstate_path
        self.selected_resource = selected_resource

    def load_tfstate(self):
        """
        Load Terraform state file.
        """
        try:
            with open(self.tfstate_path, "r") as file:
                data = json.load(file)
            return data

        except FileNotFoundError:
            print(f"[ERROR] File not found: {self.tfstate_path}")
            return None

        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format in tfstate file")
            return None

    def extract_resource_id(self, resource_type, attributes):
        """
        Extract resource ID based on resource type.
        """
        if resource_type == "aws_s3_bucket":
            return attributes.get("bucket")

        return attributes.get("id")

    def get_resources(self):
        """
        Return flattened resource list for selected resource type.
        """
        data = self.load_tfstate()

        if not data:
            return []

        resources = data.get("resources", [])
        target_type = self.RESOURCE_MAP.get(self.selected_resource)

        if not target_type:
            print(f"[ERROR] Unsupported resource type: {self.selected_resource}")
            return []

        matched_resources = []

        for resource in resources:
            if resource.get("type") != target_type:
                continue

            resource_type = resource.get("type")
            resource_name = resource.get("name")
            instances = resource.get("instances", [])

            for instance in instances:
                attributes = instance.get("attributes", {})

                resource_id = self.extract_resource_id(resource_type, attributes)

                matched_resources.append(
                    {
                        "type": resource_type,
                        "name": resource_name,
                        "resource_id": resource_id,
                        "attributes": attributes,
                    }
                )

        return matched_resources
