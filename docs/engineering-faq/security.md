# Security Engineering FAQ

## Overview

This document answers security-related questions about DriftGuard, including its design principles, AWS permissions, operational safety, and production deployment considerations.

---

# Read-Only Security

## 1. Is DriftGuard safe to run in production?

Yes.

DriftGuard is designed as a read-only analysis tool.

It only retrieves infrastructure information from AWS APIs and never modifies cloud resources or Terraform State.

---

## 2. Can DriftGuard accidentally modify AWS resources?

No.

The application only uses AWS read operations through Boto3.

No Create, Update, Delete, or Modify API calls are performed.

---

## 3. Can DriftGuard modify Terraform State?

No.

Terraform State is opened in read-only mode.

DriftGuard never executes Terraform commands such as:

- terraform apply
- terraform destroy
- terraform refresh
- terraform import

---

## 4. Why was a read-only architecture chosen?

Infrastructure remediation is a business decision.

Automatically changing production infrastructure may introduce outages.

DriftGuard intentionally separates **detection** from **remediation**, allowing engineers to review drift before taking action.

---

## 5. Can DriftGuard delete AWS resources?

No.

There is no deletion logic implemented anywhere in the project.

---

# AWS Permissions

## 6. What AWS permissions does DriftGuard require?

Only read-only IAM permissions.

Examples include:

- ec2:DescribeInstances
- ec2:DescribeSecurityGroups
- s3:GetBucketVersioning
- s3:GetBucketEncryption
- s3:GetPublicAccessBlock
- s3:GetBucketTagging

No write permissions are required.

---

## 7. Why follow the Principle of Least Privilege?

Granting only read permissions reduces the attack surface and prevents accidental infrastructure modifications.

This follows AWS security best practices.

---

## 8. Could DriftGuard work with a ReadOnlyAccess IAM policy?

Yes.

A read-only IAM policy is sufficient for the current implementation.

---

## 9. Does DriftGuard require AdministratorAccess?

No.

Administrator privileges are unnecessary.

Only the minimum permissions required to retrieve resource metadata should be granted.

---

# AWS Credentials

## 10. How does DriftGuard authenticate with AWS?

DriftGuard uses Boto3's default credential provider chain.

Supported methods include:

- Environment Variables
- AWS CLI Configuration
- IAM Roles
- EC2 Instance Profiles
- AWS SSO

---

## 11. Does DriftGuard store AWS credentials?

No.

Credentials are never stored within the application.

Authentication is delegated entirely to Boto3.

---

## 12. Does DriftGuard log AWS credentials?

No.

Sensitive credentials are never printed, logged, or exported.

---

## 13. Can IAM Roles be used instead of Access Keys?

Yes.

Using IAM Roles is the recommended production approach because it eliminates long-lived credentials.

---

# Infrastructure Security

## 14. Can DriftGuard detect security misconfigurations?

Partially.

Current implementation detects infrastructure drift.

Some drift may also represent security issues, such as:

- Open Security Groups
- Disabled S3 encryption
- Disabled public access blocks

Future versions may include dedicated security rule validation.

---

## 15. Is DriftGuard a vulnerability scanner?

No.

It detects configuration drift.

It does not scan for CVEs, malware, operating system vulnerabilities, or application security issues.

---

## 16. Does DriftGuard replace AWS Config?

No.

AWS Config continuously monitors AWS resources.

DriftGuard performs targeted, Terraform-aware drift analysis.

Both tools serve different purposes.

---

## 17. Can DriftGuard detect unauthorized manual changes?

Yes.

If a manual change modifies a supported resource attribute and the Terraform State is not updated, DriftGuard reports it as infrastructure drift.

---

## 18. Can DriftGuard determine who changed a resource?

No.

It identifies **what changed**, not **who changed it**.

To identify the user responsible, services such as AWS CloudTrail should be used.

---

# Data Protection

## 19. Does DriftGuard transmit infrastructure data externally?

No.

All comparisons occur locally.

The application does not send infrastructure information to external services.

---

## 20. Is Terraform State encrypted by DriftGuard?

No.

DriftGuard reads the state file as provided.

Encryption and secure storage remain the responsibility of the chosen Terraform backend.

---

## 21. Does DriftGuard expose sensitive infrastructure information?

No.

Only the information required for drift analysis is displayed.

Future report exports may include masking for sensitive values.

---

# Production Security

## 22. Can DriftGuard be integrated into CI/CD pipelines?

Yes.

Its read-only design makes it suitable for deployment validation and compliance checks.

---

## 23. How should DriftGuard be deployed in production?

Recommended practices include:

- Dedicated read-only IAM role
- Secure Terraform backend
- IAM Role authentication
- Least Privilege permissions
- Audit logging
- Version-controlled configuration

---

## 24. How would you secure DriftGuard in an enterprise environment?

Recommended controls include:

- IAM Roles
- MFA for administrators
- Encrypted Terraform State
- Centralized logging
- Secrets Manager integration
- Private network execution
- CI/CD security gates

---

## 25. Can DriftGuard support compliance requirements?

Yes.

Although not a compliance tool, it can assist with identifying unauthorized infrastructure changes that impact standards such as:

- CIS Benchmarks
- ISO 27001
- SOC 2
- PCI DSS

---

# Future Security Enhancements

## 26. What security features are planned?

Potential future enhancements include:

- CIS Benchmark validation
- Security risk scoring
- Compliance reporting
- IAM drift detection
- KMS drift detection
- Secrets Manager validation
- Policy-as-Code integration

---

## 27. Could DriftGuard integrate with AWS Security Hub?

Yes.

Future versions could publish drift findings to AWS Security Hub for centralized visibility.

---

## 28. Could DriftGuard integrate with SIEM platforms?

Yes.

Drift reports could be exported to platforms such as:

- Splunk
- Microsoft Sentinel
- IBM QRadar
- Elastic Security

for centralized monitoring.

---

## 29. How would you improve the security architecture in Version 2?

Future improvements include:

- RBAC
- Authentication
- Report encryption
- Signed reports
- API authentication
- Secure plugin framework
- Audit trail generation

---

## 30. What is the biggest security principle behind DriftGuard?

**Never modify production infrastructure during analysis.**

Detection and remediation are intentionally separated to minimize operational risk, preserve evidence of manual changes, and allow engineers to make informed decisions before applying any corrective actions.
