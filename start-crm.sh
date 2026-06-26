#!/bin/bash
echo "🚀 Starting CRM (Frappe v15 - Backend Only)..."
echo ""
source ~/.nvm/nvm.sh
nvm use 18
cd /workspace/frappe-bench
echo ""
echo "✅ Node.js 18 activated"
echo "✅ Starting Frappe Bench..."
echo "📌 CRM Access: Port 8000 → /app (Frappe Desk)"
echo "📋 Backend-only mode: Use DocTypes for CRM operations"
echo ""
bench start
