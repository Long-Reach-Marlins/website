<#
start-server.ps1

Simple helper to run a Python HTTP server that serves the ./src folder.

Usage examples:
# Start in foreground on port 8000 (press Ctrl+C to stop) — this will open your browser by default
PS> .\start-server.ps1

# Start in background and save PID to .server.pid (opens browser by default)
PS> .\start-server.ps1 -Background

# Start on a different port (browser opens by default). Use -NoOpen to prevent opening.
PS> .\start-server.ps1 -Port 8080

Notes:
- This script prefers the `py` launcher, then `python` from PATH.
- If running background, the PID is written to .server.pid in the repo root.
- To stop a background server started by this script:
    Get-Content .server.pid | ForEach-Object { Stop-Process -Id $_ -ErrorAction SilentlyContinue }
    Remove-Item .server.pid -ErrorAction SilentlyContinue
#>

param(
    [int]
    $Port = 8000,

    [switch]
    $Background,

    # Provided for backwards compatibility; not required since opening is the default
    [switch]
    $Open,

    # Use this switch to prevent the browser from opening (opening is the default behavior)
    [switch]
    $NoOpen
)

function Get-PythonCmd {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return $py.Source }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) { return $python.Source }

    throw "Python not found. Install Python 3 or ensure 'py' or 'python' is on PATH."
}

try {
    $pythonCmd = Get-PythonCmd
} catch {
    Write-Error $_.Exception.Message
    exit 1
}

$argList = @('-3', '-m', 'http.server', $Port.ToString(), '--directory', 'src')

# Determine effective open behavior: -NoOpen wins, then explicit -Open, otherwise default = open
$shouldOpen = if ($PSBoundParameters.ContainsKey('NoOpen')) { $false } elseif ($PSBoundParameters.ContainsKey('Open')) { $true } else { $true }

if ($Background) {
    Write-Output "Starting background server on port $Port..."
    $proc = Start-Process -FilePath $pythonCmd -ArgumentList $argList -PassThru -WindowStyle Hidden
    if ($proc -and $proc.Id) {
        $proc.Id | Out-File -FilePath .server.pid -Encoding ascii
        Write-Output "Server started (PID $($proc.Id)). Visit http://localhost:$Port"
    } else {
        Write-Error "Failed to start background server."
        exit 2
    }

    if ($shouldOpen) { Start-Process "http://localhost:$Port" }

    exit 0
} else {
    Write-Output "Starting foreground server on port $Port. Press Ctrl+C to stop."
    if ($shouldOpen) { Start-Process "http://localhost:$Port" }
    & $pythonCmd @argList
}
