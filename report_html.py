# pci_segmentation_validator/report_html.py
from datetime import datetime

class HTMLReportGenerator:
    def __init__(self, results):
        self.results = results

    def generate_html(self, filename):
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

        # CSS for styling
        css = """
        <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
        .critical { background-color: #e74c3c; color: white; }
        .high { background-color: #e67e22; color: white; }
        .medium { background-color: #f1c40f; }
        .low { background-color: #2ecc71; color: white; }
        .compliant { background-color: #27ae60; color: white; }
        .exception { background-color: #2980b9; color: white; }
        .ambiguous { background-color: #95a5a6; color: white; }
        </style>
        """

        html = [f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>PCI DSS Segmentation Report</title>{css}</head><body>"]
        html.append("<h1>PCI DSS Segmentation Validation Report</h1>")
        html.append(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

        # Executive Summary
        html.append("<h2>Executive Summary</h2>")
        html.append("<ul>")
        html.append(f"<li>Total rules analyzed: {total_rules}</li>")
        html.append(f"<li>Segmentation compliance: {compliance_pct}%</li>")
        html.append(f"<li>Critical findings: {sum(1 for v in self.results['violations'] if v['risk'] == 'Critical')}</li>")
        html.append("</ul>")

        # Violations Table
        html.append("<h2>Violations</h2>")
        if self.results["violations"]:
            html.append("<table><tr><th>Rule ID</th><th>Source</th><th>Destination</th><th>Port</th><th>Requirement</th><th>Risk</th><th>Reason</th><th>Remediation</th></tr>")
            for v in self.results["violations"]:
                risk_class = v["risk"].lower()
                html.append(f"<tr class='{risk_class}'><td>{v['rule_id']}</td><td>{v['source']}</td><td>{v['destination']}</td><td>{v['port']}</td><td>{v['requirement']}</td><td>{v['risk']}</td><td>{v['reason']}</td><td>Restrict or remove offending rule</td></tr>")
            html.append("</table>")
        else:
            html.append("<p>No violations detected.</p>")

        # Compliant Flows Table
        html.append("<h2>Compliant Flows</h2>")
        if self.results["compliant_flows"]:
            html.append("<table><tr><th>Rule ID</th><th>Source</th><th>Destination</th><th>Port</th><th>Provider</th></tr>")
            for c in self.results["compliant_flows"]:
                html.append(f"<tr class='compliant'><td>{c['id']}</td><td>{c['source']}</td><td>{c['destination']}</td><td>{c['port']}</td><td>{c['provider']}</td></tr>")
            html.append("</table>")
        else:
            html.append("<p>No compliant flows detected.</p>")

        # Exceptions Table
        html.append("<h2>Exceptions</h2>")
        if self.results["exceptions"]:
            html.append("<table><tr><th>Rule ID</th><th>Source</th><th>Destination</th><th>Port</th><th>Status</th></tr>")
            for e in self.results["exceptions"]:
                html.append(f"<tr class='exception'><td>{e['rule_id']}</td><td>{e['source']}</td><td>{e['destination']}</td><td>{e['port']}</td><td>{e['status']}</td></tr>")
            html.append("</table>")
        else:
            html.append("<p>No active exceptions.</p>")

        # Ambiguities Table
        html.append("<h2>Ambiguities (Requires Manual Review)</h2>")
        if self.results["ambiguities"]:
            html.append("<table><tr><th>Rule ID</th><th>Source</th><th>Destination</th><th>Reason</th></tr>")
            for a in self.results["ambiguities"]:
                html.append(f"<tr class='ambiguous'><td>{a['rule_id']}</td><td>{a['source']}</td><td>{a['destination']}</td><td>{a['reason']}</td></tr>")
            html.append("</table>")
        else:
            html.append("<p>No ambiguous cases flagged.</p>")

        html.append("</body></html>")
        return "".join(html)
