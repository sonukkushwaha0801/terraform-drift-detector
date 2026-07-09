# Behavioral & Interview Questions

## Overview

This document contains common interview questions that may arise while discussing the DriftGuard project.

The answers focus on engineering decisions, project motivation, technical challenges, and lessons learned throughout the development process.

---

# Project Motivation

## 1. Why did you build DriftGuard?

I wanted to solve a practical Infrastructure as Code problem that engineers face in production environments.

Although Terraform can provision infrastructure, I wanted a dedicated tool that could analyze infrastructure drift without modifying Terraform State or cloud resources.

The goal was to provide engineers with visibility before deciding whether manual changes should be accepted or reverted.

---

## 2. What real-world problem does this project solve?

DriftGuard detects infrastructure drift caused by manual changes made outside Terraform.

Examples include:

- Changing EC2 instance types
- Modifying Security Groups
- Disabling S3 encryption
- Updating bucket configuration

These changes often go unnoticed until deployments fail or security incidents occur.

---

## 3. Why did you choose this project?

I wanted to build something beyond CRUD applications.

The project combines:

- Terraform
- AWS
- Python
- Cloud APIs
- System Design
- Infrastructure as Code

while solving a genuine operational problem.

---

## 4. Who would use DriftGuard?

Typical users include:

- DevOps Engineers
- Cloud Engineers
- Platform Engineers
- SREs
- Infrastructure Engineers
- Security Teams

---

## 5. What inspired this project?

While learning Terraform, I realized that manual infrastructure changes are common in production.

Although Terraform provides refresh and plan operations, I wanted a dedicated read-only analysis tool focused on drift detection.

---

# Technical Challenges

## 6. What was the biggest challenge while building DriftGuard?

The biggest challenge was handling differences between Terraform State and AWS API responses.

Although both represented the same infrastructure, their data formats often differed, resulting in false-positive drift detection.

---

## 7. How did you solve that problem?

I introduced a normalization layer.

Both Terraform State and AWS API responses are converted into a consistent format before comparison.

This significantly improved comparison accuracy.

---

## 8. What was the hardest bug you fixed?

False-positive drift detection caused by differences in AWS and Terraform representations.

Examples included:

- Empty values
- Boolean fields
- Nested objects
- Security Group rules
- S3 versioning structures

---

## 9. What feature took the longest to implement?

The drift comparison engine.

Every supported AWS resource required its own comparison logic while maintaining a consistent architecture.

---

## 10. What part are you most proud of?

The modular architecture.

Adding a new AWS resource only requires:

- Scanner
- Drift Engine

without changing the overall execution pipeline.

---

# Engineering Decisions

## 11. Why didn't you use Terraform Refresh?

Terraform Refresh updates the Terraform State.

DriftGuard preserves the existing state and reports the differences instead.

This allows engineers to investigate changes before deciding whether to synchronize the infrastructure.

---

## 12. Why not simply use Terraform Plan?

Terraform Plan determines how Terraform should reconcile infrastructure.

DriftGuard focuses on identifying what changed before reconciliation.

Both tools solve different operational problems.

---

## 13. Why make DriftGuard read-only?

Read-only analysis eliminates the risk of accidental infrastructure modifications.

Detection and remediation should remain separate operational decisions.

---

## 14. Why separate Scanners and Drift Engines?

Scanners retrieve data.

Drift Engines compare data.

Separating these responsibilities keeps the architecture modular and easier to maintain.

---

## 15. Why support single-resource scanning?

Production investigations usually focus on one affected resource.

Scanning only the required resource reduces execution time and unnecessary AWS API calls.

---

# Design & Architecture

## 16. What architectural pattern did you follow?

A layered modular architecture consisting of:

- CLI
- Parser
- Scanner
- Drift Engine
- Report Generator

Each layer has a single responsibility.

---

## 17. How would you add Azure support?

Implement:

- Azure Scanner
- Azure Drift Engine

The existing parser, CLI, and reporting layers would remain unchanged.

---

## 18. How would you scale this project?

Potential improvements include:

- Multi-threading
- Async AWS requests
- Plugin architecture
- Multi-account support
- Multi-region scanning
- Distributed workers

---

## 19. If you started again, what would you do differently?

I would introduce a plugin architecture from the beginning.

This would reduce manual registration when adding new cloud providers or AWS services.

---

## 20. What would Version 2 include?

Planned enhancements include:

- Azure Support
- Google Cloud Support
- HTML Reports
- REST API
- Web Dashboard
- Scheduled Drift Detection
- Remote State Support

---

# Production

## 21. Is this production-ready?

The current implementation is production-oriented.

However, enterprise deployments would benefit from additional features such as:

- Authentication
- RBAC
- Report persistence
- CI/CD integration
- Notification systems

---

## 22. How would you deploy DriftGuard?

Possible deployment models include:

- Developer Workstation
- CI/CD Pipeline
- Docker Container
- Kubernetes Job
- Scheduled Lambda Function

depending on operational requirements.

---

## 23. How would teams use this tool?

Typical workflow:

Terraform Apply

↓

Infrastructure Changes

↓

Periodic Drift Scan

↓

Drift Report

↓

Engineer Decision

↓

Terraform Plan

↓

Terraform Apply

---

## Learning

## 24. What did this project teach you?

This project strengthened my understanding of:

- Terraform State
- AWS APIs
- Infrastructure Drift
- System Design
- Modular Architecture
- Cloud Automation
- Production-oriented Development

---

## 25. What engineering lesson had the biggest impact?

Two systems representing the same infrastructure may use completely different data formats.

Reliable comparison requires normalization before evaluation.

---

## Career

## 26. Why should this project matter to an interviewer?

This project demonstrates more than programming.

It showcases:

- Infrastructure as Code
- AWS Integration
- System Design
- Software Architecture
- Production Thinking
- Problem Solving

rather than just implementing a tutorial project.

---

## 27. Which role is this project most relevant for?

It is most relevant for:

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- Infrastructure Automation Engineer

---

## 28. If given six more months, what would you build?

I would evolve DriftGuard into a cloud-agnostic platform supporting:

- AWS
- Azure
- Google Cloud
- Kubernetes

along with scheduled scanning, REST APIs, dashboards, and historical drift analysis.

---

## 29. What differentiates DriftGuard from your other projects?

Unlike automation or scraping projects, DriftGuard required designing an extensible architecture, integrating with cloud APIs, handling infrastructure state, and solving a real operational problem faced by infrastructure teams.

---

## 30. What is the biggest takeaway from this project?

Building production software is not just about writing code.

It requires making thoughtful architectural decisions, designing for extensibility, handling edge cases, prioritizing operational safety, and creating a system that can evolve over time.
