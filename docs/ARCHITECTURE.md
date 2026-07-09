# System Architecture

## Overview

DriftGuard follows a modular layered architecture that separates infrastructure parsing, cloud scanning, drift analysis, and reporting into independent components.

Each module has a single responsibility, making the project easier to maintain, extend, and test.

---

# High-Level Architecture

```text
                        Terraform Managed Infrastructure

                   Terraform Configuration (.tf)
                               │
                               ▼
                        terraform apply
                               │
                               ▼
                     Terraform State (terraform.tfstate)
                               │
                               ▼
                    ┌─────────────────────────┐
                    │     DriftGuard CLI      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                     Resource Selection Engine
                                 │
                                 ▼
                      Terraform State Parser
                                 │
              Expected Infrastructure State
                                 │
                                 ▼
                      Cloud Resource Scanner
                          (AWS Boto3 APIs)
                                 │
               Actual Infrastructure State
                                 │
                                 ▼
                         Drift Detection Engine
                                 │
                                 ▼
                        Severity Classification
                                 │
                                 ▼
                          Report Generator
                                 │
                                 ▼
                          Terminal Output
```

---

# Architecture Principles

The architecture was designed around the following principles:

- Separation of Concerns
- Modular Design
- Read-only Infrastructure Analysis
- Resource-specific Processing
- Cloud-provider Independence
- Easy Extensibility

Every component has a clearly defined responsibility.

---

# Component Overview

## 1. CLI Layer

Responsible for user interaction.

Responsibilities:

- Display terminal interface
- Resource selection
- State file selection
- Resource instance selection
- Start drift analysis

Entry Point

```
run.sh
```

---

## 2. Application Controller

Coordinates the complete execution flow.

Responsibilities

- Parse CLI arguments
- Invoke resource parser
- Call appropriate scanner
- Execute drift engine
- Generate report

Main File

```
main.py
```

---

## 3. Terraform State Parser

Responsible for reading Terraform State and extracting only the selected resource type.

Responsibilities

- Load terraform.tfstate
- Validate resource existence
- Extract resource attributes
- Support single-resource and bulk-resource selection

Location

```
app/parser/
```

---

## 4. Cloud Scanner Layer

Responsible for retrieving the actual infrastructure configuration directly from AWS.

Uses

- Boto3
- AWS APIs

Current Scanners

```
EC2 Scanner

Security Group Scanner

S3 Scanner
```

Responsibilities

- Query AWS APIs
- Normalize API responses
- Return comparable data structures

Location

```
app/scanner/
```

---

## 5. Drift Detection Engine

The core component of DriftGuard.

Responsible for comparing

Expected State

↓

Actual State

↓

Detected Drift

Each supported AWS service has an independent drift engine.

Current Engines

```
EC2 Drift Engine

Security Group Drift Engine

S3 Drift Engine
```

Location

```
app/engine/
```

---

## 6. Report Generator

Responsible for presenting drift analysis results.

Responsibilities

- Severity classification
- Human-readable output
- Console reporting

Location

```
app/report/
```

---

# Execution Workflow

```
User

↓

Select Resource Type

↓

Select terraform.tfstate

↓

Terraform Parser

↓

Extract Expected State

↓

AWS Scanner

↓

Collect Live Infrastructure

↓

Normalize Data

↓

Drift Detection Engine

↓

Generate Drift Report
```

---

# Supported Resources

Current implementation supports

```
EC2 Instances

Security Groups

S3 Buckets
```

Each resource follows the same architecture

```
Terraform State

↓

Parser

↓

AWS Scanner

↓

Drift Engine

↓

Report
```

This consistent design allows new resource types to be added with minimal changes.

---

# Resource Modules

Current implementation

```
EC2

├── EC2 Scanner
├── EC2 Drift Engine
└── EC2 Report


Security Group

├── SG Scanner
├── SG Drift Engine
└── SG Report


S3

├── S3 Scanner
├── S3 Drift Engine
└── S3 Report
```

---

# Design Advantages

The architecture provides several advantages.

## Modular

Every AWS service is implemented independently.

Adding a new service requires only

- Scanner
- Drift Engine

No existing modules need modification.

---

## Read-Only

DriftGuard never performs

- terraform apply
- terraform refresh
- terraform import

It only compares infrastructure.

---

## Extensible

Future cloud providers can follow the same design.

Example

```
Azure Scanner

↓

Azure Drift Engine
```

or

```
GCP Scanner

↓

GCP Drift Engine
```

---

## Scalable

The architecture supports

- Single resource scan
- Multiple resource scan
- Entire resource-type scan

without changing the execution pipeline.

---

# Directory Structure

```
terraform-drift-detector/

├── app/
│   ├── engine/
│   ├── parser/
│   ├── report/
│   └── scanner/
│
├── terraform/
│
├── tests/
│
├── docs/
│
├── assets/
│
├── main.py
│
└── run.sh
```

---

# Future Architecture

The architecture is intentionally cloud-independent.

Future roadmap

```
                    DriftGuard

        ┌─────────────┼─────────────┐

      AWS          Azure          GCP

        │              │             │

     Scanner       Scanner      Scanner

        │              │             │

   Drift Engine  Drift Engine Drift Engine

        │              │             │

         └──────────────┼─────────────┘

                Unified Reporting Engine
```

---

# Summary

DriftGuard follows a modular, layered architecture designed for production-oriented infrastructure analysis.

The separation between parsing, scanning, drift detection, and reporting allows the project to remain maintainable, extensible, and cloud-provider agnostic while supporting future expansion to additional AWS services and other cloud platforms.
