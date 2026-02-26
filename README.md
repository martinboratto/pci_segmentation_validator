# PCI DSS Segmentation Validator

## Overview
This tool validates network segmentation for PCI DSS Requirement 1.2.1, ensuring the Cardholder Data Environment (CDE) is isolated from non-CDE systems. It ingests inventory, network rules, and exceptions, then generates audit-ready reports.

## Setup
```bash
git clone <repo-url>
cd pci_segmentation_validator
pip install -r requirements.txt

## Dependencies:
Python 3.9+
No external libraries required (uses stdlib)

## Usage
Run validator with sample data:
python main.py --format markdown
python main.py --format html


Example Output
See sample_output/audit_report.md and sample_output/audit_report.html


---

## 📑 Design Decisions & Compliance Reasoning (docs/design_decisions.md)

**Interpretation of Necessary Traffic**  
We defined “necessary” as traffic essential for payment processing, tokenization, or compliance monitoring. Monitoring agents and SIEM collectors were flagged as ambiguous, requiring manual review.

**Assumptions about CDE Scope**  
Hybrid systems (e.g., 3DS authentication) were treated as in-CDE when handling raw PAN. Monitoring agents were considered out-of-CDE but allowed exceptions.

**Conflicts Between PCI DSS and Data Minimization**  
Logging and monitoring require data flows from CDE. To balance, we flagged these as “Requires Manual Review” rather than auto-fail.

**Edge Cases**  
- Expired exceptions → flagged as violations.  
- Overly permissive CIDRs (0.0.0.0/0, 10.0.0.0/8) → Critical violations.  
- Unknown systems in rules → flagged for manual review.

**Future Enhancements**  
- Multi-cloud raw config ingestion.  
- Segmentation scoring per system.  
- Continuous monitoring mode (`--watch`).  

---

## 📊 Example Audit Report (Markdown)

