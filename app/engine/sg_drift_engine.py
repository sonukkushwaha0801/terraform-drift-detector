class SGDriftEngine:

    def normalize(self, value):
        if value in ("", [], {}):
            return None
        return value

    def normalize_tf_rules(self, rules):
        normalized_rules = []

        for rule in rules:
            protocol = rule.get("protocol")
            from_port = rule.get("from_port")
            to_port = rule.get("to_port")

            if protocol == "-1":
                from_port = 0
                to_port = 0

            if from_port is None:
                from_port = 0

            if to_port is None:
                to_port = 0

            cidr_blocks = rule.get("cidr_blocks", [])

            for cidr in cidr_blocks:
                normalized_rules.append(
                    {
                        "protocol": protocol,
                        "from_port": from_port,
                        "to_port": to_port,
                        "cidr": cidr,
                    }
                )

        return sorted(
            normalized_rules,
            key=lambda x: (
                str(x["protocol"]),
                str(x["from_port"]),
                str(x["to_port"]),
                str(x["cidr"]),
            ),
        )

    def check_basic_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        fields = [("name", "group_name", "LOW"), ("description", "description", "LOW")]

        for expected_field, actual_field, severity in fields:
            expected_value = self.normalize(attributes.get(expected_field))
            actual_value = self.normalize(actual.get(actual_field))

            if expected_value != actual_value:
                drift_report.append(
                    {
                        "field": expected_field,
                        "expected": expected_value,
                        "actual": actual_value,
                        "severity": severity,
                        "issue": f"Security group {expected_field} changed",
                    }
                )

        return drift_report

    def check_rules_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        # Ingress Rules
        expected_ingress = self.normalize_tf_rules(attributes.get("ingress", []))

        actual_ingress = actual.get("ingress_rules", [])

        if expected_ingress != actual_ingress:
            drift_report.append(
                {
                    "field": "ingress_rules",
                    "expected": expected_ingress,
                    "actual": actual_ingress,
                    "severity": "CRITICAL",
                    "issue": "Ingress rules changed",
                }
            )

        # Egress Rules
        expected_egress = self.normalize_tf_rules(attributes.get("egress", []))

        actual_egress = actual.get("egress_rules", [])

        if expected_egress != actual_egress:
            drift_report.append(
                {
                    "field": "egress_rules",
                    "expected": expected_egress,
                    "actual": actual_egress,
                    "severity": "HIGH",
                    "issue": "Egress rules changed",
                }
            )
        print("\nEXPECTED INGRESS")
        print(expected_ingress)

        print("\nACTUAL INGRESS")
        print(actual_ingress)

        print("\nEXPECTED EGRESS")
        print(expected_egress)

        print("\nACTUAL EGRESS")
        print(actual_egress)

        return drift_report

    def check_config_drift(self, expected, actual):
        drift_report = []
        attributes = expected.get("attributes", {})

        expected_tags = self.normalize(attributes.get("tags"))
        actual_tags = self.normalize(actual.get("tags"))

        if expected_tags != actual_tags:
            drift_report.append(
                {
                    "field": "tags",
                    "expected": expected_tags,
                    "actual": actual_tags,
                    "severity": "LOW",
                    "issue": "Security group tags changed",
                }
            )

        return drift_report

    def compare_sg(self, expected, actual):
        drift_report = []

        if actual is None:
            drift_report.append(
                {
                    "field": "resource",
                    "expected": "exists",
                    "actual": "missing",
                    "severity": "CRITICAL",
                    "issue": "Security group deleted",
                }
            )
            return drift_report

        drift_report.extend(self.check_basic_drift(expected, actual))
        drift_report.extend(self.check_rules_drift(expected, actual))
        drift_report.extend(self.check_config_drift(expected, actual))

        return drift_report
