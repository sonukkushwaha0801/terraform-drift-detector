# Terraform Engineering FAQ

## Overview

This document answers Terraform-related engineering questions that may arise while reviewing the DriftGuard project.

The purpose of this document is to explain the engineering decisions behind DriftGuard, clarify how it differs from native Terraform workflows, and describe the design philosophy adopted during development.

---

# General Terraform Questions

## 1. Why did you build DriftGuard when Terraform already provides drift detection?

Terraform is designed to provision and manage infrastructure, while DriftGuard focuses exclusively on infrastructure drift analysis.

Although Terraform can identify drift during planning, DriftGuard provides a dedicated, read-only analysis layer that compares Terraform State with the live AWS infrastructure without modifying either.

This allows engineers to inspect changes before deciding whether to accept or revert them.

---

## 2. What problem does DriftGuard solve that Terraform does not?

Terraform primarily focuses on provisioning and reconciliation.

DriftGuard focuses on investigation.

It allows engineers to:

- Analyze infrastructure drift
- Scan individual resources
- Produce dedicated drift reports
- Classify drift severity
- Perform read-only analysis

before any Terraform operation is executed.

---

## 3. How does DriftGuard complement Terraform?

Terraform provisions infrastructure.

DriftGuard validates that the deployed infrastructure still matches Terraform's expected state.

A typical workflow becomes:

```text
Terraform Apply
        │
Production Infrastructure
        │
Manual Change
        │
DriftGuard
        │
Drift Report
        │
Engineer Decision
        │
Terraform Plan / Apply
```

Instead of replacing Terraform, DriftGuard provides an additional validation layer.

---

## 4. Is DriftGuard a replacement for Terraform?

No.

Terraform remains responsible for:

- Infrastructure provisioning
- Infrastructure updates
- Resource lifecycle management
- State management

DriftGuard only detects and reports infrastructure drift.

Both tools serve different purposes and complement each other.

---

## 5. Why does DriftGuard rely on Terraform State?

Terraform State represents the last successfully managed infrastructure.

It contains the deployed resource identifiers and the expected configuration after provisioning.

Using the state file allows DriftGuard to compare the exact deployed infrastructure against the current cloud environment.

---

## 6. Why not compare the Terraform configuration (`.tf`) directly?

Terraform configuration describes the desired infrastructure.

Terraform State represents the infrastructure that was actually created.

Comparing against the state file provides a more accurate baseline because it includes:

- Resource IDs
- Computed attributes
- Provider-generated values
- Runtime configuration

which are not always available in Terraform configuration files.

---

## 7. Why is Terraform State treated as the expected infrastructure?

DriftGuard assumes that infrastructure should only be modified through Terraform.

Therefore, the Terraform State becomes the expected infrastructure baseline.

Any manual change performed outside Terraform is considered potential drift until an engineer decides whether it should be accepted or reverted.

---

# Terraform Refresh

## 8. Why didn't you use `terraform refresh`?

Terraform Refresh synchronizes the Terraform State with the live infrastructure.

While useful in some workflows, it updates the state file and accepts manual changes.

DriftGuard intentionally avoids modifying Terraform State.

Instead, it compares the current infrastructure with the existing state and reports the differences.

---

## 9. What happens internally when Terraform Refresh is executed?

Terraform queries the cloud provider for the latest resource configuration.

It then updates the Terraform State so that it matches the live infrastructure.

After refresh:

```text
Terraform State

↓

Updated

↓

Matches AWS
```

The original evidence of infrastructure drift is no longer present in the state file.

---

## 10. Why can Terraform Refresh be risky during investigations?

Suppose an administrator manually changes:

```text
EC2 Instance Type

t3.micro

↓

t3.small
```

Running Terraform Refresh immediately updates the Terraform State to match AWS.

As a result, engineers lose the opportunity to inspect what changed before synchronization.

DriftGuard preserves that visibility by performing read-only comparisons.

---

