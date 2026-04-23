$ErrorActionPreference = 'Stop'

function Stop-PortProcess {
	param([int]$Port)
	try {
		$conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
		if (-not $conns) { return }
		$ids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
		foreach ($id in $ids) {
			if ($id -and $id -ne 0) {
				Stop-Process -Id $id -Force -ErrorAction SilentlyContinue
			}
		}
	} catch {
		# best-effort
	}
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root 'backend'
$frontendDir = Join-Path $root 'frontend'
$backendPy = Join-Path $backendDir 'venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $backendPy)) {
	Write-Host "Missing backend venv at: $backendPy" -ForegroundColor Red
	Write-Host "Create it once: cd backend; python -m venv venv; .\\venv\\Scripts\\python.exe -m pip install -r requirements.txt" -ForegroundColor Yellow
	exit 1
}

Write-Host 'Stopping anything on ports 8001 and 5173...' -ForegroundColor Cyan
Stop-PortProcess -Port 8001
Stop-PortProcess -Port 5173

Write-Host 'Starting backend (FastAPI) on http://127.0.0.1:8001 ...' -ForegroundColor Cyan
Start-Process -FilePath 'powershell.exe' -WorkingDirectory $backendDir -ArgumentList @(
	'-NoProfile',
	'-NoExit',
	'-Command',
	"& '$backendPy' -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"
) | Out-Null

Write-Host 'Starting frontend (Vite) on http://localhost:5173 ...' -ForegroundColor Cyan
Start-Process -FilePath 'cmd.exe' -WorkingDirectory $frontendDir -ArgumentList @(
	'/k',
	'npm run dev -- --host 127.0.0.1 --port 5173 --strictPort'
) | Out-Null

Write-Host 'Waiting for services to respond...' -ForegroundColor Cyan

$backendOk = $false
$frontendOk = $false

for ($i = 0; $i -lt 25; $i++) {
	if (-not $backendOk) {
		try {
			$health = Invoke-RestMethod -Uri 'http://127.0.0.1:8001/health' -TimeoutSec 5
			Write-Host ("Backend OK: " + ($health | ConvertTo-Json -Compress)) -ForegroundColor Green
			$backendOk = $true
		} catch {
			# ignore and retry
		}
	}

	if (-not $frontendOk) {
		try {
			$resp = Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:5173/' -TimeoutSec 5
			Write-Host ("Frontend OK: STATUS=" + $resp.StatusCode + " CT=" + $resp.Headers['Content-Type']) -ForegroundColor Green
			$frontendOk = $true
		} catch {
			# ignore and retry
		}
	}

	if ($backendOk -and $frontendOk) { break }
	Start-Sleep -Seconds 1
}

if (-not $backendOk) {
	Write-Host 'Backend still not responding yet — check the backend console for errors.' -ForegroundColor Yellow
}
if (-not $frontendOk) {
	Write-Host 'Frontend still not responding yet — check the frontend console for errors.' -ForegroundColor Yellow
}

Write-Host ''
Write-Host 'Open these in your browser:' -ForegroundColor Cyan
Write-Host '  App:      http://localhost:5173' -ForegroundColor White
Write-Host '  API Docs: http://127.0.0.1:8001/docs' -ForegroundColor White
