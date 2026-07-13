{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Validation Result",
  "type": "object",
  "properties": {
    "invoice_id": { "type": "string" },
    "status": { "enum": ["passed", "warning", "blocked"] },
    "tolerance_percent": { "type": "number" },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule_id": { "type": "string" },
          "severity": { "enum": ["info", "warning", "blocker"] },
          "status": { "enum": ["passed", "failed"] },
          "message": { "type": "string" }
        }
      }
    }
  }
}
