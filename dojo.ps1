if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host '缺少 uv。请运行 winget install astral-sh.uv，然后重新打开终端。'
    exit 1
}
& uv run --no-project --python '>=3.12' (Join-Path $PSScriptRoot 'dojo.py') @args
exit $LASTEXITCODE
