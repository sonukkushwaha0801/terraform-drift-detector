import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class S3Scanner:
    def __init__(self, region="ap-south-1"):
        self.region = region
        self.s3_client = boto3.client("s3", region_name=self.region)

    def normalize_bool(self, value):
        if value in ("", [], {}, None):
            return False
        return bool(value)

    def get_bucket_encryption(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            rules = response["ServerSideEncryptionConfiguration"]["Rules"]

            return True if rules else False

        except ClientError:
            return False

    def get_bucket_versioning(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_versioning(Bucket=bucket_name)

            status = response.get("Status", "Disabled")
            return status == "Enabled"

        except ClientError:
            return False

    def get_public_access_block(self, bucket_name):
        try:
            response = self.s3_client.get_public_access_block(Bucket=bucket_name)

            config = response.get("PublicAccessBlockConfiguration", {})

            return {
                "block_public_acls": self.normalize_bool(config.get("BlockPublicAcls")),
                "ignore_public_acls": self.normalize_bool(
                    config.get("IgnorePublicAcls")
                ),
                "block_public_policy": self.normalize_bool(
                    config.get("BlockPublicPolicy")
                ),
                "restrict_public_buckets": self.normalize_bool(
                    config.get("RestrictPublicBuckets")
                ),
            }

        except ClientError:
            return {
                "block_public_acls": False,
                "ignore_public_acls": False,
                "block_public_policy": False,
                "restrict_public_buckets": False,
            }

    def get_bucket_tags(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)

            return {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}

        except ClientError:
            return {}

    def get_bucket_details(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)

            return {
                "bucket_name": bucket_name,
                "encryption": self.get_bucket_encryption(bucket_name),
                "versioning": self.get_bucket_versioning(bucket_name),
                "public_access_block": self.get_public_access_block(bucket_name),
                "tags": self.get_bucket_tags(bucket_name),
            }

        except NoCredentialsError:
            print("[ERROR] AWS credentials not found.")
            return None

        except ClientError:
            print(f"[ERROR] Bucket not found: {bucket_name}")
            return None
