# pci_segmentation_validator/report.py
from datetime import datetime

class ReportGenerator:
    def __init__(self, results):
        self.results = results

    def generate_markdown(self, filename):
        with open(filename, "w") as f:
            f.write(self._build_report())

    def _build_report(self):
        total_rules = (
            len(self.results["violations"]) +
            len(self.results["compliant_flows"]) +
            len(self.results["exceptions"]) +
            len(self.results["ambiguities"])
        )
        compliant_count = len(self.results["compliant_flows"]) + len(self.results["exceptions"])
        compliance_pct = round((compliant_count / total_rules) * 100, 2) if total_rules else 0

        report = []
        report.append(f"# PCI DSS Segmentation Validation Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("## Executive Summary\n")
        report.append(f"- Total rules analyzed: {total_rules}")
        report.append(f"- Segmentation compliance: {compliance_pct}%")
        report.append(f"- Critical findings: {sum(1 for v in self.results['violations'] if v['risk'] == 'Critical')}\n")

        # Violations
        report.append("## Violations\n")
        if self.results["violations"]:
            for v in self.results["violations"]:
                report.append(f"- **Rule {v['rule_id']}**: {v['reason']} "
                              f"(Source: {v['source']} → Destination: {v['destination']} Port {v['port']}) "
                              f"Requirement: {v['requirement']} | Risk: {v['risk']}")
                report.append(f"  - Remediation: Restrict or remove offending rule.\n")
        else:
            report.append("No violations detected.\n")

        # Compliant Flows
        report.append("## Compliant Flows\n")
        if self.results["compliant_flows"]:
            for c in self.results["compliant_flows"]:
                report.append(f"- Rule {c['id']} allows {c['source']} → {c['destination']} "
                              f"on port {c['port']} ({c['provider']}) — Compliant")
        else:
            report.append("No compliant flows detected.\n")

        # Exceptions
        report.append("\n## Exceptions\n")
        if self.results["exceptions"]:
            for e in self.results["exceptions"]:
                report.append(f"- Rule {e['rule_id']} ({e['source']} → {e['destination']} Port {e['port']}) "
                              f"Status: {e['status']}")
        else:
            report.append("No active exceptions.\n")

        # Ambiguities
        report.append("\n## Ambiguities (Requires Manual Review)\n")
        if self.results["ambiguities"]:
            for a in self.results["ambiguities"]:
                report.append(f"- Rule {a['rule_id']} ({a['source']} → {a['destination']}) "
                              f"Reason: {a['reason']}")
        else:
            report.append("No ambiguous cases flagged.\n")

        return "\n".join(report)
