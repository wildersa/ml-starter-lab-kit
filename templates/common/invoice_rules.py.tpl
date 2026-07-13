def validate_invoice(extraction, config):
    invoice_id = extraction.get("invoice_id", "unknown")
    tolerance = config.get("validation", {}).get("tolerance_percent", 2.0)

    rules_results = []
    status = "passed"

    # Rule 1: Required fields
    required_fields = config.get("validation", {}).get("required_fields", ["supplier", "total_amount", "currency", "issue_date"])
    missing = [f for f in required_fields if not extraction.get(f)]
    if missing:
        rules_results.append({
            "rule_id": "required_fields_exist",
            "severity": "blocker",
            "status": "failed",
            "message": f"Missing required fields: {', '.join(missing)}"
        })
        status = "blocked"
    else:
        rules_results.append({
            "rule_id": "required_fields_exist",
            "severity": "blocker",
            "status": "passed",
            "message": "All required fields are present."
        })

    # Rule 2: Item sum matches total
    total_amount = extraction.get("total_amount", 0)
    items = extraction.get("items", [])
    items_sum = sum(item.get("total_amount", 0) for item in items)

    diff = abs(total_amount - items_sum)
    allowed_diff = total_amount * (tolerance / 100.0)

    if diff > allowed_diff:
        rules_results.append({
            "rule_id": "sum_matches_total",
            "severity": "blocker",
            "status": "failed",
            "message": f"Items sum ({items_sum}) differs from total ({total_amount}) by {diff}, which is above tolerance ({allowed_diff})."
        })
        status = "blocked"
    else:
        rules_results.append({
            "rule_id": "sum_matches_total",
            "severity": "blocker",
            "status": "passed",
            "message": f"Items sum ({items_sum}) matches total ({total_amount}) within tolerance."
        })

    # Rule 3: Low confidence fields
    low_confidence = [i for i in items if i.get("confidence", 1.0) < 0.8]
    if low_confidence:
        rules_results.append({
            "rule_id": "high_confidence_extraction",
            "severity": "warning",
            "status": "failed",
            "message": f"Found {len(low_confidence)} items with low extraction confidence (< 80%)."
        })
        if status == "passed":
            status = "warning"
    else:
        rules_results.append({
            "rule_id": "high_confidence_extraction",
            "severity": "warning",
            "status": "passed",
            "message": "All items have high extraction confidence."
        })

    return {
        "invoice_id": invoice_id,
        "status": status,
        "tolerance_percent": tolerance,
        "rules": rules_results
    }
