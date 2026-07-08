{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ERP Output Draft",
  "type": "object",
  "properties": {
    "erp_output_id": { "type": "string" },
    "invoice_id": { "type": "string" },
    "authorization_status": { "enum": ["auto_authorize", "human_approved"] },
    "items": { "type": "array" },
    "created_at": { "type": "string" }
  }
}
