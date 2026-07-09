# Performance Engineering FAQ

## Overview

This document explains the performance-related design decisions made while building DriftGuard and discusses how the application can scale to larger production environments.

---

# Resource Selection

## 1. Why does DriftGuard ask the user to select a resource type first?

Large cloud environments contain hundreds or thousands of resources.

Selecting the resource type first significantly reduces unnecessary parsing and AWS API calls.

This improves execution speed and provides a better user experience.

---

## 2. Why allow scanning a single resource?

Production investigations rarely require scanning every resource.

Most incidents involve a specific EC2 instance, Security Group, or S3 bucket.

Scanning a single resource minimizes API calls and reduces execution time.

---

## 3. Why provide an option to scan all resources?

Bulk scanning is useful during:

- Security audits
- Compliance checks
- Infrastructure reviews
- Pre-deployment validation

Users can choose between targeted investigations and complete resource validation.

---

## 4. Why not scan every resource automatically?

Automatically scanning every supported resource would:

- Increase execution time
- Generate unnecessary AWS API calls
- Slow down investigations
- Consume more AWS API quota

Resource-specific scanning is more efficient.

---

## AWS API Performance

## 5. How does DriftGuard reduce AWS API calls?

DriftGuard only queries resources that exist inside the selected Terraform State.

It never scans the entire AWS account.

---

## 6. Why parse Terraform State before calling AWS APIs?

Terraform State already contains the resource identifiers.

Using these identifiers allows DriftGuard to directly query the required resources instead of listing every resource from AWS.

---

## 7. How many AWS API calls are performed?

The number depends on:

- Selected resource type
- Number of selected resources

Scanning a single EC2 instance typically requires only one or two API calls.

---

## 8. Does DriftGuard scan unused AWS resources?

No.

Only resources managed by the supplied Terraform State are scanned.

Resources outside Terraform management are ignored.

---

## Execution Speed

## 9. What affects execution time?

Execution time mainly depends on:

- Number of resources
- AWS API latency
- Network latency
- Resource type
- AWS throttling

---

## 10. Why is the current implementation sequential?

Sequential execution keeps the implementation simple, deterministic, and easier to debug.

Correctness was prioritized before introducing concurrency.

---

## 11. Would multithreading improve performance?

Yes.

Independent AWS API requests can be executed concurrently.

Future versions may use:

- ThreadPoolExecutor
- asyncio
- multiprocessing

depending on the workload.

---

## 12. Would asynchronous execution help?

Yes.

Since most execution time is spent waiting for AWS API responses, asynchronous requests can significantly reduce overall scan time.

---

## 13. Why wasn't concurrency implemented initially?

The first objective was to build a correct and modular architecture.

Performance optimizations can be added later without changing the system design.

---

# Scalability

## 14. How would DriftGuard handle 1,000 EC2 instances?

The architecture already supports this.

Performance improvements would include:

- Parallel scanning
- Resource batching
- Progress tracking
- Worker pools

---

## 15. How would you support 10,000+ resources?

Future optimizations may include:

- Thread pools
- Pagination
- Cached API responses
- Batch processing
- Distributed workers

---

## 16. How would you avoid AWS API throttling?

Possible strategies include:

- Request throttling
- Exponential backoff
- Retry mechanisms
- API batching
- Configurable concurrency limits

---

## 17. How would you improve scan performance?

Potential optimizations include:

- Multi-threading
- Async execution
- Connection pooling
- API response caching
- Efficient data structures

---

## 18. Can DriftGuard scan multiple AWS accounts simultaneously?

Not currently.

Future versions could execute account-specific scans concurrently using assumed IAM roles.

---

## 19. Can DriftGuard scan multiple regions?

Current implementation targets one configured region.

Future versions may execute region scans in parallel.

---

## Memory & Processing

## 20. Does DriftGuard load the entire AWS account into memory?

No.

Only the selected Terraform resources are loaded and processed.

This keeps memory usage low.

---

## 21. How is memory usage minimized?

Memory consumption is reduced by:

- Parsing only selected resources
- Using lightweight dictionaries
- Avoiding unnecessary object creation
- Processing resources independently

---

## 22. Could caching improve performance?

Yes.

Caching repeated AWS API responses would reduce duplicate requests during large scans.

---

## Production Considerations

## 23. Is DriftGuard suitable for production environments?

Yes.

Its read-only architecture and targeted scanning make it safe for production investigations.

---

## 24. How would you schedule periodic scans?

Future implementations could integrate with:

- GitHub Actions
- Jenkins
- Cron Jobs
- AWS Lambda
- EventBridge

to automate drift detection.

---

## 25. Could DriftGuard support continuous monitoring?

Yes.

A future monitoring mode could periodically scan infrastructure and notify engineers when new drift is detected.

---

## 26. How would you generate reports for large infrastructures?

Future reporting enhancements may include:

- Streaming reports
- Incremental report generation
- HTML dashboards
- JSON exports
- Database-backed history

---

## Design Decisions

## 27. Why optimize resource selection instead of comparison logic?

Comparison operations are computationally inexpensive.

The real bottleneck is network communication with AWS APIs.

Reducing unnecessary API calls has a much greater impact on performance.

---

## 28. What is the biggest performance bottleneck?

The largest bottleneck is AWS API latency, not Python execution.

Optimizing API usage provides the greatest performance improvements.

---

## 29. What performance optimization would you implement first?

The highest-impact improvement would be parallel AWS API requests using a configurable thread pool.

This would significantly reduce scan time for large infrastructures.

---

## 30. What would Performance Version 2 look like?

Performance-focused enhancements would include:

- Parallel scanning
- Async AWS requests
- Worker pools
- API response caching
- Progress indicators
- Scan metrics
- Multi-account scanning
- Multi-region scanning
- Incremental drift detection
- Performance benchmarking
