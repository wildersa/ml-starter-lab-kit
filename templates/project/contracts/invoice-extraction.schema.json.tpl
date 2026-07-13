{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Invoice Extraction",
  "type": "object",
  "properties": {
    "invoice_id": { "type": "string" },
    "supplier": { "type": "string" },
    "invoice_number": { "type": "string" },
    "issue_date": { "type": "string" },
    "due_date": { "type": "string" },
    "total_amount": { "type": "number" },
    "currency": { "type": "string" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_id": { "type": "string" },
          "description": { "type": "string" },
          "quantity": { "type": "number" },
          "unit_amount": { "type": "number" },
          "total_amount": { "type": "number" },
          "confidence": { "type": "number" },
          "evidence_ref": { "type": "string" }
        }
      }
    }
  }
}
