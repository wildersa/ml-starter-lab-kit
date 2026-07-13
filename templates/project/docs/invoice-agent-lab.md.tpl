# Azure Document AI Invoice Agent Lab

This lab demonstrates a local-first scaffold for an invoice reconciliation solution using the pattern:
**Extraction → Validation → Agent Audit → ERP Output Draft**.

## 1. Architecture Overview

```mermaid
flowchart TD
    INPUT[Sample invoice document] --> EXTRACT[Extraction contract]
    EXTRACT --> RULES[Deterministic validation rules]
    RULES --> AGENT[Agent-assisted reconciliation tools]
    AGENT --> DOSSIER[Human review dossier]
    RULES --> GATE{Within tolerance and no blockers?}
    GATE -->|Yes| AUTO[Auto-authorized draft]
    GATE -->|No| HITL[Human review required]
    AUTO --> ERP[ERP output draft]
    HITL --> DOSSIER
```

## 2. Key Components

- **Extraction Contract:** Standardized JSON format for invoice data (normalized from OCR).
- **Deterministic Rules:** Approval logic owned by clear business rules (e.g., sums must match).
- **Agent Audit:** An AI assistant that explains variances and builds a reconciliation dossier.
- **ERP Output:** A final, authorized payload ready for downstream accounting systems.

## 3. Local Demo

Run the local demo to see the pipeline in action:

```bash
python -m {{PACKAGE_NAME}}.lab invoice-agent demo
```

This command will:
1. Load a sample invoice extraction from `data/samples/invoices/`.
2. Run validation rules defined in `src/{{PACKAGE_NAME}}/invoice_rules.py`.
3. Simulate an agent audit using tools in `src/{{PACKAGE_NAME}}/invoice_agent_tools.py`.
4. Generate artifacts in the `reports/` directory:
   - `invoice-validation-result-sample-001.json`
   - `invoice-agent-dossier-sample-001.json`
   - `invoice-agent-dossier-sample-001.md` (Human-readable)
   - `erp-output-draft-sample-001.json` (Only if authorized)

## 4. Future Azure Integration

In a production environment:
- **Extraction** can be handled by **Azure AI Document Intelligence**.
- **Agent Audit** can be powered by **Azure AI Foundry Agent Service**.
- **Workflow** can be orchestrated using **Azure Durable Functions**.

---
*Note: This is an educational scaffold. It uses local deterministic simulation and does not require Azure credentials to run.*
