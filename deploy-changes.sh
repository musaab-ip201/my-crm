#!/bin/bash

echo "🔄 Syncing CRM changes from git repo to Frappe app..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Sync the entire crm module
echo -e "${YELLOW}Copying crm module...${NC}"
cp -r /workspace/crm /workspace/frappe-bench/apps/crm

# Run migration to apply any database changes
echo -e "${YELLOW}Running database migration...${NC}"
cd /workspace/frappe-bench
bench --site dev.localhost migrate

# Clear cache
echo -e "${YELLOW}Clearing cache...${NC}"
bench --site dev.localhost clear-cache

# Restart bench
echo -e "${YELLOW}Restarting Frappe...${NC}"
bench restart

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Changes deployed:"
echo "  - Updated hooks.py"
echo "  - Synced lead_routing module"
echo "  - Synced order_integration module"
echo "  - Applied database migrations"
echo "  - Cleared cache"
echo ""
echo "Your CRM is now updated with the latest changes."
