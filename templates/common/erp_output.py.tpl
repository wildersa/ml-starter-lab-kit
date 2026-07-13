from datetime import datetime

def generate_draft(extraction, dossier):
    return {
        "erp_output_id": f"erp-{extraction.get('invoice_id')}",
        "invoice_id": extraction.get("invoice_id"),
        "authorization_status": dossier["recommended_action"],
        "supplier": extraction.get("supplier"),
        "total_amount": extraction.get("total_amount"),
        "currency": extraction.get("currency"),
        "items": extraction.get("items", []),
        "created_at": datetime.now().isoformat()
    }
