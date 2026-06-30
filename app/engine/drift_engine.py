class DriftEngine:
    def compare_ec2(self, expected, actual):
        """
        Compare expected EC2 state vs actual AWS state.
        """

        drift_report = []

        # Resource missing
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

        expected_attributes = expected.get("attributes", {})

        # Instance type drift
        expected_instance_type = expected_attributes.get("instance_type")
        actual_instance_type = actual.get("instance_type")

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

        # Instance state drift
        actual_state = actual.get("state")

        if actual_state != "running":
            drift_report.append(
                {
                    "field": "state",
                    "expected": "running",
                    "actual": actual_state,
                    "severity": "MEDIUM",
                    "issue": "EC2 state changed",
                }
            )

        return drift_report
