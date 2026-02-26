# PCI DSS Segmentation Validator

## Overview
This tool validates network segmentation for PCI DSS Requirement 1.2.1, ensuring the Cardholder Data Environment (CDE) is isolated from non-CDE systems. It ingests inventory, network rules, and exceptions, then generates audit-ready reports.

## Setup
```bash
git clone https://github.com/martinboratto/pci_segmentation_validator.git
cd pci_segmentation_validator
```
Dependencies
```
python3 -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows

pip install -r requirements.txt
```

## Dependencies:
- Python 3.9+
- No external libraries required (uses stdlib)

## Usage
Run validator with sample data:
```bash
python main.py --format markdown
python main.py --format html
```

And in your ```main.py```:
```
# pci_segmentation_validator/main.py
import argparse
import json
from validator import SegmentationValidator
from report_generator import CombinedReportGenerator

def load_file(path):
    with open(path) as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="PCI DSS Segmentation Validator")
    parser.add_argument("--format", choices=["markdown", "html"], default="markdown",
                        help="Output format for the report")
    args = parser.parse_args()

    cde_inventory = load_file("cde_inventory.json")
    network_rules = load_file("network_rules.json")
    exceptions = load_file("allowed_exceptions.json")

    validator = SegmentationValidator(cde_inventory, network_rules, exceptions)
    results = validator.run_validation()

    report = CombinedReportGenerator(results)
    report.generate(format=args.format, filename="audit_report")

if __name__ == "__main__":
    main()

```


Example Output
See sample_output/audit_report.md and sample_output/audit_report.html

# PCI DSS Segmentation Validation Report
**Generated:** 2026-02-26 18:20:00

## Executive Summary
- Total rules analyzed: 30
- Segmentation compliance: 82%
- Critical findings: 3

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
- Red: Critical findings
- Green: Correct workflows
- Blue: Approved exceptions
- Gray: Ambiguities and/or for manual review.

