# Design Decisions & Compliance Reasoning

## Interpretation of "Necessary Traffic" in PCI DSS 1.2.1
We interpreted "necessary traffic" as strictly the flows required to support payment processing, tokenization, and compliance monitoring. For inbound traffic, only connections from merchant-facing APIs, load balancers, or other CDE systems are considered necessary. Outbound traffic from the CDE is limited to approved destinations such as SIEM collectors or monitoring agents. Any rule that allows broad access (e.g., 0.0.0.0/0 or entire VPC ranges) is automatically flagged as a violation. This interpretation aligns with the principle of least privilege and ensures that only business-critical flows are permitted.

## Assumptions About CDE Scope
We assumed that any system handling raw PAN data, even temporarily, is part of the CDE. This includes hybrid services such as the 3DS authentication service, which decrypts PANs for verification. Systems that only handle tokenized data, such as analytics databases or merchant dashboards, were classified as out-of-CDE. Monitoring agents and logging services were treated as out-of-CDE but their traffic into the CDE was considered ambiguous. These flows were either flagged for manual review or handled via approved exceptions. This approach minimizes CDE scope while still recognizing operational realities.

## Handling Conflicts Between PCI DSS and Data Minimization
PCI DSS requires logging and monitoring of CDE systems, but data minimization principles discourage unnecessary data flows. To balance these, the tool does not automatically fail monitoring or logging traffic. Instead, such flows are flagged as "Requires Manual Review." This ensures that compliance teams can justify the necessity of these flows while maintaining awareness of potential data minimization risks. Approved exceptions (e.g., Prometheus scraping or SIEM logging) are marked as compliant but tracked with expiration dates to prevent indefinite scope creep.

## Edge Cases and Manual Review
The tool handles several edge cases:
- **Expired exceptions**: flagged as violations.
- **Overly permissive CIDRs** (0.0.0.0/0, 10.0.0.0/8): flagged as critical violations.
- **Unknown systems** in rules: flagged for manual review since their CDE status is unclear.
- **Hybrid systems**: treated as in-CDE when handling raw PAN, otherwise out-of-CDE.
- **Monitoring/logging flows**: flagged as ambiguous unless explicitly approved.

This nuanced handling reflects the reality that compliance is not binary and requires human judgment.

## Future Enhancements
With more time, we would add:
- **Multi-cloud raw config ingestion**: parsing AWS Security Group JSON, GCP Firewall exports, and Kubernetes NetworkPolicies directly.
- **Segmentation scoring**: assigning each system a risk score (0–100) based on violations, exceptions, and overly broad rules, with a "Top 10 riskiest systems" list.
- **Continuous monitoring mode**: a `--watch` flag that re-runs validation on every infrastructure change and alerts when segmentation breaks.
- **PDF/HTML export**: polished reports with tables and severity color-coding for auditors.

These additions would make the tool more robust, proactive, and auditor-friendly, ensuring ongoing compliance and reducing manual effort.

