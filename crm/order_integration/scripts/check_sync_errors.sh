#!/bin/bash
echo "=== Recent Order Sync errors ==="
mysql -u _dad6286a58a0d31d -pF8hxztqKMzAtXSKA _dad6286a58a0d31d -e "
SELECT method, SUBSTRING(error,1,800) as err, creation 
FROM \`tabError Log\` 
WHERE method LIKE '%Order Sync%' OR method LIKE '%order_sync%' OR error LIKE '%order_sync%'
ORDER BY creation DESC 
LIMIT 10;" 2>&1

echo ""
echo "=== Recent leads ==="
mysql -u _dad6286a58a0d31d -pF8hxztqKMzAtXSKA _dad6286a58a0d31d -e "
SELECT name, lead_name, email, mobile_no, order_source, creation 
FROM \`tabCRM Lead\` 
ORDER BY creation DESC 
LIMIT 5;" 2>&1

echo ""
echo "=== Worker log tail ==="
tail -20 /mnt/d/frappe/ipshopy-bench/logs/worker.log 2>/dev/null
echo ""
echo "=== Worker error log tail ==="
tail -20 /mnt/d/frappe/ipshopy-bench/logs/worker.error.log 2>/dev/null
