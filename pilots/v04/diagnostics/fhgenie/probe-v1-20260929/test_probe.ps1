[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'probe.ps1')
$script:Calls = 0; $script:SecretReads = 0; $script:Cases = 0
$script:DummyKey = 'TEST_DUMMY_SECRET_CANARY_91'
$script:TestRoot = Join-Path ([IO.Path]::GetTempPath()) ('fhgenie-offline-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($script:TestRoot) | Out-Null

function Assert($Condition, [string]$Label) { if (-not $Condition) { throw "Offline assertion failed: $Label" } }
function Get-ProbeSecret {
    $script:SecretReads++
    ConvertTo-SecureString -String $script:DummyKey -AsPlainText -Force
}
function Invoke-WebRequest {
    param($Uri,$Method,$Headers,$ContentType,$Body,$MaximumRedirection,$MaximumRetryCount,$TimeoutSec,[switch]$UseBasicParsing,$ErrorAction)
    $script:Calls++
    Assert ($Uri -ceq '<FHGENIE_ENDPOINT>' -and $Method -ceq 'Post') 'fixed single POST'
    Assert ($Headers.Authorization -ceq ('Bearer ' + $script:DummyKey)) 'dummy Bearer key'
    Assert ($MaximumRedirection -eq 0 -and $MaximumRetryCount -eq 0 -and $TimeoutSec -eq 90) 'no redirects, no retries, bounded timeout'
    Assert ($UseBasicParsing -and $ContentType -ceq 'application/json; charset=utf-8') 'explicit transport settings'
    Assert (([Text.Encoding]::UTF8.GetString($Body) | ConvertFrom-Json).model -ceq 'deepseek-ai/DeepSeek-V4-Flash-0731') 'approved request body'
    if ($script:MockMode -eq 'http_error') {
        $exception = [Exception]::new('UNSAFE_ERROR_CANARY ' + $script:DummyKey)
        $exception | Add-Member -NotePropertyName Response -NotePropertyValue ([pscustomobject]@{StatusCode=400})
        $record = [Management.Automation.ErrorRecord]::new($exception,'MockFailure',[Management.Automation.ErrorCategory]::InvalidOperation,$null)
        $record.ErrorDetails = [Management.Automation.ErrorDetails]::new('{"error":{"message":"UNSAFE_BODY_CANARY","type":"invalid_request_error","code":"unsupported_parameter","param":"reasoning_effort"}}')
        throw $record
    }
    [pscustomobject]@{StatusCode=200;Content=$script:ResponseText}
}
function New-Case {
    $script:Calls = 0; $script:SecretReads = 0; $script:Cases++; $script:MockMode = 'success'
    $folder = Join-Path $script:TestRoot ([string]$script:Cases)
    [IO.Directory]::CreateDirectory($folder) | Out-Null
    foreach ($name in @('probe.ps1','test_probe.ps1')) { Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $folder $name) }
    $request = @{
        model='deepseek-ai/DeepSeek-V4-Flash-0731';messages=@(@{role='user';content='Return exactly this JSON object and nothing else: {"status":"ok"}. Do not use tools.'})
        stream=$false;max_tokens=2048;reasoning_effort='low';temperature=1;top_p=1
        response_format=@{type='json_schema';json_schema=@{name='connection_test';strict=$true;schema=@{type='object';properties=@{status=@{type='string';enum=@('ok')}};required=@('status');additionalProperties=$false}}}
    }
    $request | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $folder 'request.json')
    $plan = @{request_sha256=(Get-ProbeHash (Join-Path $folder 'request.json'));probe_sha256=(Get-ProbeHash (Join-Path $folder 'probe.ps1'));tests_sha256=(Get-ProbeHash (Join-Path $folder 'test_probe.ps1'));endpoint=$script:ProbeEndpoint;timeout_seconds=90}
    $plan | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $folder 'plan.json')
    @{approved=$true;reviewer='Milad Morad';response='Offline dummy approval only';date='2026-09-29';plan_sha256=(Get-ProbeHash (Join-Path $folder 'plan.json'));request_sha256=$plan.request_sha256} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $folder 'approval.json')
    $script:ResponseData = @{model='deepseek-ai/DeepSeek-V4-Flash-0731';system_fingerprint='fp_mock';usage=@{prompt_tokens=28;completion_tokens=5};choices=@(@{finish_reason='stop';message=@{role='assistant';content='{"status":"ok"}'}})}
    $script:ResponseText = $script:ResponseData | ConvertTo-Json -Depth 10
    return $folder
}
function Run-ResponseCase([string]$Expected) {
    $script:ResponseText = $script:ResponseData | ConvertTo-Json -Depth 10
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq $Expected) ("expected $Expected; got " + $result.status)
    Assert ($script:Calls -eq 1 -and $script:SecretReads -eq 1) 'exactly one mocked call and dummy key read'
    Assert (Test-Path -LiteralPath (Join-Path $script:CaseDirectory 'attempt.json')) 'persistent reservation'
    Assert (-not (($result | ConvertTo-Json).Contains($script:DummyKey))) 'no credential output'
    return $result
}

