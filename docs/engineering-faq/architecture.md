# Architecture Engineering FAQ

## Overview

This document explains the architectural decisions behind DriftGuard and the reasoning that influenced the system design.

---

# System Design

## 1. Why did you choose a modular architecture?

A modular architecture separates independent responsibilities into dedicated components. This improves maintainability, testing, scalability, and allows new resource types to be added without modifying existing modules.

---

## 2. Why not build everything inside a single Python file?

A monolithic implementation quickly becomes difficult to maintain as features grow. Separating responsibilities keeps the codebase organized and reduces coupling.

---

## 3. What architectural pattern does DriftGuard follow?

DriftGuard follows a layered modular architecture consisting of:

- CLI Layer
- Parser Layer
- Scanner Layer
- Drift Engine
- Report Generator

Each layer has a single responsibility.

---

## 4. Why separate scanners from drift engines?

Scanners collect live infrastructure data.

Drift Engines compare expected and actual configurations.

Separating them improves maintainability and allows comparison logic to evolve independently of cloud APIs.

---

## 5. Why create one scanner for each AWS service?

Every AWS service exposes different APIs and data structures.

Separate scanners prevent service-specific logic from affecting other resources.

---

## 6. Why create one drift engine per resource?

Every AWS resource has different configuration attributes.

Separate drift engines keep comparison logic simple and resource-specific.

---

## 7. Why not build one generic drift engine?

A generic engine would contain numerous conditional statements for different resources, increasing complexity.

Independent drift engines are easier to maintain and extend.

---

## 8. Why separate the parser from scanners?

The parser extracts expected infrastructure from Terraform State.

Scanners retrieve actual infrastructure from AWS.

Keeping them independent maintains clear separation of responsibilities.

---

## 9. Why have a dedicated report generator?

Reporting is independent of drift detection.

Future output formats such as HTML, JSON, PDF, or dashboards can be added without changing detection logic.

---

## 10. Why use a layered architecture?

Layered architectures reduce coupling and improve extensibility.

Each layer can evolve independently while preserving a stable execution pipeline.

---

# Design Decisions

## 11. Why normalize AWS API responses?

Terraform and AWS frequently represent identical values differently.

Normalization converts equivalent representations into a consistent format before comparison, eliminating false positives.

---

## 12. Why normalize data inside scanners instead of drift engines?

Scanners are responsible for producing standardized outputs.

This allows drift engines to focus exclusively on comparison logic.

---

## 13. Why not compare raw AWS responses?

Raw AWS responses contain nested structures, optional fields, and inconsistent representations.

Normalization simplifies comparison and improves reliability.

---

## 14. Why use dictionaries instead of AWS response objects?

Dictionaries provide a lightweight, provider-independent format that simplifies comparison and future cloud-provider support.

---

## 15. Why classify drift severity?

Not every infrastructure change has the same operational impact.

Severity helps engineers prioritize remediation.

---

# Execution Flow

## 16. What is the execution pipeline?

```
CLI

↓

Parser

↓

Scanner

↓

Drift Engine

↓

Report Generator
```

Each component performs one specific task.

---

## 17. Why parse Terraform State before calling AWS?

Terraform State identifies which resources should be inspected.

This prevents unnecessary AWS API calls.

---

## 18. Why scan AWS after parsing?

The scanner requires resource identifiers extracted from Terraform State.

Without parsing, the scanner would not know which resources to inspect.

---

## 19. Why compare expected and actual separately?

Keeping both datasets independent improves readability and simplifies debugging.

---

## 20. Why not compare resources directly during scanning?

Scanning should only retrieve infrastructure information.

Mixing comparison logic into scanners violates the Single Responsibility Principle.

---

# Scalability

## 21. How would you add support for Azure?

Implement:

- Azure Scanner
- Azure Drift Engine

The remaining architecture remains unchanged.

---

## 22. How would you support GCP?

The same architecture can be reused.

Only provider-specific scanners and comparison logic need to be implemented.

---

## 23. Why is the architecture cloud-provider independent?

The execution pipeline remains identical regardless of the cloud provider.

Only the implementation of scanners changes.

---

## 24. How would you add a new AWS resource?

Create:

- Scanner
- Drift Engine

Then register the resource in the parser and CLI.

---

## 25. How scalable is the architecture?

The modular design allows additional services to be added with minimal changes to existing code.

---

# Performance

## 26. Why scan only one resource by default?

Production investigations usually focus on a specific resource.

Scanning everything increases execution time and API usage.

---

## 27. Why support bulk scanning?

Bulk scans are useful during audits and compliance reviews.

Users can choose between targeted investigations and full resource analysis.

---

## 28. How would you improve performance?

Potential improvements include:

- Parallel AWS API calls
- Thread pools
- Async execution
- API batching
- Cached responses

---

## 29. How would you scale to thousands of resources?

Use worker pools, pagination, batching, and concurrent API requests while respecting AWS rate limits.

---

## 30. Why isn't parallel scanning implemented yet?

The current focus is correctness and architecture.

Parallel execution is a planned optimization rather than a core architectural requirement.

---

# Maintainability

## 31. How does the architecture simplify maintenance?

Each module has one responsibility.

Changes to one AWS service do not affect others.

---

## 32. How does the architecture improve testing?

Each scanner and drift engine can be tested independently using mocked AWS responses.

---

## 33. How does the architecture reduce bugs?

Small, isolated modules are easier to debug and reason about than large monolithic implementations.

---

## 34. What architectural principle are you most proud of?

The clear separation between:

- Parsing
- Scanning
- Comparison
- Reporting

This keeps the project extensible while minimizing coupling.

---

## 35. What would you improve in Version 2?

Future improvements include:

- Plugin architecture
- Multi-cloud support
- Parallel scanning
- Remote backend support
- Web dashboard
- REST API
- Scheduled drift detection
- Report history
