#!/bin/bash
echo "🚀 Starting CRM..."
echo ""
source ~/.nvm/nvm.sh
nvm use 24
cd /workspace/frappe-bench
echo ""
echo "✅ Node.js 24 activated"
echo "✅ Starting Frappe Bench..."
echo ""
bench start
