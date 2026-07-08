def build_approval_dossier(extraction, validation_result):
    invoice_id = extraction.get("invoice_id")
    status = validation_result.get("status")

    # Simple deterministic agent simulation
    summary = f"Agent audit for invoice {invoice_id} from {extraction.get('supplier')}."
    explanations = []
    tool_calls = ["get_invoice_extraction", "get_validation_results"]

    if status == "passed":
        recommended_action = "auto_authorize"
        explanations.append("The invoice passed all deterministic validation rules.")
    elif status == "warning":
        recommended_action = "human_review"
        explanations.append("The invoice has warnings (e.g. low confidence) and requires human review.")
    else:
        recommended_action = "reject"
        explanations.append("The invoice is blocked due to critical validation failures.")

    return {
        "dossier_id": f"dossier-{invoice_id}",
        "invoice_id": invoice_id,
        "summary": summary,
        "recommended_action": recommended_action,
        "explanations": explanations,
        "evidence_refs": [item.get("evidence_ref") for item in extraction.get("items", []) if item.get("evidence_ref")],
        "tool_calls": tool_calls
    }

def format_dossier_md(dossier):
    md = [
        f"# Invoice Agent Dossier: {dossier['invoice_id']}",
        "",
        f"**Dossier ID:** {dossier['dossier_id']}",
        f"**Recommended Action:** `{dossier['recommended_action']}`",
        "",
        "## Summary",
        dossier['summary'],
        "",
        "## Explanations",
    ]
    for exp in dossier['explanations']:
        md.append(f"- {exp}")

    md.append("")
    md.append("## Tool Calls Simulated")
    for tool in dossier['tool_calls']:
        md.append(f"- `{tool}()`")

    return "\n".join(md)
