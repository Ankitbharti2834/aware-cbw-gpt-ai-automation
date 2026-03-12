# Project 3 — GPT-Powered Automation & AI Agent Workflow Development

**Organization:** Aware Custom Biometric Wearables  
**Domain:** AI/ML | Process Automation | Workflow Orchestration  
**Reported To:** CFO, COO, VPs, Directors  
**Confidentiality:** 🔒 Enterprise Internal Project — Defense-Adjacent Organization  
> *Production workflows, OAuth credentials, Logic App configurations, and CRM integration endpoints are confidential. This repository reproduces the AI agent architecture and automation logic using mock data and environment-variable placeholders.*

---

## Business Problem

Aware CBW's cross-functional teams spent significant time on manual, repetitive tasks: routing inbound procurement documents (including DoD contracts), manually updating Dynamics 365 CRM sales records, and distributing Power BI reports via email. These tasks were error-prone, delayed, and not scalable as the business grew across Defense, Industrial, and Healthcare segments.

## Solution

Designed and deployed a suite of GPT-powered AI agent pipelines using Power Automate and Azure Logic Apps. The system automated three major workflows: intelligent document routing (classifying inbound DoD, industrial, and healthcare documents using GPT-4o), real-time CRM anomaly flagging triggered by Dynamics 365 events, and automated BI report distribution via Microsoft Graph API. Copilot was embedded in MS Fabric to enable natural-language querying of operational datasets for non-technical stakeholders.

## Technical Architecture

```
Email Inbox / SharePoint Trigger
        │
        ▼
Power Automate Flow ──► Azure Logic App ──► GPT-4o API
        │                                       │
        ├── Document Classification ────────────┤
        ├── CRM Anomaly Detection  ─────────────┤
        └── Report Distribution   ─────────────┘
                │
                ▼
        Dynamics 365 CRM Update + Microsoft Graph Email
```

## Key Deliverables

- GPT-4o document intake router classifying Defense, Industrial, Healthcare, Finance, and Compliance documents  
- Real-time pipeline anomaly detection against Dynamics 365 CRM deal records  
- Automated report distribution using Microsoft Graph API  
- OAuth and Google API integrations for external partner data exchange  
- Power Automate flow design training materials for junior analysts  

## Impact

| Metric | Result |
|---|---|
| Manual processing time | **45% reduction** |
| Cross-functional workflows automated | **10+** |
| Report distribution lag eliminated | ✅ |

## Repository Contents

```
Project_03_GPT_AI_Automation/
├── src/
│   └── gpt_agent_pipeline.py   # Document router, anomaly detector, report distributor
└── README.md
```

## Running the Demo

```bash
pip install openai
# Set your key (optional — falls back to mock mode):
export OPENAI_API_KEY=your-key-here
python src/gpt_agent_pipeline.py
```

## Tools & Technologies

Power Automate · Azure Logic Apps · GPT API (OpenAI) · MS Fabric · Microsoft Copilot · OAuth 2.0 · Google API · Dynamics 365 CRM · Microsoft Graph API

---
*For technical discussion, connect via [LinkedIn](https://linkedin.com/in/ankitbharti2834).*