try {
    $script:CaseDirectory = New-Case
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory
    Assert ($result.status -ceq 'check_only' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'default mode has no HTTP or secret read'
    Assert ($result.plan_hashes_valid -and $result.request_valid) 'default mode validates plan and request'
    Remove-Item -LiteralPath (Join-Path $script:CaseDirectory 'approval.json')
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory
    Assert ($result.status -ceq 'check_only' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'check-only needs no approval'
    Add-Content -LiteralPath (Join-Path $script:CaseDirectory 'probe.ps1') -Value '# changed'
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory
    Assert ($result.status -ceq 'approval_hash_mismatch' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'check-only detects changed code'
    $script:CaseDirectory = New-Case
    Remove-Item -LiteralPath (Join-Path $script:CaseDirectory 'approval.json')
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'approval_missing' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'missing approval fails closed'
    $script:CaseDirectory = New-Case
    $approvalPath = Join-Path $script:CaseDirectory 'approval.json'
    $approval = Get-Content -LiteralPath $approvalPath -Raw | ConvertFrom-Json
    $approval.approved = $false
    $approval | ConvertTo-Json | Set-Content -LiteralPath $approvalPath
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'approval_invalid' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'unapproved fails closed'
    $script:CaseDirectory = New-Case
    Add-Content -LiteralPath (Join-Path $script:CaseDirectory 'request.json') -Value ' '
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'approval_hash_mismatch' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'changed request fails closed'
    $script:CaseDirectory = New-Case
    Add-Content -LiteralPath (Join-Path $script:CaseDirectory 'test_probe.ps1') -Value '# changed'
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'approval_hash_mismatch' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'changed test code fails closed'
    $script:CaseDirectory = New-Case
    $result = Run-ResponseCase 'success'
    Assert ($result.prompt_tokens -eq 28 -and $result.completion_tokens -eq 5) 'observed usage'
    $script:Calls = 0; $script:SecretReads = 0
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'attempt_already_reserved' -and $script:Calls -eq 0 -and $script:SecretReads -eq 0) 'second attempt blocked before secret read'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].finish_reason = 'length'
    $null = Run-ResponseCase 'response_finish_invalid'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.refusal = 'Mock refusal'
    $null = Run-ResponseCase 'response_refusal'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.tool_calls = @(@{id='mock'})
    $null = Run-ResponseCase 'response_tool_call'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.function_call = @{name='mock'}
    $null = Run-ResponseCase 'response_tool_call'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.tool_calls = @()
    $null = Run-ResponseCase 'success'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.content = '{invalid'
    $null = Run-ResponseCase 'response_content_invalid'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.content = '{"status":"ok","extra":true}'
    $null = Run-ResponseCase 'response_content_invalid'
    $script:CaseDirectory = New-Case
    $script:ResponseData.Remove('usage')
    $result = Run-ResponseCase 'response_usage_unknown'
    Assert ($null -eq $result.prompt_tokens -and $null -eq $result.completion_tokens) 'unknown usage remains null'
    $script:CaseDirectory = New-Case
    $script:ResponseData.usage.completion_tokens = -1
    $null = Run-ResponseCase 'response_usage_unknown'
    $script:CaseDirectory = New-Case
    $script:ResponseData.usage.completion_tokens = '5'
    $null = Run-ResponseCase 'response_usage_unknown'
    $script:CaseDirectory = New-Case
    $script:ResponseData.choices[0].message.reasoning_content = 'UNSAFE_REASONING_CANARY'
    $result = Run-ResponseCase 'success'
    Assert ($result.reasoning_content_present -and -not (($result | ConvertTo-Json).Contains('UNSAFE_REASONING_CANARY'))) 'reasoning content is not printed'
    $script:CaseDirectory = New-Case
    $script:ResponseText = '{invalid'
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    Assert ($result.status -ceq 'response_invalid_json' -and $script:Calls -eq 1) 'invalid response JSON'
    $script:CaseDirectory = New-Case
    $script:MockMode = 'http_error'
    $result = Invoke-FhgenieProbe -Directory $script:CaseDirectory -ExecuteOnce
    $serialized = $result | ConvertTo-Json
    Assert ($result.status -ceq 'http_error' -and $result.http_status -eq 400 -and $script:Calls -eq 1) 'HTTP error without retry'
    Assert ($result.provider_error_type -ceq 'invalid_request_error' -and $result.provider_error_code -ceq 'unsupported_parameter' -and $result.provider_error_param -ceq 'reasoning_effort') 'constrained provider identifiers'
    Assert (-not ($serialized.Contains('UNSAFE_ERROR_CANARY') -or $serialized.Contains('UNSAFE_BODY_CANARY') -or $serialized.Contains($script:DummyKey))) 'exception and response body redacted'
    $persisted = Get-Content -LiteralPath (Join-Path $script:CaseDirectory 'result.json') -Raw
    Assert (-not ($persisted.Contains('UNSAFE_') -or $persisted.Contains($script:DummyKey))) 'persisted result redacted'
    [pscustomobject]@{status='passed';offline_cases=$script:Cases;real_network_requests=0;real_credential_reads=0} | ConvertTo-Json
} finally {
    # Only our GUID-named test directory, resolved beneath the system temp directory.
    $resolved = [IO.Path]::GetFullPath($script:TestRoot)
    $tempRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if ($resolved.StartsWith($tempRoot, [StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetFileName($resolved) -match '^fhgenie-offline-[a-f0-9]{32}$') { Remove-Item -LiteralPath $resolved -Recurse -Force }
}
