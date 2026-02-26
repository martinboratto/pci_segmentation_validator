# pci_segmentation_validator/report_generator.py
from datetime import datetime
from report import ReportGenerator
from report_html import HTMLReportGenerator

class CombinedReportGenerator:
    def __init__(self, results):
        self.results = results

    def generate(self, format="markdown", filename="audit_report"):
        if format == "markdown":
            generator = ReportGenerator(self.results)
            generator.generate_markdown(f"{filename}.md")
            print(f"Markdown report saved to {filename}.md")
        elif format == "html":
            generator = HTMLReportGenerator(self.results)
            generator.generate_html(f"{filename}.html")
            print(f"HTML report saved to {filename}.html")
        else:
            raise ValueError("Unsupported format. Use 'markdown' or 'html'.")
