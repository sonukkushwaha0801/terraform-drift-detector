<!-- ====================================================== -->
<!-- DriftGuard -->
<!-- ====================================================== -->

# 🛡️ DriftGuard

### Infrastructure Drift Detection Engine for Terraform-managed Cloud Infrastructure

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-1.x-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Boto3](https://img.shields.io/badge/Boto3-AWS_SDK-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

## 📌 Overview

**DriftGuard** is a production-oriented Infrastructure Drift Detection Engine that identifies manual changes made to Terraform-managed cloud resources.

Infrastructure drift occurs when resources are modified directly from the cloud console, CLI, SDKs, or automation tools instead of through Terraform. These changes leave the infrastructure in an inconsistent state where the actual cloud configuration no longer matches the Terraform state.

DriftGuard compares the **expected infrastructure state stored in the Terraform State File** with the **actual infrastructure state retrieved directly from the cloud provider APIs** and generates a detailed drift report highlighting every detected deviation.

The project is designed with a modular architecture, making it easy to extend to additional cloud providers and resource types.

---

## ✨ Key Features

- 🔍 Detects infrastructure drift in Terraform-managed resources
- ☁️ Direct AWS API validation using **Boto3**
- 📄 Parses Terraform State Files (`terraform.tfstate`)
- 🖥️ Interactive CLI with resource selection
- ⚡ Scan a single resource or all resources of the same type
- 📊 Severity-based drift reporting
- 🧩 Modular architecture for easy extension
- 🔒 Security-focused drift detection
- 🚀 Production-inspired project structure
- 🌍 Cloud-provider extensible (AWS → Azure → GCP)

---

## 🎯 Why DriftGuard?

Terraform assumes that infrastructure changes are performed exclusively through Infrastructure as Code.

In real-world environments, administrators frequently make emergency or manual changes directly from the cloud console.

Examples include:

- Changing EC2 instance types
- Opening Security Group ports
- Disabling S3 bucket encryption
- Modifying IAM configurations
- Changing networking configurations

These unmanaged modifications create **Infrastructure Drift**, resulting in:

- Security vulnerabilities
- Configuration inconsistencies
- Compliance violations
- Failed deployments
- Unexpected Terraform plans
- Production outages

DriftGuard helps identify these changes before they become operational risks.

---
