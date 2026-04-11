# validate-submission.ps1 — SentinelCore Submission Validator (Windows Native)
#
# Usage: ./validate-submission.ps1 https://your-space.hf.space
#

param (
    [Parameter(Mandatory=$true)]
    [string]$PingUrl
)

$ErrorActionPreference = "Continue"

function Write-Log([string]$msg) {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $msg"
}

function Write-Pass([string]$msg) {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] PASSED -- $msg" -ForegroundColor Green
}

function Write-Fail([string]$msg) {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] FAILED -- $msg" -ForegroundColor Red
}

Write-Host "==========================================" -ForegroundColor Cyan -FontWeight Bold
Write-Host "  SentinelCore: Submission Validator (PS)" -ForegroundColor Cyan -FontWeight Bold
Write-Host "==========================================" -ForegroundColor Cyan -FontWeight Bold
Write-Log "Ping URL: $PingUrl"
Write-Host ""

# ── STEP 1: Ping ─────────────────────────────────────────────────────────────
Write-Log "Step 1/4: Pinging HF Space ($PingUrl/reset) ..."
try {
    $Response = Invoke-WebRequest -Uri "$($PingUrl.TrimEnd('/'))/reset" -Method Post -ContentType "application/json" -Body '{}' -TimeoutSec 30 -ErrorAction Stop
    if ($Response.StatusCode -eq 200) {
        Write-Pass "HF Space is live and responds to /reset"
    } else {
        Write-Fail "HF Space /reset returned $($Response.StatusCode)"
        exit 1
    }
} catch {
    Write-Fail "HF Space not reachable: $($_.Exception.Message)"
    Write-Host "  Hint: Check your network and ensure the Space is in 'Running' state." -ForegroundColor Yellow
    exit 1
}

# ── STEP 2: Docker Build ──────────────────────────────────────────────────────
Write-Log "Step 2/4: Running docker build ..."
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Fail "docker command not found"
    exit 1
}

try {
    $BuildResult = docker build . 2>&1
    Write-Pass "Docker build succeeded"
} catch {
    Write-Fail "Docker build failed"
    Write-Host $BuildResult -ForegroundColor Red
    exit 1
}

# ── STEP 3: OpenEnv Validate ──────────────────────────────────────────────────
Write-Log "Step 3/4: Running openenv validate ..."
if (-not (Get-Command openenv -ErrorAction SilentlyContinue)) {
    Write-Fail "openenv command not found (pip install openenv-core)"
    exit 1
}

$ValidateResult = openenv validate
if ($LASTEXITCODE -eq 0) {
    Write-Pass "openenv validate passed"
} else {
    Write-Fail "openenv validate failed"
    Write-Host $ValidateResult -ForegroundColor Red
    exit 1
}

# ── STEP 4: Baseline Reproduction ───────────────────────────────────────────
Write-Log "Step 4/4: Running inference script baseline ..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Fail "python command not found"
    exit 1
}

$env:HF_TOKEN = if ($env:HF_TOKEN) { $env:HF_TOKEN } else { "dummy_verification_key" }
$env:OPENENV_TASK_ID = "task1_devops"

$InferenceOutput = python inference.py 2>&1
if ($InferenceOutput -like "*[START]*" -and $InferenceOutput -like "*[END]*") {
    Write-Pass "Baseline reproduction successful (Found tags)"
} else {
    Write-Fail "Inference script baseline failed"
    Write-Host $InferenceOutput -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  All 4/4 checks passed! READY TO SUBMIT." -ForegroundColor Green -FontWeight Bold
Write-Host "==========================================" -ForegroundColor Cyan
