"""
Project 3: GPT-Powered Automation & AI Agent Workflow Development
Aware Custom Biometric Wearables — Enterprise Internal (Confidential)

This module demonstrates the AI Agent pipeline architecture used to automate
document intake routing, report distribution, and CRM anomaly flagging across
business units. In production, these flows run inside Azure Logic Apps and
Power Automate, triggered by Dynamics 365 CRM events.

NOTE: API keys are loaded from environment variables only.
      All sample data is synthetic.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional

# In production: pip install openai requests azure-identity
try:
    import openai
except ImportError:
    openai = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Configuration ────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "<set-in-azure-key-vault>")
DYNAMICS_API   = os.getenv("DYNAMICS365_ENDPOINT", "https://<org>.crm.dynamics.com/api/data/v9.2")
OAUTH_TOKEN    = os.getenv("DYNAMICS_OAUTH_TOKEN", "<oauth-token>")


# ═══════════════════════════════════════════════════════════════════════════
# DOCUMENT INTAKE ROUTER
# ═══════════════════════════════════════════════════════════════════════════

ROUTING_SYSTEM_PROMPT = """
You are an intelligent document routing agent for Aware Custom Biometric Wearables.
Classify the incoming document into one of the following categories:
  - DEFENSE_CONTRACT   : Military or government procurement documents
  - INDUSTRIAL_ORDER   : Industrial hearing protection purchase orders
  - HEALTHCARE_INQUIRY : Clinical trial, research, or healthcare RFP
  - FINANCE_REPORT     : Internal financial reports or invoices
  - COMPLIANCE_AUDIT   : GDPR, HIPAA, or DoD data governance documents
  - GENERAL_INQUIRY    : Any other correspondence

Respond ONLY with a JSON object in this format:
{
  "category": "<CATEGORY>",
  "confidence": <0.0-1.0>,
  "routing_team": "<team name>",
  "priority": "<HIGH|MEDIUM|LOW>",
  "summary": "<one sentence summary>"
}
"""


def classify_document(document_text: str) -> dict:
    """
    Routes an incoming document to the correct business unit using GPT.
    In production this is triggered by an email arrival event in Power Automate,
    which passes the parsed email body to this Azure Function.
    """
    if openai is None:
        logger.warning("openai not installed — returning mock classification.")
        return _mock_classification(document_text)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ROUTING_SYSTEM_PROMPT},
            {"role": "user",   "content": document_text[:4000]}
        ],
        temperature=0.1,
        max_tokens=300
    )
    raw = response.choices[0].message.content.strip()
    result = json.loads(raw)
    logger.info(f"Document classified: {result['category']} (confidence={result['confidence']})")
    return result


def _mock_classification(text: str) -> dict:
    """Returns a deterministic mock for demo/testing purposes."""
    text_lower = text.lower()
    if any(k in text_lower for k in ["army","navy","military","dod","defense","warfighter"]):
        cat, team, priority = "DEFENSE_CONTRACT", "Aware Defense Team", "HIGH"
    elif any(k in text_lower for k in ["manufacturing","industrial","osha","ppe"]):
        cat, team, priority = "INDUSTRIAL_ORDER", "Industrial Sales", "MEDIUM"
    elif any(k in text_lower for k in ["hipaa","gdpr","audit","compliance"]):
        cat, team, priority = "COMPLIANCE_AUDIT", "Data Governance", "HIGH"
    else:
        cat, team, priority = "GENERAL_INQUIRY", "Operations", "LOW"
    return {
        "category": cat, "confidence": 0.91,
        "routing_team": team, "priority": priority,
        "summary": f"Auto-classified as {cat} based on keyword analysis."
    }


# ═══════════════════════════════════════════════════════════════════════════
# SALES PIPELINE ANOMALY DETECTION
# ═══════════════════════════════════════════════════════════════════════════

ANOMALY_SYSTEM_PROMPT = """
You are a sales analytics AI for Aware Custom Biometric Wearables.
Analyze the provided sales pipeline data and identify:
1. Deals at risk of stalling (no activity > 14 days)
2. Revenue forecast gaps vs target
3. Segments showing unusual drop-off

