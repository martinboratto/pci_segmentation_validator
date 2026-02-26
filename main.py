# pci_segmentation_validator/main.py
import json
from validator import SegmentationValidator
from report import ReportGenerator

def load_file(path):
    with open(path) as f:
        return json.load(f)

def main():
    cde_inventory = load_file("cde_inventory.json")
    network_rules = load_file("network_rules.json")
    exceptions = load_file("allowed_exceptions.json")

    validator = SegmentationValidator(cde_inventory, network_rules, exceptions)
    results = validator.run_validation()

    report = ReportGenerator(results)
    report.generate_markdown("audit_report.md")

if __name__ == "__main__":
    main()
