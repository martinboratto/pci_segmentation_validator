# PCI DSS Segmentation Validator

## Overview
This tool validates network segmentation for PCI DSS Requirement 1.2.1, ensuring the Cardholder Data Environment (CDE) is isolated from non-CDE systems. It ingests inventory, network rules, and exceptions, then generates audit-ready reports.

## Setup
```bash
git clone <repo-url>
cd pci_segmentation_validator
pip install -r requirements.txt