Respond with a JSON object:
{
  "at_risk_deals": [{"deal_id": ..., "reason": ..., "recommended_action": ...}],
  "forecast_gap_usd": <number>,
  "alert_segments": ["..."],
  "summary": "..."
}
"""


def analyze_pipeline(pipeline_records: list) -> dict:
    """
    Sends CRM pipeline snapshot to GPT for anomaly detection.
    In production this runs as a daily Logic App trigger against Dynamics 365.
    """
    if openai is None:
        return _mock_anomaly_analysis(pipeline_records)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    payload = json.dumps(pipeline_records[:30], default=str)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ANOMALY_SYSTEM_PROMPT},
            {"role": "user",   "content": payload}
        ],
        temperature=0.2,
        max_tokens=600
    )
    return json.loads(response.choices[0].message.content.strip())


def _mock_anomaly_analysis(records: list) -> dict:
    stale = [r for r in records if r.get("days_since_activity", 0) > 14]
    return {
        "at_risk_deals": [{"deal_id": r.get("deal_id"), "reason": "No activity > 14 days",
                           "recommended_action": "Schedule follow-up call"} for r in stale[:3]],
        "forecast_gap_usd": round(sum(r.get("deal_value",0) for r in stale) * 0.35, 2),
        "alert_segments": list({r.get("segment","Unknown") for r in stale}),
        "summary": f"{len(stale)} deals flagged as at-risk out of {len(records)} total pipeline records."
    }


# ═══════════════════════════════════════════════════════════════════════════
# REPORT DISTRIBUTION AUTOMATION
# ═══════════════════════════════════════════════════════════════════════════

def distribute_report(report_name: str, recipients: list, trigger_event: str) -> dict:
    """
    Simulates the Power Automate flow that auto-distributes BI reports
    to stakeholders upon data refresh completion in Power BI / MS Fabric.
    In production: calls Microsoft Graph API to send SharePoint report links.
    """
    logger.info(f"Distributing report: {report_name}")
    result = {
        "report": report_name,
        "trigger": trigger_event,
        "recipients": recipients,
        "status": "DISPATCHED",
        "dispatched_at": datetime.utcnow().isoformat(),
        "delivery_method": "Microsoft_Graph_Email + SharePoint_Link"
    }
    logger.info(f"  → Report dispatched to {len(recipients)} recipients.")
    return result


# ═══════════════════════════════════════════════════════════════════════════
# DEMO RUNNER
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Aware CBW — GPT AI Agent Demo")
    print("="*60)

    # Document routing demo
    sample_doc = """
    Subject: Q3 Procurement Request — Aware EarDefender (Camouflage) x 500 units
    From: Contracting Officer, U.S. Army Garrison Fort Liberty
    This letter constitutes a formal request for proposal under FAR Part 12
    for custom hearing protection devices for deployment-ready personnel.
    Delivery required at Fort Liberty, NC within 90 days of contract award.
    """
    classification = classify_document(sample_doc)
    print("\n[1] Document Routing Result:")
    print(json.dumps(classification, indent=2))

    # Anomaly detection demo
    pipeline_data = [
        {"deal_id": "DEAL-001", "segment": "Defense", "deal_value": 45000, "days_since_activity": 21, "stage": "Proposal"},
        {"deal_id": "DEAL-002", "segment": "Industrial", "deal_value": 12000, "days_since_activity": 3, "stage": "Negotiation"},
        {"deal_id": "DEAL-003", "segment": "Healthcare", "deal_value": 8500, "days_since_activity": 18, "stage": "Discovery"},
    ]
    anomalies = analyze_pipeline(pipeline_data)
    print("\n[2] Pipeline Anomaly Analysis:")
    print(json.dumps(anomalies, indent=2))

    # Report distribution demo
    report_result = distribute_report(
        report_name="Weekly_KPI_Dashboard_PowerBI",
        recipients=["cfo@awarecbw.com", "coo@awarecbw.com", "vp_sales@awarecbw.com"],
        trigger_event="PowerBI_DataRefresh_Completed"
    )
    print("\n[3] Report Distribution:")
    print(json.dumps(report_result, indent=2))
    print("\n✅ Demo complete.")
