import argparse
import sys

from app.parser.tfstate_parser import TFStateParser
from app.scanner.ec2_scanner import EC2Scanner
from app.engine.drift_engine import DriftEngine
from app.report.report_generator import ReportGenerator
from app.scanner.sg_scanner import SGScanner
from app.engine.sg_drift_engine import SGDriftEngine


def display_resources(resources):
    """
    Display resources.
    Show resource ID only if duplicate names exist.
    """
    resource_names = [resource["name"] for resource in resources]
    has_duplicates = len(resource_names) != len(set(resource_names))

    for index, resource in enumerate(resources, start=1):
        if has_duplicates:
            print(f"{index}. {resource['name']} " f"({resource['resource_id']})")
        else:
            print(f"{index}. {resource['name']}")


def select_resource(resources):
    """
    Handle resource selection.
    """
    resource_count = len(resources)

    if resource_count == 0:
        print("\n[ERROR] No matching resources found in tfstate.")
        sys.exit(1)

    if resource_count == 1:
        selected = resources[0]
        print(f"\n[INFO] Found 1 matching resource: {selected['name']}")
        return selected

    print(f"\n[INFO] Found {resource_count} matching resources:\n")

    display_resources(resources)

    print(f"{resource_count + 1}. Scan All Resources")
    print("0. Exit")

    while True:
        try:
            choice = int(input("\nSelect option: "))

            if choice == 0:
                print("[INFO] Exiting...")
                sys.exit(0)

            elif 1 <= choice <= resource_count:
                selected = resources[choice - 1]
                print(f"\n[INFO] Selected resource: {selected['name']}")
                return selected

            elif choice == resource_count + 1:
                print("\n[INFO] Starting bulk drift detection...")
                return resources

            else:
                print("[ERROR] Invalid selection.")

        except ValueError:
            print("[ERROR] Please enter a valid number.")


def run_ec2_drift(selected_resources):
    """
    Execute EC2 drift detection pipeline.
    """
    scanner = EC2Scanner()
    drift_engine = DriftEngine()
    reporter = ReportGenerator()

    # Bulk scan
    if isinstance(selected_resources, list):
        for resource in selected_resources:
            print(f"\nScanning: {resource['name']} ({resource['resource_id']})")

            actual = scanner.get_instance_details(resource["resource_id"])
            drift_report = drift_engine.compare_ec2(resource, actual)
            reporter.generate(drift_report)

    # Single scan
    else:
        actual = scanner.get_instance_details(selected_resources["resource_id"])
        drift_report = drift_engine.compare_ec2(selected_resources, actual)
        reporter.generate(drift_report)


def main():
    parser = argparse.ArgumentParser(description="DriftGuard")

    parser.add_argument("--resource", required=True)
    parser.add_argument("--tfstate", required=True)

    args = parser.parse_args()

    tf_parser = TFStateParser(args.tfstate, args.resource)
    resources = tf_parser.get_resources()

    selected_resources = select_resource(resources)
    # print(selected_resources["attributes"].keys())

    if args.resource == "ec2":
        run_ec2_drift(selected_resources)

    elif args.resource == "security_group":
        run_sg_drift(selected_resources)

    elif args.resource == "s3":
        print("[INFO] S3 drift detection not implemented yet.")


def run_sg_drift(selected_resources):
    """
    Execute Security Group drift detection pipeline.
    """
    scanner = SGScanner()
    drift_engine = SGDriftEngine()
    reporter = ReportGenerator()

    # Bulk scan
    if isinstance(selected_resources, list):
        for resource in selected_resources:
            print(f"\nScanning: {resource['name']} ({resource['resource_id']})")

            actual = scanner.get_security_group_details(resource["resource_id"])

            drift_report = drift_engine.compare_sg(resource, actual)
            reporter.generate(drift_report)

    # Single scan
    else:
        actual = scanner.get_security_group_details(selected_resources["resource_id"])

        drift_report = drift_engine.compare_sg(selected_resources, actual)

        reporter.generate(drift_report)


if __name__ == "__main__":
    main()
