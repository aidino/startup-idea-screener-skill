#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python3 "$ScriptDir/scripts/run_pipeline.py" @args
exit $LASTEXITCODE
