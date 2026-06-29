# Update module references in DocType JSON files
$doctypes = @(
    "department_pipeline_stage",
    "department_team_member",
    "department_shift",
    "department_transition_rule",
    "lead_department_log",
    "order_sync_source",
    "api_schema_storage"
)

foreach ($doctype in $doctypes) {
    $jsonPath = "fcrm\doctype\$doctype\$doctype.json"

    if (Test-Path $jsonPath) {
        Write-Host "Updating $doctype..."
        $content = Get-Content $jsonPath -Raw

        # Replace "Lead Routing" or "Order Integration" with "FCRM"
        $content = $content -replace '"module": "Lead Routing"', '"module": "FCRM"'
        $content = $content -replace '"module": "Order Integration"', '"module": "FCRM"'

        Set-Content $jsonPath $content -NoNewline
        Write-Host "Updated $doctype" -ForegroundColor Green
    } else {
        Write-Host "File not found: $jsonPath" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "All modules updated to FCRM!" -ForegroundColor Green
