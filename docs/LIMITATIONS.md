# Limitations

## Overview

DriftGuard is designed as a production-oriented Infrastructure Drift Detection Engine for Terraform-managed cloud infrastructure.

While the current implementation provides accurate drift detection for supported AWS resources, several limitations exist due to the current project scope and design choices.

These limitations are intentionally documented to provide transparency and define future improvement opportunities.

---

# Current Limitations

## AWS Only

Current implementation supports only Amazon Web Services (AWS).

Supported resources include:

- Amazon EC2
- AWS Security Groups
- Amazon S3

Support for Microsoft Azure and Google Cloud Platform is planned for future releases.

---

## Limited AWS Resource Coverage

Only selected AWS resources are currently supported.

Resources such as:

- VPC
- IAM
- Route Tables
- Network ACLs
- Elastic Load Balancers
- Auto Scaling Groups
- RDS
- Lambda

are not yet implemented.

---

## Terraform State Dependency

DriftGuard relies on an existing Terraform State (`terraform.tfstate`) file.

If the state file is:

- missing
- corrupted
- outdated

drift analysis may be incomplete or inaccurate.

---

## Local State Files

Current implementation analyzes local Terraform State files only.

Remote backends such as:

- Amazon S3
- Azure Blob Storage
- Terraform Cloud
- HashiCorp HCP Terraform

are not directly supported.

Users must first obtain the state file before running DriftGuard.

---

# Technical Limitations

## Read-Only Analysis

DriftGuard intentionally does **not** modify:

- Terraform Configuration
- Terraform State
- Cloud Infrastructure

Although this improves operational safety, remediation must still be performed manually using Terraform or cloud-native tooling.

---

## Manual Execution

DriftGuard is currently executed manually through the CLI.

It does not yet support:

- Scheduled scans
- Continuous monitoring
- Event-driven execution
- Background scanning

---

## Single Cloud Account

Current implementation scans resources from one configured AWS account at a time.

Cross-account drift analysis is not yet supported.

---

## Region Scope

DriftGuard operates within the configured AWS region.

Multi-region scanning is currently outside the project scope.

---

## Console Reporting

Results are displayed in the terminal.

Report formats such as:

- HTML
- JSON
- CSV
- PDF

are planned for future versions.

---

# Performance Considerations

## Sequential Resource Scanning

Resources are currently scanned sequentially.

Large infrastructures containing hundreds or thousands of resources may experience longer execution times.

Future versions may introduce parallel scanning to improve performance.

---

## AWS API Rate Limits

DriftGuard relies on AWS APIs through Boto3.

Large scans may be affected by AWS service rate limits depending on account configuration and resource count.

---

# Design Trade-offs

Several architectural decisions were made intentionally.

## No Automatic Remediation

DriftGuard reports drift but never attempts to correct it.

This design prevents accidental infrastructure modifications and allows engineers to investigate changes before deciding on remediation.

---

## Resource-Level Scanning

Users explicitly select the resource type to analyze.

Although scanning the entire infrastructure automatically could be implemented, resource-level analysis reduces execution time and unnecessary API requests.

---

## Terraform State as Source of Truth

The current implementation considers the Terraform State to be the expected infrastructure state.

If the Terraform State itself is outdated or incorrect, DriftGuard will compare against that state.

Maintaining an accurate Terraform State remains the responsibility of the infrastructure team.

---

# Future Improvements

The following enhancements are planned to address current limitations:

- Remote Backend Support
- Multi-Region Scanning
- Multi-Account Support
- Parallel Resource Scanning
- Azure Support
- Google Cloud Platform Support
- HTML Report Generation
- JSON Export
- Scheduled Drift Detection
- Notification Integrations
- Web Dashboard
- REST API

---

# Conclusion

The current version of DriftGuard focuses on providing safe, accurate, and production-oriented drift detection for selected Terraform-managed AWS resources.

Its intentionally modular architecture allows future capabilities to be added incrementally while maintaining a clear separation between infrastructure parsing, cloud scanning, drift analysis, and reporting.
