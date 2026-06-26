# CRM Setup - GitHub Codespaces

## Quick Start

```bash
/workspace/start-crm.sh
Then access at port 8000 → /app

Login:

Username: Administrator
Password: admin
What's Installed
Frappe Framework: v15 (stable)
Node.js: v18
CRM App: Backend only (frontend build disabled due to memory constraints)
Database: MariaDB (via Docker)
Cache: Redis (via Docker)
Accessing CRM
Use the Frappe Desk to access CRM DocTypes:

Press Ctrl+K to open search
Type: CRM Lead, CRM Deal, CRM Organization, etc.
Create and manage records through standard Frappe forms
Codespace Management
Stop to save free hours:

Go to: https://github.com/codespaces
Click "..." → "Stop codespace"
Restart:

Click codespace → "Open in browser"
Run: /workspace/start-crm.sh
Modifications
Telemetry fix: crm/api/__init__.py (Frappe v17 compatibility)
Startup script: /workspace/start-crm.sh
Notes
Frontend build requires 4-core Codespace (8GB RAM)
Current setup uses 2-core (4GB RAM) - backend only
All CRM features work through Frappe Desk UI
Free tier: 60 hours/month on 2-core machine