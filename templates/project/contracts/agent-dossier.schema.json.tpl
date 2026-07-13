{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Dossier",
  "type": "object",
  "properties": {
    "dossier_id": { "type": "string" },
    "invoice_id": { "type": "string" },
    "summary": { "type": "string" },
    "recommended_action": { "enum": ["auto_authorize", "human_review", "correction_required", "reject"] },
    "explanations": { "type": "array", "items": { "type": "string" } },
    "evidence_refs": { "type": "array", "items": { "type": "string" } },
    "tool_calls": { "type": "array", "items": { "type": "string" } }
  }
}
