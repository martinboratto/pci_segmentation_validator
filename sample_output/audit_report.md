# PCI DSS Segmentation Validation Report
**Generated:** 2026-02-26 18:20:00

## Executive Summary
- Total rules analyzed: 30
- Segmentation compliance: 82%
- Critical findings: 3

## Violations
- **Rule sg-aws-payment-api-inbound**: Overly permissive inbound rule to CDE  
  (Source: 0.0.0.0/0 → Destination: payment-api-prod Port 443)  
  Requirement: 1.2.1 | Risk: Critical  
  - Remediation: Restrict source to CDE IP range

- **Rule logging-to-vault**: Outbound CDE traffic to non-CDE logging system  
  (Source: logging-service → Destination: tokenization-vault Port 9200)  
  Requirement: 1.2.1 | Risk: High  
  - Remediation: Route logs via approved SIEM collector

- **Rule corp-laptop-to-vault**: Corporate endpoint accessing CDE database  
  (Source: employee-laptop → Destination: tokenization-vault Port 3306)  
  Requirement: 1.2.1 | Risk: Critical  
  - Remediation: Block workstation access to CDE

## Compliant Flows
- Rule gcp-analytics-to-vault allows analytics-db → tokenization-vault  
  on port 5432 (gcp_firewall) — Compliant

- Rule fraud-to-3ds allows fraud-detection → 3ds-auth-service  
  on port 443 (gcp_firewall) — Compliant

## Exceptions
- Rule monitoring-agent-exception (monitoring-agent → payment-api-prod Port 9090)  
  Status: Compliant (Exception)  
  Justification: Prometheus metrics scraping for SOC 2 monitoring  
  Approved by: CISO | Expires: 2025-12-31

## Ambiguities (Requires Manual Review)
- Rule corp-laptop-to-vault flagged for manual review  
  Reason: Unclear if corporate endpoints should access CDE

- Rule siem-collector-to-vault flagged for manual review  
  Reason: Logging traffic may be necessary but conflicts with data minimization

