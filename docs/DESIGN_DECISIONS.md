# Design Decisions

## Overview

This document explains the major architectural and engineering decisions made during the development of DriftGuard.

Each decision was made to improve maintainability, scalability, usability, and production readiness.

---

# Decision 1

## Read-Only Drift Detection

### Decision

DriftGuard performs **read-only infrastructure analysis**.

The application never modifies:

- Terraform State
- Terraform Configuration
- Cloud Infrastructure

---

### Why?

The primary objective of DriftGuard is to **detect** infrastructure drift rather than automatically reconcile it.

Infrastructure reconciliation is an operational decision that should remain under the control of engineers.

Automatically modifying Terraform State could permanently hide important configuration changes.

---

### Benefits

- Safe to execute
- No accidental infrastructure modifications
- No Terraform State corruption
- Suitable for production environments

---

# Decision 2

## Compare Terraform State Instead of Running Terraform

### Decision

DriftGuard parses the existing `terraform.tfstate` file instead of invoking Terraform commands.

---

### Why?

Running Terraform introduces unnecessary dependencies and can modify state depending on the operation being executed.

Parsing the state file directly allows DriftGuard to remain lightweight and independent from Terraform execution.

---

### Benefits

- Faster execution
- Read-only analysis
- No dependency on Terraform commands
- Simplified execution pipeline

---

# Decision 3

## Resource-Specific Scanning

### Decision

Users select a resource type before drift detection begins.

Examples

- EC2
- Security Groups
- S3

---

### Why?

Production environments may contain hundreds or thousands of cloud resources.

Scanning every supported resource during every execution would increase runtime and API usage.

Resource-level selection provides a more focused and efficient workflow.

---

### Benefits

- Faster execution
- Reduced AWS API calls
- Better user experience
- Easier troubleshooting

---

# Decision 4

## Single Resource or Bulk Resource Selection

### Decision

After selecting a resource type, users may:

- Scan a single resource
- Scan all resources of the selected type

---

### Why?

Infrastructure investigations typically focus on a specific resource.

Scanning only the required resource significantly reduces execution time while still allowing bulk analysis when needed.

---

### Benefits

- Reduced execution time
- Flexible workflow
- Production-oriented behavior

---

# Decision 5

## Independent Scanner per Resource

### Decision

Every supported AWS service has its own scanner.

Current implementation

```
EC2 Scanner

Security Group Scanner

S3 Scanner
```

---

### Why?

AWS services expose different APIs and data models.

Separating scanners avoids service-specific logic becoming tightly coupled.

---

### Benefits

- High cohesion
- Low coupling
- Easier maintenance
- Easy feature expansion

---

# Decision 6

## Independent Drift Engine per Resource

### Decision

Each AWS service implements its own drift comparison engine.

Examples

```
EC2 Drift Engine

SG Drift Engine

S3 Drift Engine
```

---

### Why?

Each AWS resource has different attributes and drift characteristics.

Keeping comparison logic isolated prevents a single generic engine from becoming overly complex.

---

### Benefits

- Easier testing
- Cleaner implementation
- Better scalability

---

# Decision 7

## Normalize AWS API Responses

### Decision

All scanner outputs are normalized before comparison.

Examples include:

- Empty values
- Boolean defaults
- Security Group rule formats
- Missing AWS attributes

---

### Why?

Terraform State and AWS APIs frequently represent identical configurations using different data structures.

Without normalization, logically equivalent configurations may appear as infrastructure drift.

---

### Example

Terraform State

```
from_port = 0
to_port = 0
```

AWS API

```
from_port = None
to_port = None
```

After normalization

```
from_port = 0
to_port = 0
```

---

### Benefits

- Eliminates false positives
- Consistent comparison
- Reliable drift analysis

---

# Decision 8

## Severity-Based Reporting

### Decision

Every detected drift is assigned a severity level.

Current levels

- LOW
- MEDIUM
- HIGH
- CRITICAL

---

### Why?

Not every infrastructure change has the same operational impact.

Severity helps engineers prioritize remediation.

---

### Example

| Drift                           | Severity |
| ------------------------------- | -------- |
| Tag Change                      | LOW      |
| Monitoring Disabled             | MEDIUM   |
| Instance Type Changed           | HIGH     |
| Security Group Open to Internet | CRITICAL |

---

# Decision 9

## Modular Project Structure

### Decision

The project is divided into functional modules.

```
Parser

↓

Scanner

↓

Drift Engine

↓

Report Generator
```

---

### Why?

Separating responsibilities simplifies development and enables independent testing.

---

### Benefits

- Easier debugging
- Cleaner codebase
- Better scalability
- Easier onboarding for contributors

---

# Decision 10

## Cloud-Provider Agnostic Architecture

### Decision

The architecture was intentionally designed so that cloud providers can be added without changing the execution pipeline.

Future providers

- Azure
- Google Cloud Platform

---

### Why?

The execution pipeline remains identical regardless of the cloud provider.

Only scanners and drift engines need to change.

---

### Benefits

- Reusable architecture
- Easy cloud expansion
- Long-term maintainability

---

# Decision 11

## Production-Oriented Design

### Decision

The project was developed using production-inspired design principles rather than tutorial-oriented implementation.

Examples include

- Modular architecture
- Resource isolation
- Independent scanners
- Independent drift engines
- Read-only analysis
- Explicit normalization
- Structured reporting

---

### Why?

The objective was to simulate how infrastructure analysis tools are designed in enterprise environments.

---

# Summary

Every design decision in DriftGuard prioritizes one or more of the following goals:

- Safety
- Scalability
- Maintainability
- Extensibility
- Performance
- Readability

The result is a modular Infrastructure Drift Detection Engine that can evolve beyond AWS while maintaining a consistent execution model.
