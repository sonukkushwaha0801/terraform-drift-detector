# Implementation Engineering FAQ

## Overview

This document explains the implementation choices made while developing DriftGuard.

The objective is to clarify why specific technologies, coding patterns, and implementation strategies were selected throughout the project.

---

# Programming Language

## 1. Why did you choose Python?

Python provides an excellent balance between readability, rapid development, and AWS ecosystem support.

Its mature libraries, especially Boto3, make it well suited for infrastructure automation and cloud engineering.

---

## 2. Why not Go?

Go is an excellent language for cloud-native tooling.

However, the objective of DriftGuard was to build a production-oriented infrastructure analysis tool while leveraging existing expertise in Python and AWS automation.

The architecture is language-independent and could be reimplemented in Go in the future.

---

## 3. Why not Java?

Java introduces additional complexity for a CLI-based infrastructure tool.

Python provides faster development, cleaner syntax, and excellent AWS SDK support.

---

## AWS SDK

## 4. Why did you use Boto3?

Boto3 is the official AWS SDK for Python.

It provides complete access to AWS APIs and is actively maintained by AWS.

---

## 5. Why not use Terraform Provider SDK?

Terraform Provider SDK is intended for developing Terraform providers.

DriftGuard performs infrastructure analysis rather than resource provisioning, making Boto3 a more appropriate choice.

---

## 6. Why not call AWS CLI commands?

Calling AWS CLI commands requires spawning subprocesses and parsing command-line output.

Using Boto3 provides:

- Native Python objects
- Better error handling
- Improved performance
- Easier testing

---

# Terraform Implementation

## 7. Why manually parse Terraform State?

Terraform State already contains the deployed infrastructure along with resource identifiers.

Reading the file directly removes the dependency on Terraform execution while keeping the implementation lightweight.

---

## 8. Why not execute Terraform commands?

The goal of DriftGuard is analysis, not infrastructure management.

Executing Terraform commands introduces unnecessary dependencies and potential side effects.

---

## 9. Why use Terraform State instead of HCL files?

Terraform State represents the deployed infrastructure.

HCL files describe the desired infrastructure.

Drift detection requires comparison against what Terraform actually created.

---

# Data Handling

## 10. Why convert AWS responses into dictionaries?

AWS API responses are complex and deeply nested.

Converting them into standardized dictionaries simplifies comparison and keeps the drift engines provider-independent.

---

## 11. Why normalize data?

Terraform State and AWS APIs often represent identical values differently.

Normalization eliminates false positives by converting equivalent values into a consistent format.

---

## 12. Why not compare raw JSON?

Raw JSON comparisons produce unnecessary differences due to:

- Ordering
- Empty values
- Nested structures
- Provider-specific formatting

Field-level comparison is more accurate.

---

## 13. Why compare attributes individually?

Individual comparison allows:

- Better reporting
- Severity classification
- Easier debugging
- Cleaner implementation

---

# Project Structure

## 14. Why separate each AWS service into its own module?

Each AWS service has different APIs and configuration models.

Independent modules reduce coupling and simplify future development.

---

## 15. Why use separate scanners?

Scanners are responsible only for retrieving live infrastructure data.

They should not contain comparison logic.

---

## 16. Why use separate drift engines?

Comparison logic varies significantly across AWS services.

Separate drift engines keep the implementation clean and maintainable.

---

## 17. Why use a report generator?

Separating reporting from detection allows future support for:

- HTML reports
- JSON export
- PDF reports
- Web dashboards

without changing detection logic.

---

# User Experience

## 18. Why use an interactive CLI?

Interactive selection reduces user input errors and provides a guided workflow.

It also makes the tool easier to use during operational investigations.

---

## 19. Why ask users to select a resource first?

Large Terraform States may contain hundreds of resources.

Selecting the target resource first reduces execution time and unnecessary AWS API calls.

---

## 20. Why allow scanning a single resource?

Most production investigations involve a specific resource rather than the entire infrastructure.

Single-resource scanning improves efficiency.

---

# Error Handling

## 21. How does DriftGuard handle missing resources?

The parser validates that the selected resource exists in the Terraform State before scanning begins.

If not found, execution stops with a clear error message.

---

## 22. How does DriftGuard handle AWS API failures?

AWS API exceptions are caught and reported without crashing the application whenever possible.

Meaningful error messages are displayed to help identify the issue.

---

## 23. How does DriftGuard handle invalid Terraform State files?

The parser validates the file before processing.

Malformed or corrupted state files generate descriptive errors and terminate execution safely.

---

# Code Quality

## 24. Why keep each module focused on one responsibility?

Applying the Single Responsibility Principle makes the codebase easier to understand, test, and maintain.

---

## 25. How do you ensure the project remains maintainable?

The project follows:

- Modular architecture
- Consistent naming conventions
- Independent resource modules
- Clear separation of concerns
- Reusable comparison logic

---

## 26. How would you test DriftGuard?

Testing can include:

- Unit tests for parsers
- Mocked AWS API responses
- Drift engine comparison tests
- Integration tests against AWS
- End-to-end CLI testing

---

## Future Improvements

## 27. What implementation improvements are planned?

Future work includes:

- Plugin architecture
- Async AWS requests
- Remote state support
- HTML report generation
- JSON exports
- CI/CD integration

---

## 28. Would you refactor anything?

As the number of supported resources grows, a plugin-based architecture would reduce registration logic and simplify onboarding of new resource modules.

---

## 29. What implementation decision had the biggest impact?

Separating the project into:

- Parser
- Scanner
- Drift Engine
- Report Generator

This made the project significantly easier to extend and maintain.

---

## 30. What was the most challenging implementation problem?

The biggest challenge was handling differences between Terraform State and AWS API responses.

Although both represented the same infrastructure, differences in formatting, nested structures, and default values initially produced false-positive drift results.

Implementing normalization across scanners resolved this issue while improving comparison accuracy.
