import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from .core.config import project_root
from . import invoice_rules
from . import invoice_agent_tools
from . import erp_output

def load_extraction(invoice_path: Path):
    with open(invoice_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_pipeline(invoice_id: str = "sample-001", config_path: str = "configs/invoice_agent_config.json"):
    root = project_root()
    config_full_path = root / config_path

    with open(config_full_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    invoice_path = root / f"data/samples/invoices/{invoice_id}.json"
    if not invoice_path.exists():
        # Fallback to the one in template if not found by id
        invoice_path = root / "data/samples/invoices/sample_invoice.json"

    print(f"\n>>> Loading invoice extraction: {invoice_path.name}")
    extraction = load_extraction(invoice_path)

    print(">>> Running deterministic validation rules...")
    validation_result = invoice_rules.validate_invoice(extraction, config)

    # Save validation result
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    validation_path = reports_dir / f"invoice-validation-result-{invoice_id}.json"
    with open(validation_path, "w", encoding="utf-8") as f:
        json.dump(validation_result, f, indent=2)
    print(f"    Artifact: {validation_path.relative_to(root)}")

    print(">>> Running agent-assisted reconciliation simulation...")
    dossier = invoice_agent_tools.build_approval_dossier(extraction, validation_result)

    # Save dossier (JSON and MD)
    dossier_json_path = reports_dir / f"invoice-agent-dossier-{invoice_id}.json"
    with open(dossier_json_path, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2)

    dossier_md_path = reports_dir / f"invoice-agent-dossier-{invoice_id}.md"
    with open(dossier_md_path, "w", encoding="utf-8") as f:
        f.write(invoice_agent_tools.format_dossier_md(dossier))

    print(f"    Artifact: {dossier_json_path.relative_to(root)}")
    print(f"    Artifact: {dossier_md_path.relative_to(root)}")

    # ERP Output Draft
    if dossier["recommended_action"] in ["auto_authorize", "human_approved"]:
        print(">>> Generating ERP output draft...")
        erp_draft = erp_output.generate_draft(extraction, dossier)
        erp_path = reports_dir / f"erp-output-draft-{invoice_id}.json"
        with open(erp_path, "w", encoding="utf-8") as f:
            json.dump(erp_draft, f, indent=2)
        print(f"    Artifact: {erp_path.relative_to(root)}")
    else:
        print(">>> ERP output draft skipped (invoice blocked or requires review).")

def main():
    parser = argparse.ArgumentParser(description="Invoice Agent Pipeline")

    # Strip 'invoice-agent' command if called from lab.py
    argv = sys.argv[1:]
    if argv and argv[0] == "invoice-agent":
        argv = argv[1:]

    parser.add_argument("command", choices=["demo", "run", "dossier"], help="Command to run")
    parser.add_argument("--invoice-id", default="sample-001", help="Invoice ID to process")
    parser.add_argument("--config", default="configs/invoice_agent_config.json", help="Path to config file")

    args = parser.parse_args(argv)

    if args.command == "demo":
        run_pipeline("sample-001")
    elif args.command == "run":
        run_pipeline(args.invoice_id, args.config)
    elif args.command == "dossier":
        # For dossier command, we could just run the pipeline or show existing
        run_pipeline(args.invoice_id, args.config)

if __name__ == "__main__":
    main()
