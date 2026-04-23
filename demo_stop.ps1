$ErrorActionPreference = 'SilentlyContinue'

function Stop-PortProcess {
	param([int]$Port)
	$conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
	if (-not $conns) { return }
	$ids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
	foreach ($id in $ids) {
		if ($id -and $id -ne 0) {
			Stop-Process -Id $id -Force -ErrorAction SilentlyContinue
		}
	}
}

Stop-PortProcess -Port 8001
Stop-PortProcess -Port 5173
Write-Host 'Stopped anything on ports 8001 and 5173.'
