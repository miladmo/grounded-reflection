#Requires -Version 7.0
[CmdletBinding()]
param([switch]$ExecuteOnce)

$ErrorActionPreference = 'Stop'
$script:ProbeEndpoint = '<FHGENIE_ENDPOINT>'
$script:ProbeKeyPath = Join-Path $env:LOCALAPPDATA 'reflectAI/fhgenie-api-key.dpapi'

function Get-ProbeHash([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-ProbeSecret {
    # Windows user DPAPI; never called by check-only mode.
    ConvertTo-SecureString -String ([IO.File]::ReadAllText($script:ProbeKeyPath))
}

function Test-ProbeCount($Value) {
    ($Value -is [int] -or $Value -is [long] -or $Value -is [System.Numerics.BigInteger]) -and $Value -ge 0 -and $Value -le [long]::MaxValue
}

function Get-FinalJsonStatus($Content) {
    if ($Content -isnot [string]) { return 'not_string' }
    $document = $null
    try { $document = [System.Text.Json.JsonDocument]::Parse($Content) }
    catch { return 'invalid_json' }
    try {
        if ($document.RootElement.ValueKind -ne [System.Text.Json.JsonValueKind]::Object) { return 'not_object' }
        $fields = @($document.RootElement.EnumerateObject())
        if ($fields.Count -ne 1 -or $fields[0].Name -cne 'status') { return 'wrong_properties' }
        if ($fields[0].Value.ValueKind -ne [System.Text.Json.JsonValueKind]::String) { return 'wrong_value_type' }
        if ($fields[0].Value.GetString() -cne 'ok') { return 'wrong_value' }
        return 'valid'
    }
    finally { $document.Dispose() }
}

function Test-ProbeRequest($Request) {
    $expectedNames = @('model','messages','stream','max_tokens','reasoning_effort','temperature','top_p','response_format')
    $names = @($Request.PSObject.Properties.Name)
    if ($names.Count -ne $expectedNames.Count -or @($names | Where-Object { $_ -cnotin $expectedNames }).Count) { return $false }
    if ($Request.model -cne 'deepseek-ai/DeepSeek-V4-Flash-0731' -or $Request.stream -isnot [bool] -or $Request.stream -ne $false -or $Request.max_tokens -ne 2048 -or $Request.reasoning_effort -cne 'low' -or $Request.temperature -ne 1 -or $Request.top_p -ne 1) { return $false }
    if ($Request.messages -isnot [array] -or $Request.messages.Count -ne 1) { return $false }
    $message = $Request.messages[0]
    if (@($message.PSObject.Properties).Count -ne 2 -or $message.role -cne 'user' -or $message.content -cne 'Return exactly this JSON object and nothing else: {"status":"ok"}. Do not use tools.') { return $false }
    $format = $Request.response_format
    $schema = $format.json_schema
    if (@($format.PSObject.Properties).Count -ne 2 -or $format.type -cne 'json_schema' -or @($schema.PSObject.Properties).Count -ne 3 -or $schema.name -cne 'connection_test' -or $schema.strict -isnot [bool] -or $schema.strict -ne $true) { return $false }
    $shape = $schema.schema
    if (@($shape.PSObject.Properties).Count -ne 4 -or $shape.type -cne 'object' -or $shape.additionalProperties -isnot [bool] -or $shape.additionalProperties -ne $false -or $shape.required -isnot [array] -or $shape.required.Count -ne 1 -or $shape.required[0] -cne 'status') { return $false }
    $property = $shape.properties.status
    if (@($shape.properties.PSObject.Properties).Count -ne 1 -or @($property.PSObject.Properties).Count -ne 2 -or $property.type -cne 'string' -or $property.enum -isnot [array] -or $property.enum.Count -ne 1 -or $property.enum[0] -cne 'ok') { return $false }
    return $true
}

function Invoke-FhgenieProbe {
    param([string]$Directory = $PSScriptRoot, [switch]$ExecuteOnce)
    $summary = [ordered]@{
        status = 'check_only'; key_exists = [bool](Test-Path -LiteralPath $script:ProbeKeyPath)
        network_requests = 0; http_status = $null; observed_model = $null; model_matches_requested = $null
        plan_hashes_valid = $false; request_valid = $false
        prompt_tokens = $null; completion_tokens = $null; elapsed_ms = $null
        system_fingerprint = $null; reasoning_content_present = $false
        provider_error_type = $null; provider_error_code = $null; provider_error_param = $null
        final_content_kind = $null; final_content_utf8_bytes = $null; final_json_status = $null; final_capture_status = 'not_reached'
    }
    $secret = $null; $pointer = [IntPtr]::Zero; $plain = $null; $headers = $null; $reserved = $false
    $attemptPath = Join-Path $Directory 'attempt.json'
    $timer = [Diagnostics.Stopwatch]::new()
    try {
        if ($ExecuteOnce -and (Test-Path -LiteralPath $attemptPath)) { throw 'attempt_already_reserved' }
        $requestPath = Join-Path $Directory 'request.json'
        $planPath = Join-Path $Directory 'plan.json'
        $plan = Get-Content -LiteralPath $planPath -Raw | ConvertFrom-Json
        $requestHash = Get-ProbeHash $requestPath
        if ($plan.request_sha256 -cne $requestHash -or $plan.probe_sha256 -cne (Get-ProbeHash (Join-Path $Directory 'probe.ps1')) -or $plan.tests_sha256 -cne (Get-ProbeHash (Join-Path $Directory 'test_probe.ps1'))) { throw 'approval_hash_mismatch' }
        $summary.plan_hashes_valid = $true
        if ($plan.endpoint -cne $script:ProbeEndpoint -or $plan.timeout_seconds -ne 90) { throw 'plan_invalid' }
        $requestText = [IO.File]::ReadAllText($requestPath)
        $request = ConvertFrom-Json -InputObject $requestText
        if (-not (Test-ProbeRequest $request)) { throw 'request_invalid' }
        $summary.request_valid = $true
        if (-not $ExecuteOnce) { return [pscustomobject]$summary }
        $approvalPath = Join-Path $Directory 'approval.json'
        if (-not (Test-Path -LiteralPath $approvalPath)) { throw 'approval_missing' }
        $approval = Get-Content -LiteralPath $approvalPath -Raw | ConvertFrom-Json
        if ($approval.approved -isnot [bool] -or $approval.approved -ne $true -or $approval.reviewer -cne 'Milad Morad' -or [string]::IsNullOrWhiteSpace($approval.response) -or [string]::IsNullOrWhiteSpace($approval.date)) { throw 'approval_invalid' }
        if ($approval.plan_sha256 -cne (Get-ProbeHash $planPath) -or $approval.request_sha256 -cne $requestHash) { throw 'approval_hash_mismatch' }
        # CreateNew makes this an exclusive, durable reservation. Never delete/reuse it,
        # even if key decryption, HTTP, validation, or result persistence fails.
        $reservation = [IO.File]::Open($attemptPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $reserved = $true
        try {
            $bytes = [Text.Encoding]::UTF8.GetBytes((@{status='reserved';reserved_at_utc=[DateTime]::UtcNow.ToString('o');request_sha256=$requestHash;plan_sha256=$approval.plan_sha256} | ConvertTo-Json))
            $reservation.Write($bytes, 0, $bytes.Length)
            $reservation.Flush($true)
        } finally { $reservation.Dispose() }
        $secret = Get-ProbeSecret
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
        if ([string]::IsNullOrWhiteSpace($plain) -or $plain -match '[\r\n]') { throw 'credential_invalid' }
        $headers = @{ Authorization = 'Bearer ' + $plain; Accept = 'application/json' }
        $timer.Start()
        $summary.network_requests = 1
        try {
            $response = Invoke-WebRequest -Uri $script:ProbeEndpoint -Method Post -Headers $headers `
                -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($requestText)) `
                -MaximumRedirection 0 -MaximumRetryCount 0 -TimeoutSec 90 -UseBasicParsing -ErrorAction Stop
        } catch {
            if ($null -ne $_.Exception.Response) {
                try { $status = [int]$_.Exception.Response.StatusCode; if ($status -ge 100 -and $status -le 599) { $summary.http_status = $status } } catch { }
            }
            # Optional diagnostic identifiers only; never emit the provider message/body.
            $errorText = [string]$_.ErrorDetails.Message
            if ($errorText.Length -le 65536 -and -not $errorText.Contains($plain)) {
                try {
                    $provider = (ConvertFrom-Json -InputObject $errorText).error
                    foreach ($field in @('type','code','param')) {
                        $identifier = $provider.$field
                        if ($identifier -is [string] -and -not $identifier.Contains($plain) -and $identifier -cmatch '^[A-Za-z][A-Za-z0-9_.\[\]-]{0,79}$') { $summary['provider_error_' + $field] = $identifier }
                    }
                } catch { }
            }
            throw 'http_error'
        } finally { $timer.Stop(); $summary.elapsed_ms = $timer.ElapsedMilliseconds }
        $summary.http_status = [int]$response.StatusCode
        if ($summary.http_status -ne 200) { throw 'http_error' }
        $body = [string]$response.Content
        if ($body.Length -gt 1048576 -or $body.Contains($plain)) { throw 'response_rejected' }
        try { $data = ConvertFrom-Json -InputObject $body } catch { throw 'response_invalid_json' }
        foreach ($candidate in @($data.model, $data.system_fingerprint)) {
            if ($candidate -is [string] -and $candidate.Contains($plain)) { throw 'response_rejected' }
        }
        if ($data.model -is [string] -and $data.model -cmatch '^[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}$') { $summary.observed_model = $data.model } else { throw 'response_model_invalid' }
        $summary.model_matches_requested = $data.model -ceq $request.model
        if ($data.system_fingerprint -is [string] -and $data.system_fingerprint -cmatch '^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$') { $summary.system_fingerprint = $data.system_fingerprint }
        if ($null -ne $data.usage -and (Test-ProbeCount $data.usage.prompt_tokens) -and (Test-ProbeCount $data.usage.completion_tokens)) {
            $summary.prompt_tokens = $data.usage.prompt_tokens; $summary.completion_tokens = $data.usage.completion_tokens
        } else { throw 'response_usage_unknown' }
        if ($data.choices -isnot [array] -or $data.choices.Count -ne 1) { throw 'response_choice_invalid' }
        $choice = $data.choices[0]; $message = $choice.message
        # Capture only the final channel, never the separate reasoning field.
        # A gateway may put reasoning into the final channel; do not relabel it.
        $summary.final_content_kind = if ($null -eq $message.content) { 'null' } elseif ($message.content -is [string]) { 'string' } else { 'other' }
        $summary.final_capture_status = 'not_string'
        if ($message.content -is [string]) {
            if ($message.content.Contains($plain)) { $summary.final_capture_status = 'credential_rejected'; throw 'response_rejected' }
            $summary.final_content_utf8_bytes = [Text.Encoding]::UTF8.GetByteCount($message.content)
            $summary.final_capture_status = 'skipped_size_limit'
            if ($summary.final_content_utf8_bytes -le 16384) {
                $finalRecord = @{content=$message.content;channel='message.content';content_utf8_bytes=$summary.final_content_utf8_bytes}
                try {
                    [IO.File]::WriteAllText((Join-Path $Directory 'final-content.json'), ($finalRecord | ConvertTo-Json -Depth 3), [Text.UTF8Encoding]::new($false))
                    $summary.final_capture_status = 'saved'
                } catch { $summary.final_capture_status = 'write_failed'; throw 'capture_write_failed' }
            }
        }
        $summary.final_json_status = Get-FinalJsonStatus $message.content
        if ($choice.finish_reason -cne 'stop') { throw 'response_finish_invalid' }
        if ($message.role -cne 'assistant') { throw 'response_role_invalid' }
        if (($null -ne $message.tool_calls -and ($message.tool_calls -isnot [array] -or $message.tool_calls.Count -gt 0)) -or $null -ne $message.function_call) { throw 'response_tool_call' }
        if ($null -ne $message.refusal -and $message.refusal -cne '') { throw 'response_refusal' }
        if ($null -ne $message.reasoning_content -and $message.reasoning_content -cne '') { $summary.reasoning_content_present = $true }
        if ($summary.final_json_status -cne 'valid') { throw 'response_content_invalid' }
        $summary.status = 'success'
    } catch {
        $safeCodes = @('attempt_already_reserved','approval_missing','approval_invalid','approval_hash_mismatch','plan_invalid','request_invalid','credential_invalid','http_error','response_rejected','response_invalid_json','response_model_invalid','response_usage_unknown','response_choice_invalid','response_finish_invalid','response_role_invalid','response_tool_call','response_refusal','response_content_invalid','capture_write_failed')
        $summary.status = if ($_.Exception.Message -cin $safeCodes) { $_.Exception.Message } else { 'local_error' }
    } finally {
        if ($null -ne $headers) { $headers.Clear() }
        $plain = $null; $body = $null; $errorText = $null
        if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
        if ($null -ne $secret) { $secret.Dispose() }
    }
    if ($reserved) {
        try { [IO.File]::WriteAllText((Join-Path $Directory 'result.json'), ([pscustomobject]$summary | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false)) }
        catch { $summary.status = 'result_write_failed' }
    }
    return [pscustomobject]$summary
}

if ($MyInvocation.InvocationName -ne '.') {
    Invoke-FhgenieProbe -Directory $PSScriptRoot -ExecuteOnce:$ExecuteOnce | ConvertTo-Json -Depth 4
}
