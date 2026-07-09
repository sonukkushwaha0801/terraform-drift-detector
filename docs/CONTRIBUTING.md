# Contributing

First of all, thank you for considering contributing to **DriftGuard**.

Contributions of all sizes are welcome, including bug fixes, documentation improvements, feature enhancements, and new cloud provider support.

---

# Ways to Contribute

You can contribute by:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Optimizing existing code
- Adding support for new AWS services
- Implementing Azure or Google Cloud support
- Improving report generation
- Writing tests
- Fixing performance issues

---

# Development Setup

## 1. Fork the Repository

Click the **Fork** button on GitHub.

---

## 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/terraform-drift-detector.git
```

---

## 3. Navigate to the Project

```bash
cd terraform-drift-detector
```

---

## 4. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Branch Naming

Create a feature branch before making changes.

Examples:

```text
feature/ec2-module
feature/azure-support
feature/report-export
bugfix/security-group-parser
docs/readme-update
```

---

# Coding Guidelines

Please follow these guidelines:

- Follow PEP 8
- Write clear and descriptive variable names
- Keep functions focused on a single responsibility
- Prefer modular code over large functions
- Add comments where necessary
- Preserve the existing project architecture

---

# Commit Message Convention

Use Conventional Commits.

Examples:

```text
feat: add IAM drift detection

fix: resolve security group normalization bug

refactor: simplify EC2 scanner

docs: update architecture documentation

test: add parser unit tests
```

---

# Pull Request Guidelines

Before submitting a Pull Request:

- Ensure the project runs successfully
- Verify that existing functionality is not broken
- Update documentation when required
- Keep Pull Requests focused on a single feature or fix

Provide a clear description of:

- What changed
- Why the change was made
- Any limitations or known issues

---

# Code Review

All Pull Requests may be reviewed for:

- Code quality
- Maintainability
- Project architecture
- Performance
- Documentation

Constructive feedback is encouraged throughout the review process.

---

# Reporting Issues

When creating an issue, please include:

- Operating System
- Python Version
- Terraform Version
- AWS Region
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if applicable)

Providing complete information helps reproduce and resolve issues more efficiently.

---

# Feature Requests

Feature requests are welcome.

Please include:

- Problem statement
- Proposed solution
- Expected benefits
- Possible implementation approach (optional)

---

# Areas Open for Contribution

Current high-priority areas include:

- AWS resource coverage expansion
- Azure support
- Google Cloud support
- HTML report generation
- JSON report export
- Multi-threaded scanning
- Unit and integration testing
- Performance optimization

---

# Code of Conduct

Please be respectful and constructive in all interactions.

Treat all contributors with professionalism and collaborate in good faith.

---

# Thank You

Every contribution—whether it's code, documentation, bug reports, or suggestions—helps improve DriftGuard.

Thank you for contributing to the project.
