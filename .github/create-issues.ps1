# Create GitHub Issues for v4.0 Development
# Reads issue-templates.json and creates all issues with proper labels

$ErrorActionPreference = "Stop"

Write-Host "Creating GitHub Issues for Modern Data Platform v4.0..." -ForegroundColor Cyan

# Read the issue templates
$templates = Get-Content ".github/issue-templates.json" | ConvertFrom-Json

$issueNumbers = @{}
$totalIssues = 0

foreach ($phaseKey in $templates.phases.PSObject.Properties.Name) {
    $phase = $templates.phases.$phaseKey
    $phaseName = $phase.name
    $priority = $phase.priority
    
    Write-Host "`n📋 Phase $phaseKey - $phaseName" -ForegroundColor Yellow
    
    foreach ($task in $phase.tasks) {
        $totalIssues++
        $title = $task.title
        $body = $task.body
        $estimate = $task.estimate
        
        # Build labels
        $labels = @("phase-$phaseKey")
        
        # Add category label based on phase
        switch ($phaseKey) {
            "4.1" { $labels += "testing" }
            "4.2" { $labels += "security" }
            "4.3" { $labels += "scripts" }
            "4.4" { $labels += "documentation" }
            "4.5" { $labels += "quality" }
            "4.6" { $labels += "dashboard" }
        }
        
        # Add priority label
        switch ($priority) {
            "critical" { $labels += "critical" }
            "high" { $labels += "high-priority" }
            "medium" { $labels += "medium-priority" }
        }
        
        # Add estimate to body
        $fullBody = "**Estimated Time:** $estimate`n**Phase:** $phaseKey - $phaseName`n**Priority:** $priority`n`n$body"
        
        # Create issue
        Write-Host "  Creating: $title" -ForegroundColor Gray
        
        $labelString = $labels -join ","
        $result = gh issue create --title $title --body $fullBody --label $labelString 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            # Extract issue number from result
            if ($result -match '#(\d+)') {
                $issueNumber = $matches[1]
                $issueNumbers[$title] = $issueNumber
                Write-Host "    ✓ Created issue #$issueNumber" -ForegroundColor Green
            }
        } else {
            Write-Host "    ✗ Failed: $result" -ForegroundColor Red
        }
        
        Start-Sleep -Milliseconds 500  # Rate limiting
    }
}

Write-Host "`n✅ Created $totalIssues issues for v4.0 development" -ForegroundColor Green
Write-Host "`nView all issues: https://github.com/DeanLuus22021994/docker_dotfiles/issues" -ForegroundColor Cyan