## 11. When is Terraform Refresh actually the correct solution?

Terraform Refresh is appropriate when manual infrastructure changes are intentional and should become part of Terraform's managed state.

Examples include:

- Emergency infrastructure modifications
- Planned operational updates
- Provider-generated changes

It is not intended as a dedicated drift investigation tool.

---

## 12. How is DriftGuard different from Terraform Refresh?

| Terraform Refresh           | DriftGuard             |
| --------------------------- | ---------------------- |
| Updates Terraform State     | Read-only analysis     |
| Accepts manual changes      | Reports manual changes |
| Synchronizes infrastructure | Detects drift          |
| No dedicated drift report   | Detailed drift report  |
| Modifies state              | Never modifies state   |

---

# Terraform Import

## 13. Why didn't you use `terraform import`?

Terraform Import is intended to bring unmanaged infrastructure under Terraform management.

It is not designed for drift analysis.

Using import would require updating the Terraform State instead of simply inspecting infrastructure changes.

---

## 14. What is the primary purpose of Terraform Import?

Terraform Import associates existing cloud resources with Terraform State.

Its purpose is resource adoption rather than configuration comparison.

---

## 15. Why isn't Terraform Import suitable for drift detection?

Terraform Import:

- Requires importing resources individually
- Updates Terraform State
- Focuses on state management
- Does not generate drift reports

For large infrastructures this becomes repetitive and inefficient.

---

## 16. How does DriftGuard avoid the limitations of Terraform Import?

DriftGuard directly compares:

```text
Terraform State

↓

AWS APIs

↓

Drift Report
```

No importing.

No state modification.

No resource adoption.

Only infrastructure analysis.

---

# Terraform Plan

## 17. Why not simply use `terraform plan`?

Terraform Plan calculates the actions required to reconcile infrastructure with Terraform configuration.

DriftGuard focuses on analyzing and explaining infrastructure differences before any reconciliation takes place.

---

## 18. How is DriftGuard different from `terraform plan`?

Terraform Plan answers:

> "What changes will Terraform make?"

DriftGuard answers:

> "What changed in the infrastructure?"

Although related, they solve different operational questions.

---

## 19. When should an engineer use DriftGuard instead of Terraform Plan?

DriftGuard is most useful when:

- Investigating incidents
- Validating production infrastructure
- Performing security reviews
- Checking manual console changes
- Auditing infrastructure

Terraform Plan should be used after deciding how to reconcile the infrastructure.

---

## 20. Can DriftGuard replace Terraform Plan?

No.

DriftGuard identifies configuration drift.

Terraform Plan determines the Terraform actions required to reconcile that drift.

## Both tools belong to different stages of the Infrastructure as Code workflow.

# Terraform State

## 21. Why parse the Terraform State manually?

DriftGuard parses the Terraform State directly because it contains the exact deployed infrastructure along with resource identifiers and computed attributes.

This allows the application to perform lightweight, read-only analysis without executing Terraform commands.

---

## 22. Why not use `terraform show -json`?

`terraform show -json` is a valid approach, but it requires invoking the Terraform CLI.

DriftGuard is designed to work independently of Terraform execution.

Reading the state file directly reduces dependencies, simplifies deployment, and improves execution speed.

---

## 23. What happens if the Terraform State is outdated?

If the Terraform State no longer represents the infrastructure that Terraform last managed, DriftGuard will compare AWS resources against outdated information.

This may produce drift reports that reflect stale state rather than recent infrastructure changes.

Keeping the Terraform State current remains the responsibility of the infrastructure team.

---

## 24. What happens if the Terraform State is corrupted?

DriftGuard validates the state file before beginning analysis.

If the file is corrupted or unreadable, execution stops and an appropriate error is displayed.

The application never attempts to repair or modify the state file.

---

## 25. Does DriftGuard support remote state backends?

Current implementation supports local Terraform State files only.

Support for remote backends such as:

- Amazon S3
- Terraform Cloud
- HCP Terraform
- Azure Blob Storage

