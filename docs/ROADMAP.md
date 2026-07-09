# Roadmap

## Overview

DriftGuard is designed to evolve from an AWS-focused Infrastructure Drift Detection Engine into a cloud-agnostic platform capable of analyzing infrastructure drift across multiple cloud providers.

This roadmap outlines the planned evolution of the project.

---

# Version 1.0.0 ✅

## Initial Stable Release

### Core Framework

- [x] Interactive CLI
- [x] Terraform State Parser
- [x] Modular Architecture
- [x] Resource Selection Engine
- [x] Read-only Drift Detection
- [x] Severity-based Reporting

### AWS Resources

- [x] EC2 Drift Detection
- [x] Security Group Drift Detection
- [x] S3 Drift Detection

---

# Version 1.1

## AWS Resource Expansion

### Compute

- [ ] Auto Scaling Groups
- [ ] Launch Templates
- [ ] Elastic Load Balancers
- [ ] Target Groups

### Networking

- [ ] VPC
- [ ] Subnets
- [ ] Route Tables
- [ ] Internet Gateway
- [ ] NAT Gateway
- [ ] Network ACLs
- [ ] Elastic IP

### Security

- [ ] IAM Roles
- [ ] IAM Policies
- [ ] IAM Users
- [ ] KMS Keys

### Storage

- [ ] EBS Volumes
- [ ] EFS
- [ ] S3 Bucket Policies
- [ ] S3 Lifecycle Rules

---

# Version 1.2

## Database & Container Support

### Databases

- [ ] Amazon RDS
- [ ] Aurora
- [ ] DynamoDB

### Containers

- [ ] ECS
- [ ] EKS
- [ ] ECR

---

# Version 1.3

## Advanced Reporting

- [ ] HTML Reports
- [ ] JSON Reports
- [ ] CSV Export
- [ ] PDF Reports
- [ ] Report History
- [ ] Drift Summary Dashboard

---

# Version 1.4

## Performance Improvements

- [ ] Multi-threaded Scanning
- [ ] Parallel AWS API Requests
- [ ] Progress Indicators
- [ ] Scan Time Metrics
- [ ] Large Infrastructure Optimization

---

# Version 2.0

## Azure Support

### Azure Resources

- [ ] Virtual Machines
- [ ] Network Security Groups
- [ ] Virtual Networks
- [ ] Storage Accounts
- [ ] Azure SQL Database
- [ ] Azure Kubernetes Service (AKS)

---

# Version 2.5

## Google Cloud Platform Support

### GCP Resources

- [ ] Compute Engine
- [ ] Cloud Storage
- [ ] Firewall Rules
- [ ] Cloud SQL
- [ ] Google Kubernetes Engine (GKE)

---

# Version 3.0

## Enterprise Features

- [ ] Multi-cloud Scanning
- [ ] Drift Baselines
- [ ] Scheduled Drift Scans
- [ ] Email Notifications
- [ ] Slack Notifications
- [ ] Microsoft Teams Integration
- [ ] Web Dashboard
- [ ] REST API
- [ ] Authentication
- [ ] Role-Based Access Control (RBAC)

---

# Long-Term Vision

DriftGuard aims to become a cloud-agnostic Infrastructure Drift Detection Platform capable of identifying configuration drift across multiple cloud providers while remaining:

- Read-only
- Modular
- Extensible
- Cloud-independent
- Production-oriented

The long-term goal is to provide infrastructure engineers with a unified platform for drift analysis without modifying cloud resources or Terraform state.
