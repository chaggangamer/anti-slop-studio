<#
.SYNOPSIS
  Install the anti-slop-studio skill into an agent's skills folder (Windows PowerShell 5.1+ or PowerShell 7).
.EXAMPLE
  .\install.ps1                          # shared folder, user scope (%USERPROFILE%\.agents\skills)
  .\install.ps1 -Agent claude            # Claude Code (%USERPROFILE%\.claude\skills)
  .\install.ps1 -Agent all -Scope project
  .\install.ps1 -Dest D:\my\skills       # any folder you choose
  .\install.ps1 -DryRun
.NOTES
  Agents: shared (default), claude, copilot, opencode, codex, cursor, gemini, all.
  codex, cursor and gemini use the shared folder; check your agent's docs if it scans elsewhere.
#>
param(
  [ValidateSet('shared','claude','copilot','opencode','codex','cursor','gemini','all')][string]$Agent = 'shared',
  [ValidateSet('user','project')][string]$Scope = 'user',
  [string]$Dest = '',
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'skills\anti-slop-studio'
if (-not (Test-Path (Join-Path $src 'SKILL.md'))) { Write-Error "cannot find $src\SKILL.md" }

function Get-SkillDir([string]$a) {
  $home_ = $env:USERPROFILE
  if ($Scope -eq 'user') {
    switch ($a) {
      { $_ -in 'shared','codex','cursor','gemini' } { return Join-Path $home_ '.agents\skills' }
      'claude'   { return Join-Path $home_ '.claude\skills' }
      'copilot'  { return Join-Path $home_ '.copilot\skills' }
      'opencode' { $cfg = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { Join-Path $home_ '.config' }; return Join-Path $cfg 'opencode\skills' }
    }
  } else {
    switch ($a) {
      { $_ -in 'shared','codex','cursor','gemini' } { return '.agents\skills' }
      'claude'   { return '.claude\skills' }
      'copilot'  { return '.github\skills' }
      'opencode' { return '.opencode\skills' }
    }
  }
}

if ($Dest) { $targets = @($Dest) }
elseif ($Agent -eq 'all') { $targets = @('shared','claude','copilot','opencode' | ForEach-Object { Get-SkillDir $_ } | Select-Object -Unique) }
else { $targets = @(Get-SkillDir $Agent) }

foreach ($base in $targets) {
  $target = Join-Path $base 'anti-slop-studio'
  if ($DryRun) { Write-Host "would copy $src -> $target"; continue }
  New-Item -ItemType Directory -Force -Path $base | Out-Null
  if (Test-Path $target) { Remove-Item -Recurse -Force $target }
  Copy-Item -Recurse -Path $src -Destination $target
  Write-Host "installed: $target"
}
Write-Host 'Done. Restart or reload your agent so it rescans its skills.'
