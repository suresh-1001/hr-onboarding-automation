# Automated Onboarding & Offboarding Workflow

> HR-triggered provisioning for Google Workspace / Microsoft 365 (Entra + Intune), Slack, and Jira — with full audit trails for PCI DSS & SOC 2.

## 🎯 Goal
Turn HR personnel data into **consistent account provisioning**, **role‑based access**, and **compliance-grade logging** — with deprovisioning that actually closes the loop.

## 🧩 Workflow
1. **HR System** (BambooHR/Paylocity/HiBob) change → webhook or scheduled pull
2. **Python Orchestrator** reads HR profile → determines role template → emits tasks
3. **Provisioning Adapters** (PowerShell/Python) create/update accounts in:
   - Google Workspace or Entra ID / Intune
   - Slack (role-based channels, SCIM or Invite API)
   - Jira/Confluence (groups, project roles)
4. **Post-Provisioning**: welcome emails, Slack DMs, Jira onboarding ticket
5. **Offboarding**: disable → transfer ownership → archive → revoke tokens → ticket closure

## ⚙️ Features
- Role templates in YAML (least privilege by default)
- Device enrollment with Intune (Windows/macOS) or MDM alternatives
- Audit logs (JSON) + signed daily digest
- Documentation generated via ChatGPT (runbook summary + changelog)

## 🏗️ Structure
```
/scripts/
  orchestrator.py          # main HR → adapters pipeline
  adapters/
    google_workspace.py
    entra_intune.ps1
    slack_scim.py
    jira_api.py
/config/
  roles/*.yaml             # per‑role app & group mappings
/docs/                     # architecture, SOPs, redacted screenshots
/examples/                 # sample HR records & outputs
```

## 🚀 Quick Start
```bash
python ./scripts/orchestrator.py   --source bamboohr   --email jane.doe@company.com   --role "Finance Analyst"   --dry-run
```

## 🔐 Compliance
- Every create/update/delete is logged with request/response, actor, and timestamp
- Hash manifest for daily logs; optional S3/Blob immutability (WORM)
- Offboarding checklist ensures access revocation and data retention alignment

## 📈 Impact (benchmarks)
- ~60% faster time-to-ready on Day 1
- Fewer provisioning mistakes, consistent app access
- Clear evidence for PCI DSS 7.x & 8.x, SOC 2 CC6.x

## 🛣️ Roadmap
- [ ] Okta/JumpCloud adapters
- [ ] Hardware asset handoff + label printing
- [ ] Badge/door access system adapter

## 🧠 Skills & Tools
`Python` `PowerShell` `Google Workspace Admin` `Entra ID / Intune` `Slack API` `Jira` `SOC 2` `PCI DSS`

## 📝 License
MIT — see `LICENSE`.

---

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Last commit](https://img.shields.io/github/last-commit/suresh-1001/hr-onboarding-automation)
