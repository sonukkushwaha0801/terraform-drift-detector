class DriftEngine:

    def normalize(self, value):
        if value in ("", [], {}):
            return None
        return value

    def check_compute_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        # Instance Type
        expected_instance_type = self.normalize(attributes.get("instance_type"))
        actual_instance_type = self.normalize(actual.get("instance_type"))

        if expected_instance_type != actual_instance_type:
            drift_report.append(
                {
                    "field": "instance_type",
                    "expected": expected_instance_type,
                    "actual": actual_instance_type,
                    "severity": "HIGH",
                    "issue": "EC2 instance type changed",
                }
            )

        # AMI
        expected_ami = self.normalize(attributes.get("ami"))
        actual_ami = self.normalize(actual.get("ami"))

        if expected_ami != actual_ami:
            drift_report.append(
                {
                    "field": "ami",
                    "expected": expected_ami,
                    "actual": actual_ami,
                    "severity": "HIGH",
                    "issue": "EC2 AMI changed",
                }
            )

        # Instance State
        expected_state = self.normalize(attributes.get("instance_state"))
        actual_state = self.normalize(actual.get("state"))

        if expected_state != actual_state:
            drift_report.append(
                {
                    "field": "instance_state",
                    "expected": expected_state,
                    "actual": actual_state,
                    "severity": "MEDIUM",
                    "issue": "EC2 instance state changed",
                }
            )

        return drift_report

    def check_storage_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        expected_root = attributes.get("root_block_device", [])
        actual_root = actual.get("root_block_device")

        if not expected_root or not actual_root:
            return drift_report

        expected_root = expected_root[0]

        fields = [
            ("device_name", "HIGH"),
            ("volume_size", "HIGH"),
            ("volume_type", "HIGH"),
            ("encrypted", "CRITICAL"),
            ("iops", "MEDIUM"),
            ("throughput", "MEDIUM"),
        ]

        for field, severity in fields:
            expected_value = self.normalize(expected_root.get(field))
            actual_value = self.normalize(actual_root.get(field))

            if expected_value != actual_value:
                drift_report.append(
                    {
                        "field": f"root_block_device.{field}",
                        "expected": expected_value,
                        "actual": actual_value,
                        "severity": severity,
                        "issue": f"Root volume {field} changed",
                    }
                )

        return drift_report

    def check_security_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        # Security Groups
        expected_sg = self.normalize(
            sorted(attributes.get("vpc_security_group_ids", []))
        )
        actual_sg = self.normalize(sorted(actual.get("security_group_ids", [])))

        if expected_sg != actual_sg:
            drift_report.append(
                {
                    "field": "security_groups",
                    "expected": expected_sg,
                    "actual": actual_sg,
                    "severity": "CRITICAL",
                    "issue": "Security groups changed",
                }
            )

        # Key Pair
        expected_key = self.normalize(attributes.get("key_name"))
        actual_key = self.normalize(actual.get("key_name"))

        if expected_key != actual_key:
            drift_report.append(
                {
                    "field": "key_name",
                    "expected": expected_key,
                    "actual": actual_key,
                    "severity": "MEDIUM",
                    "issue": "EC2 key pair changed",
                }
            )

        # Termination Protection
        expected_term = self.normalize(attributes.get("disable_api_termination"))
        actual_term = self.normalize(actual.get("disable_api_termination"))

        if expected_term != actual_term:
            drift_report.append(
                {
                    "field": "disable_api_termination",
                    "expected": expected_term,
                    "actual": actual_term,
                    "severity": "HIGH",
                    "issue": "Termination protection changed",
                }
            )

        # Metadata Options
        expected_meta = attributes.get("metadata_options", [])
        actual_meta = actual.get("metadata_options", {})

        if expected_meta:
            expected_meta = expected_meta[0]

            expected_http_tokens = expected_meta.get("http_tokens")
            actual_http_tokens = actual_meta.get("HttpTokens")

            if expected_http_tokens != actual_http_tokens:
                drift_report.append(
                    {
                        "field": "metadata_options.http_tokens",
                        "expected": expected_http_tokens,
                        "actual": actual_http_tokens,
                        "severity": "HIGH",
                        "issue": "Metadata options changed",
                    }
                )

        return drift_report

    def check_network_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        fields = [
            ("subnet_id", "HIGH"),
            ("private_ip", "MEDIUM"),
            ("public_ip", "MEDIUM"),
            ("source_dest_check", "HIGH"),
        ]

        for field, severity in fields:
            expected_value = self.normalize(attributes.get(field))
            actual_value = self.normalize(actual.get(field))

            if expected_value != actual_value:
                drift_report.append(
                    {
                        "field": field,
                        "expected": expected_value,
                        "actual": actual_value,
                        "severity": severity,
                        "issue": f"EC2 {field} changed",
                    }
                )

        return drift_report

    def check_config_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        # Monitoring
        expected_monitoring = self.normalize(attributes.get("monitoring"))
        actual_monitoring = actual.get("monitoring") == "enabled"

        if expected_monitoring != actual_monitoring:
            drift_report.append(
                {
                    "field": "monitoring",
                    "expected": expected_monitoring,
                    "actual": actual_monitoring,
                    "severity": "LOW",
                    "issue": "EC2 monitoring changed",
                }
            )

        # Tags
        expected_tags = self.normalize(attributes.get("tags"))
        actual_tags = self.normalize(actual.get("tags"))

        if expected_tags != actual_tags:
            drift_report.append(
                {
                    "field": "tags",
                    "expected": expected_tags,
                    "actual": actual_tags,
                    "severity": "LOW",
                    "issue": "EC2 tags changed",
                }
            )

        return drift_report

    def compare_ec2(self, expected, actual):
        drift_report = []

        if actual is None:
            drift_report.append(
                {
                    "field": "resource",
                    "expected": "exists",
                    "actual": "missing",
                    "severity": "CRITICAL",
                    "issue": "EC2 instance deleted",
                }
            )
            return drift_report

        drift_report.extend(self.check_compute_drift(expected, actual))
        drift_report.extend(self.check_storage_drift(expected, actual))
        drift_report.extend(self.check_security_drift(expected, actual))
        drift_report.extend(self.check_network_drift(expected, actual))
        drift_report.extend(self.check_config_drift(expected, actual))

        return drift_report
