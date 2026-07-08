{
  "project": {
    "name": "{{PROJECT_NAME}}",
    "lab": "invoice_agent"
  },
  "validation": {
    "tolerance_percent": 2.0,
    "required_fields": [
      "supplier",
      "total_amount",
      "currency",
      "issue_date"
    ]
  },
  "agent": {
    "mode": "deterministic_simulation",
    "auto_authorize_on_passed": true
  }
}
