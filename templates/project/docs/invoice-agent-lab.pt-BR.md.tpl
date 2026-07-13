# Lab: Azure Document AI Invoice Agent

Este lab demonstra um scaffold local para uma solução de reconciliação de faturas usando o padrão:
**Extração → Validação → Auditoria de Agente → Rascunho de Saída ERP**.

## 1. Visão Geral da Arquitetura

```mermaid
flowchart TD
    INPUT[Documento de fatura de amostra] --> EXTRACT[Contrato de extração]
    EXTRACT --> RULES[Regras de validação determinísticas]
    RULES --> AGENT[Ferramentas de reconciliação assistida por agente]
    AGENT --> DOSSIER[Dossiê de revisão humana]
    RULES --> GATE{Dentro da tolerância e sem bloqueios?}
    GATE -->|Sim| AUTO[Rascunho auto-autorizado]
    GATE -->|Não| HITL[Revisão humana necessária]
    AUTO --> ERP[Rascunho de saída ERP]
    HITL --> DOSSIER
```

## 2. Componentes Principais

- **Contrato de Extração:** Formato JSON padronizado para dados de faturas (normalizado a partir de OCR).
- **Regras Determinísticas:** Lógica de aprovação baseada em regras de negócio claras (ex: as somas devem bater).
- **Auditoria de Agente:** Um assistente de IA que explica divergências e constrói um dossiê de reconciliação.
- **Saída ERP:** Um payload final autorizado pronto para sistemas de contabilidade.

## 3. Demo Local

Execute a demo local para ver o pipeline em ação:

```bash
python -m {{PACKAGE_NAME}}.lab invoice-agent demo
```

Este comando irá:
1. Carregar uma extração de fatura de amostra de `data/samples/invoices/`.
2. Executar as regras de validação definidas em `src/{{PACKAGE_NAME}}/invoice_rules.py`.
3. Simular uma auditoria de agente usando ferramentas em `src/{{PACKAGE_NAME}}/invoice_agent_tools.py`.
4. Gerar artefatos no diretório `reports/`:
   - `invoice-validation-result-sample-001.json`
   - `invoice-agent-dossier-sample-001.json`
   - `invoice-agent-dossier-sample-001.md` (Legível por humanos)
   - `erp-output-draft-sample-001.json` (Apenas se autorizado)

## 4. Futura Integração com Azure

Em um ambiente de produção:
- **Extração** pode ser tratada pelo **Azure AI Document Intelligence**.
- **Auditoria de Agente** pode ser alimentada pelo **Azure AI Foundry Agent Service**.
- **Workflow** pode ser orquestrado usando **Azure Durable Functions**.

---
*Nota: Este é um scaffold educacional. Ele usa simulação determinística local e não requer credenciais Azure para ser executado.*
