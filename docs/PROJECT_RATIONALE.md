# Project Rationale

## Overview

DriftGuard was built to solve a common operational problem in Infrastructure as Code (IaC) environments—**Infrastructure Drift**.

Infrastructure drift occurs when cloud resources managed by Terraform are modified directly through the cloud provider instead of through Terraform itself. These unmanaged changes create inconsistencies between the infrastructure defined in Terraform and the infrastructure actually running in production.

Although Terraform provides mechanisms such as state refresh and resource import, these commands are designed for state management rather than operational drift analysis.

DriftGuard was created as a **read-only Infrastructure Drift Detection Engine** that allows engineers to inspect and understand configuration changes before deciding whether those changes should be accepted or reverted.

---

# Problem Statement

Infrastructure managed through Terraform is expected to be modified exclusively using Infrastructure as Code.

In real production environments, however, manual changes frequently occur due to:

- Emergency production fixes
- Security incident response
- Temporary operational changes
- Human error
- Direct console access
- CLI or SDK automation

These changes introduce infrastructure drift.

Examples include:

- Changing an EC2 instance type
- Opening a Security Group to the Internet
- Disabling S3 encryption
- Modifying IAM configurations
- Updating network settings

Without proper visibility, these changes may remain undetected until they cause deployment failures, compliance violations, or security incidents.

---

# Existing Terraform Approaches

Terraform already provides commands that interact with infrastructure state.

However, these commands solve different problems.

---

## Terraform Import

`terraform import` is designed to bring existing unmanaged resources under Terraform management.

### Advantages

- Imports existing infrastructure into Terraform State
- Enables Terraform to manage previously unmanaged resources

### Limitations

- Requires importing each resource individually
- Requires resource identifiers for every import operation
- Updates Terraform State during the import process
- Intended for resource adoption rather than drift analysis
- Time-consuming in environments containing dozens or hundreds of resources

For large infrastructures, repeatedly importing resources simply to inspect configuration changes is inefficient.

---

## Terraform Refresh

Terraform refresh synchronizes the Terraform State with the current infrastructure.

### Advantages

- Updates Terraform State to reflect the live cloud environment
- Keeps Terraform State synchronized

### Limitations

- Modifies the Terraform State
- Accepts manual infrastructure changes into the state
- Removes the opportunity to inspect differences before synchronization
- Does not produce a dedicated drift analysis report

In environments where manual changes should be investigated before being accepted, state refresh is not an ideal solution.

---

# Why DriftGuard?

DriftGuard was designed around a different philosophy.

Instead of modifying Terraform State, it performs a **read-only comparison** between:

- Expected infrastructure stored in `terraform.tfstate`
- Actual infrastructure retrieved directly from AWS APIs

The project never changes:

- Terraform configuration
- Terraform State
- Cloud infrastructure

Instead, it reports the detected differences and allows engineers to decide the appropriate remediation strategy.

---

# Design Goals

The primary design objectives of DriftGuard are:

- Read-only infrastructure analysis
- No modification of Terraform State
- No modification of cloud resources
- Modular architecture
- Resource-specific drift detection
- Cloud-provider extensibility
- Production-oriented implementation
- Easy integration with additional AWS services

---

# Why Resource-Level Detection?

Production environments often contain hundreds or thousands of cloud resources.

Scanning every resource during every investigation is inefficient.

DriftGuard allows engineers to:

- Select a resource type
- Select a specific resource
- Scan every resource of the selected type when required

This targeted approach reduces execution time while making investigations more focused.

---

# Current Supported Resources

Current implementation supports:

- Amazon EC2
- AWS Security Groups
- Amazon S3

Each resource has its own:

- Scanner
- Drift Engine
- Comparison Logic

This modular architecture allows additional resource types to be added without affecting existing implementations.

---

# Future Vision

DriftGuard is designed to evolve beyond AWS.

Future releases are planned to support:

- Microsoft Azure
- Google Cloud Platform

Additional AWS services include:

- IAM
- VPC
- Route Tables
- Network ACLs
- RDS
- Load Balancers
- EKS
- Lambda
- DynamoDB

---

# Conclusion

DriftGuard was developed to provide engineers with visibility into infrastructure drift without modifying Terraform State or cloud resources.

Rather than replacing Terraform, DriftGuard complements existing Infrastructure as Code workflows by providing a dedicated drift analysis layer that enables informed operational decisions before reconciliation occurs.
