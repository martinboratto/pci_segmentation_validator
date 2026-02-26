# pci_segmentation_validator/validator.py
import datetime

class SegmentationValidator:
    def __init__(self, cde_inventory, network_rules, exceptions):
        self.cde_inventory = {s["id"]: s for s in cde_inventory["systems"]}
        self.rules = network_rules["rules"]
        self.exceptions = exceptions["exceptions"]

    def run_validation(self):
        results = {
            "violations": [],
            "compliant_flows": [],
            "exceptions": [],
            "ambiguities": []
        }

        for rule in self.rules:
            src = rule["source"]
            dst = rule["destination"]
            action = rule["action"]
            port = rule["port"]

            src_status = self.cde_inventory.get(src, {}).get("cde_status", "unknown")
            dst_status = self.cde_inventory.get(dst, {}).get("cde_status", "unknown")

            # Check if rule matches an exception
            if self.is_exception(src, dst, port):
                results["exceptions"].append({
                    "rule_id": rule["id"],
                    "source": src,
                    "destination": dst,
                    "port": port,
                    "status": "Compliant (Exception)"
                })
                continue

            # Inbound CDE traffic
            if dst_status == "in_cde":
                if src_status == "out_of_cde" and action == "allow":
                    results["violations"].append(self.violation(rule, "1.2.1", "Critical",
                        "Non-CDE system has inbound access to CDE"))
                elif rule["source"] in ["0.0.0.0/0", "10.0.0.0/8"]:
                    results["violations"].append(self.violation(rule, "1.2.1", "Critical",
                        "Overly permissive inbound rule to CDE"))
                else:
                    results["compliant_flows"].append(rule)

            # Outbound CDE traffic
            elif src_status == "in_cde" and dst_status == "out_of_cde" and action == "allow":
                results["violations"].append(self.violation(rule, "1.2.1", "High",
                    "CDE system initiates outbound connection to non-CDE"))

            # Ambiguity handling
            elif "monitoring" in src or "logging" in src:
                results["ambiguities"].append({
                    "rule_id": rule["id"],
                    "source": src,
                    "destination": dst,
                    "reason": "Monitoring/logging traffic requires manual review"
                })

        return results

    def is_exception(self, src, dst, port):
        for ex in self.exceptions:
            if ex["source"] == src and ex["destination"] == dst and ex["port"] == port:
                expiry = datetime.datetime.strptime(ex["expires"], "%Y-%m-%d")
                if expiry > datetime.datetime.now():
                    return True
        return False

    def violation(self, rule, requirement, risk, reason):
        return {
            "rule_id": rule["id"],
            "source": rule["source"],
            "destination": rule["destination"],
            "port": rule["port"],
            "requirement": requirement,
            "risk": risk,
            "reason": reason
        }
