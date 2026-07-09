class S3DriftEngine:

    def normalize(self, value):
        if value in ("", [], {}, None):
            return False
        return value

    def check_core_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        # Encryption
        expected_encryption = False
        if attributes.get("server_side_encryption_configuration"):
            expected_encryption = True

        actual_encryption = self.normalize(actual.get("encryption"))

        if expected_encryption != actual_encryption:
            drift_report.append(
                {
                    "field": "encryption",
                    "expected": expected_encryption,
                    "actual": actual_encryption,
                    "severity": "CRITICAL",
                    "issue": "S3 bucket encryption changed",
                }
            )

        # Versioning
        expected_versioning = False
        versioning_config = attributes.get("versioning", [])

        if versioning_config:
            expected_versioning = versioning_config[0].get("enabled", False)

        actual_versioning = actual.get("versioning", False)
        actual_versioning = self.normalize(actual_versioning)

        if expected_versioning != actual_versioning:
            drift_report.append(
                {
                    "field": "versioning",
                    "expected": expected_versioning,
                    "actual": actual_versioning,
                    "severity": "HIGH",
                    "issue": "S3 bucket versioning changed",
                }
            )

        # print("\nEXPECTED ENCRYPTION")
        # print(expected_encryption)

        # print("ACTUAL ENCRYPTION")
        # print(actual_encryption)

        # print("\nEXPECTED VERSIONING")
        # print(expected_versioning)

        # print("ACTUAL VERSIONING")
        # print(actual_versioning)
        return drift_report

    def check_public_access_drift(self, expected, actual):
        drift_report = []

        # Default secure configuration assumption
        expected_public_access = {
            "block_public_acls": True,
            "ignore_public_acls": True,
            "block_public_policy": True,
            "restrict_public_buckets": True,
        }

        actual_public_access = actual.get("public_access_block", {})

        if expected_public_access != actual_public_access:
            drift_report.append(
                {
                    "field": "public_access_block",
                    "expected": expected_public_access,
                    "actual": actual_public_access,
                    "severity": "CRITICAL",
                    "issue": "S3 public access configuration changed",
                }
            )
        # print("\nEXPECTED PUBLIC ACCESS")
        # print(expected_public_access)

        # print("ACTUAL PUBLIC ACCESS")
        # print(actual_public_access)
        return drift_report

    def check_config_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        expected_tags = attributes.get("tags", {})
        actual_tags = actual.get("tags", {})

        if expected_tags != actual_tags:
            drift_report.append(
                {
                    "field": "tags",
                    "expected": expected_tags,
                    "actual": actual_tags,
                    "severity": "LOW",
                    "issue": "S3 bucket tags changed",
                }
            )

        return drift_report

    def compare_s3(self, expected, actual):
        drift_report = []

        if actual is None:
            drift_report.append(
                {
                    "field": "resource",
                    "expected": "exists",
                    "actual": "missing",
                    "severity": "CRITICAL",
                    "issue": "S3 bucket deleted",
                }
            )
            return drift_report

        drift_report.extend(self.check_core_drift(expected, actual))
        drift_report.extend(self.check_public_access_drift(expected, actual))
        drift_report.extend(self.check_config_drift(expected, actual))

        return drift_report
