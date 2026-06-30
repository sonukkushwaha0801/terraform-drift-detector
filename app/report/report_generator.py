class ReportGenerator:
    def generate(self, drift_report):
        """
        Generate drift report output.
        """

        print("\n" + "=" * 60)
        print("DRIFT REPORT")
        print("=" * 60)

        if not drift_report:
            print("[STATUS] NO DRIFT DETECTED")
            print("=" * 60)
            return

        print("[STATUS] DRIFT DETECTED")
        print()

        for drift in drift_report:
            print(f"Issue    : {drift['issue']}")
            print(f"Field    : {drift['field']}")
            print(f"Expected : {drift['expected']}")
            print(f"Actual   : {drift['actual']}")
            print(f"Severity : {drift['severity']}")
            print("-" * 60)
