$conn = Get-NetTCPConnection 
$results = @{}
foreach($c in $conn) { 
    if (($c.state).tostring() -like "*Established*") {
        $p = (Get-Process -id $c.OwningProcess)
        $results[$p.ProcessName] = $p.Id
        $p
    }
}
While (!($input -eq 'q')) { 
    Write-Host "If you don't recognize a process and want to kill it, enter it's name. Enter 'q' to exit. " -ForegroundColor yellow -NoNewline
    $input = Read-Host
    if ($input -eq 'q') { 
        $done = $true 
    } else {
        if ($results.$input) {
            Write-Host "killing $input..."
            taskkill /PID $results.$input /F
            Write-Host "Done."
        }
    }
}