is planned for future releases.

---

## 26. How would you add support for Terraform Cloud or S3 backends?

The parser can be extended with backend-specific adapters.

Instead of reading a local file, the parser would first retrieve the latest state from the configured backend before continuing with the existing drift detection pipeline.

The remaining architecture would remain unchanged.

---

# Infrastructure Drift

## 27. What exactly is Infrastructure Drift?

Infrastructure Drift occurs when cloud resources are modified outside Terraform.

Examples include:

- AWS Console
- AWS CLI
- SDKs
- Third-party automation
- Manual administrator changes

As a result, the deployed infrastructure no longer matches Terraform's expected state.

---

## 28. What types of manual changes can DriftGuard detect?

Current implementation detects drift for:

### EC2

- Instance Type
- Instance State
- AMI
- Root Volume
- Security Groups
- Key Pair
- IAM Instance Profile
- Monitoring
- Networking
- Tags

### Security Groups

- Ingress Rules
- Egress Rules
- Description
- Tags

### S3

- Bucket Existence
- Versioning
- Server-Side Encryption
- Public Access Configuration
- Tags

---

## 29. What types of changes are currently outside the scope of DriftGuard?

Current limitations include:

- Unsupported AWS resources
- Terraform configuration validation
- Automatic remediation
- Compliance policy enforcement
- Historical drift tracking
- Scheduled monitoring

These capabilities are planned for future versions.

---

## 30. How does DriftGuard determine whether a resource has drifted?

DriftGuard compares:

```text
Terraform State
(Expected)

↓

AWS APIs
(Actual)

↓

Field-by-field Comparison

↓

Drift Report
```

Every supported attribute is compared individually.

Any difference is classified as infrastructure drift.

---

# Production Questions

## 31. Why perform read-only drift analysis?

Read-only analysis ensures that the application cannot accidentally modify infrastructure or Terraform State.

This makes DriftGuard safe to execute in production environments.

---

## 32. Why not automatically fix detected drift?

Infrastructure reconciliation is an operational decision.

Some manual changes are intentional.

Automatically reverting them could introduce production outages.

DriftGuard reports the differences while allowing engineers to decide the appropriate action.

---

## 33. Can DriftGuard accidentally modify infrastructure?

No.

The application performs only read operations through AWS APIs.

It never calls APIs that create, update, or delete cloud resources.

---

## 34. Can DriftGuard modify the Terraform State?

No.

The Terraform State is treated as a read-only data source.

DriftGuard never executes Terraform commands that modify state.

---

## 35. Is DriftGuard safe to run in production environments?

Yes.

Because the application performs read-only analysis and does not modify infrastructure or Terraform State, it can safely be used for operational investigations and drift analysis in production environments.

---

# Future Questions

## 36. Could DriftGuard support OpenTofu?

Yes.

OpenTofu maintains compatibility with Terraform State and Infrastructure as Code workflows.

Supporting OpenTofu would primarily involve validating state compatibility and updating provider integrations where necessary.

---

## 37. Could DriftGuard support Pulumi?

Yes, but additional work would be required.

Pulumi uses a different state model and programming-based infrastructure definitions.

A dedicated Pulumi parser would need to be implemented.

---

## 38. Could DriftGuard compare against multiple Terraform States?

Yes.

A future version could support multiple environments such as:

- Development
- Staging
- Production

Each environment would have its own state source while reusing the existing comparison engine.

---

## 39. How would you support Terraform Workspaces?

Workspace support can be added by allowing users to select a workspace before analysis.

DriftGuard would then load the corresponding state file and execute the same drift detection pipeline.

The core architecture would remain unchanged.

---

## 40. How would you support multi-account AWS environments?

Multi-account support can be implemented by assuming IAM roles into different AWS accounts.

Each account would be scanned independently, and the results could be consolidated into a unified drift report.

This approach would preserve the existing modular architecture while extending DriftGuard for enterprise-scale environments.
