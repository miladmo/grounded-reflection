#Requires -Version 7.0
# One request, with no retry, redirect, tool, transcript, or session support.
# Dot-sourcing defines functions only, enabling tests with an in-memory fake key.
$ErrorActionPreference = 'Stop'
# The endpoint is supplied by the caller from local configuration and must match
# this pinned SHA-256 before any credential access. The address is not published.
$script:FhgenieEndpointSha256 = '36247a636ec109c62faa6d828357e6027571e8f56e1c6890e8e0d169acc730db'

function Test-FhgenieEndpoint($Value) {
    if ($Value -isnot [string] -or [string]::IsNullOrWhiteSpace($Value)) { return $false }
    $digest = [System.Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($Value))
    return ([Convert]::ToHexString($digest).ToLowerInvariant() -ceq $script:FhgenieEndpointSha256)
}

function Get-FhgenieSecret {
    $keyPath = Join-Path $env:LOCALAPPDATA 'reflectAI/fhgenie-api-key.dpapi'
    ConvertTo-SecureString -String ([IO.File]::ReadAllText($keyPath))
}

function Test-FhgenieCount($Value) {
    ($Value -is [int] -or $Value -is [long] -or $Value -is [System.Numerics.BigInteger]) -and
        $Value -ge 0 -and $Value -le [long]::MaxValue
}

function Test-FhgenieRequest($InputRecord) {
    if ($null -eq $InputRecord -or @($InputRecord.PSObject.Properties).Count -ne 3 -or
        'request' -cnotin @($InputRecord.PSObject.Properties.Name) -or
        'endpoint' -cnotin @($InputRecord.PSObject.Properties.Name) -or
        -not (Test-FhgenieEndpoint $InputRecord.endpoint) -or
        'timeout_seconds' -cnotin @($InputRecord.PSObject.Properties.Name) -or
        -not (Test-FhgenieCount $InputRecord.timeout_seconds) -or
        $InputRecord.timeout_seconds -le 0 -or $InputRecord.timeout_seconds -gt [int]::MaxValue) { return $false }
    $request = $InputRecord.request
    $expectedNames = @('model','messages','stream','max_tokens','reasoning_effort','temperature','top_p')
    $names = @($request.PSObject.Properties.Name)
    if ($names.Count -ne $expectedNames.Count -or @($names | Where-Object { $_ -cnotin $expectedNames }).Count) { return $false }
    if ($request.model -cne 'deepseek-ai/DeepSeek-V4-Flash-0731' -or $request.stream -isnot [bool] -or
        $request.stream -ne $false -or -not (Test-FhgenieCount $request.max_tokens) -or
        $request.max_tokens -le 0 -or $request.max_tokens -gt [int]::MaxValue -or
        $request.reasoning_effort -isnot [string] -or $request.reasoning_effort -cnotin @('low','high','max') -or -not (Test-FhgenieCount $request.temperature) -or
        -not (Test-FhgenieCount $request.top_p) -or $request.temperature -ne 1 -or $request.top_p -ne 1) { return $false }
    if ($request.messages -isnot [array] -or $request.messages.Count -ne 2) { return $false }
    foreach ($message in $request.messages) {
        if (@($message.PSObject.Properties).Count -ne 2 -or
            'role' -cnotin @($message.PSObject.Properties.Name) -or
            'content' -cnotin @($message.PSObject.Properties.Name) -or
            $message.content -isnot [string] -or [string]::IsNullOrWhiteSpace($message.content)) { return $false }
    }
    if ($request.messages[0].role -cne 'system' -or $request.messages[1].role -cne 'user') { return $false }
    $prefix = 'Return one JSON object conforming to the JSON schema below. Return only the JSON object, without markdown fences or extra text. Do not use tools. JSON schema: '
    if (-not $request.messages[0].content.StartsWith($prefix, [StringComparison]::Ordinal)) { return $false }
    $schema = $null
    try {
        $schema = [System.Text.Json.JsonDocument]::Parse($request.messages[0].content.Substring($prefix.Length))
        if ($schema.RootElement.ValueKind -ne [System.Text.Json.JsonValueKind]::Object) { return $false }
    } catch { return $false } finally { if ($null -ne $schema) { $schema.Dispose() } }
    return $true
}

function Test-FhgenieJsonProperties([System.Text.Json.JsonElement]$Element) {
    # ConvertFrom-Json otherwise silently accepts duplicate provider properties.
    if ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Object) {
        $names = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        foreach ($property in $Element.EnumerateObject()) {
            if (-not $names.Add($property.Name) -or -not (Test-FhgenieJsonProperties $property.Value)) { return $false }
        }
    } elseif ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Array) {
        foreach ($item in $Element.EnumerateArray()) {
            if (-not (Test-FhgenieJsonProperties $item)) { return $false }
        }
    }
    return $true
}

function Invoke-FhgenieRequest([string]$InputText) {
    $result = [ordered]@{
        schema_version = 1; status = 'process_failed'; error_code = $null
        network_requests = 0; http_status = $null; actual_model = $null
        system_fingerprint = $null; finish_reason = $null; role = $null; choice_count = $null
        usage = [ordered]@{input_tokens=$null;output_tokens=$null;cached_input_tokens=$null;reasoning_output_tokens=$null}
        tool_use_detected = $false; reasoning_content_present = $false; refusal_present = $false
        final_content = $null
    }
    $secret = $null; $pointer = [IntPtr]::Zero; $plain = $null; $headers = $null; $document = $null
    $body = $null; $data = $null
    try {
        try {
            $document = [System.Text.Json.JsonDocument]::Parse($InputText)
            if (-not (Test-FhgenieJsonProperties $document.RootElement)) { throw 'request_invalid' }
            $inputRecord = ConvertFrom-Json -InputObject $InputText -Depth 100
            if (-not (Test-FhgenieRequest $inputRecord)) { throw 'request_invalid' }
        } catch { throw 'request_invalid' }
        $requestText = ConvertTo-Json -InputObject $inputRecord.request -Depth 100 -Compress
        try { $secret = Get-FhgenieSecret } catch { throw 'credential_unavailable' }
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
        if ([string]::IsNullOrWhiteSpace($plain) -or $plain -match '[\r\n]') { throw 'credential_invalid' }
        $headers = @{ Authorization = 'Bearer ' + $plain; Accept = 'application/json' }
        $result.network_requests = 1
        try {
            $response = Invoke-WebRequest -Uri $inputRecord.endpoint -Method Post `
                -Headers $headers -ContentType 'application/json; charset=utf-8' `
                -Body ([Text.Encoding]::UTF8.GetBytes($requestText)) -MaximumRedirection 0 `
                -MaximumRetryCount 0 -TimeoutSec $inputRecord.timeout_seconds -UseBasicParsing -ErrorAction Stop
        } catch {
            if ($null -ne $_.Exception.Response) {
                try {
                    $status = [int]$_.Exception.Response.StatusCode
                    if ($status -ge 100 -and $status -le 599) { $result.http_status = $status }
                } catch { }
            }
            # Do not copy exception text, response headers or provider error bodies.
            throw 'http_error'
        }
        $result.http_status = [int]$response.StatusCode
        if ($result.http_status -ne 200) { throw 'http_error' }
        $body = [string]$response.Content
        if ([Text.Encoding]::UTF8.GetByteCount($body) -gt 8388608 -or $body.Contains($plain)) { throw 'response_rejected' }
        try {
            $document.Dispose(); $document = [System.Text.Json.JsonDocument]::Parse($body)
            if ($document.RootElement.ValueKind -ne [System.Text.Json.JsonValueKind]::Object -or
                -not (Test-FhgenieJsonProperties $document.RootElement)) { throw 'response_invalid_json' }
            $data = ConvertFrom-Json -InputObject $body -Depth 100
        } catch { throw 'response_invalid_json' }
        # Encoded/escaped key echoes may only become visible after JSON decoding.
        $decoded = ConvertTo-Json -InputObject $data -Depth 100 -Compress
        if ($decoded.Contains($plain)) { throw 'response_rejected' }
        if ($data.model -is [string] -and $data.model -cmatch '^[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}$') {
            $result.actual_model = $data.model
        }
        if ($data.system_fingerprint -is [string] -and $data.system_fingerprint -cmatch '^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$') {
            $result.system_fingerprint = $data.system_fingerprint
        }
        $usageInvalid = $false
        if ($null -ne $data.usage) {
            foreach ($mapping in @(@('prompt_tokens','input_tokens'),@('completion_tokens','output_tokens'))) {
                $value = $data.usage.($mapping[0])
                if (Test-FhgenieCount $value) { $result.usage[$mapping[1]] = $value }
                elseif ($null -ne $value) { $usageInvalid = $true }
            }
            foreach ($mapping in @(@('prompt_tokens_details','cached_tokens','cached_input_tokens'),
                                    @('completion_tokens_details','reasoning_tokens','reasoning_output_tokens'))) {
                $value = $data.usage.($mapping[0]).($mapping[1])
                if (Test-FhgenieCount $value) { $result.usage[$mapping[2]] = $value }
                elseif ($null -ne $value) { $usageInvalid = $true }
            }
            foreach ($mapping in @(@('cached_input_tokens','input_tokens'),@('reasoning_output_tokens','output_tokens'))) {
                if ($null -ne $result.usage[$mapping[0]] -and $null -ne $result.usage[$mapping[1]] -and
                    $result.usage[$mapping[0]] -gt $result.usage[$mapping[1]]) {
                    $result.usage[$mapping[0]] = $null; $usageInvalid = $true
                }
            }
        }
        if ($data.choices -isnot [array] -or $data.choices.Count -ne 1) { throw 'response_choice_invalid' }
        $result.choice_count = 1
        $choice = $data.choices[0]; $message = $choice.message
        if ($choice.finish_reason -is [string] -and $choice.finish_reason -cmatch '^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$') {
            $result.finish_reason = $choice.finish_reason
        }
        if ($message.role -is [string] -and $message.role -cmatch '^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$') { $result.role = $message.role }
        $result.tool_use_detected = ($null -ne $message.tool_calls -and
            ($message.tool_calls -isnot [array] -or $message.tool_calls.Count -gt 0)) -or $null -ne $message.function_call
        $result.reasoning_content_present = $null -ne $message.reasoning_content -and $message.reasoning_content -cne ''
        $result.refusal_present = $null -ne $message.refusal -and $message.refusal -cne ''
        if ($message.content -is [string] -and [Text.Encoding]::UTF8.GetByteCount($message.content) -le 1048576) {
            if ($message.content.Contains($plain)) { throw 'response_rejected' }
            $result.final_content = $message.content
        }
        if ($null -eq $result.actual_model) { throw 'response_model_invalid' }
        if ($result.actual_model -cne $inputRecord.request.model) { throw 'response_model_mismatch' }
        if ($usageInvalid) { throw 'response_usage_invalid' }
        if ($null -eq $result.usage.input_tokens -or $null -eq $result.usage.output_tokens) { throw 'response_usage_unknown' }
        if ($result.tool_use_detected) { throw 'response_tool_call' }
        if ($result.refusal_present) { throw 'response_refusal' }
        if ($result.finish_reason -cne 'stop') { throw 'response_finish_invalid' }
        if ($result.role -cne 'assistant') { throw 'response_role_invalid' }
        if ($null -eq $result.final_content) { throw 'response_content_invalid' }
        $result.status = 'completed'
    } catch {
        $safeCodes = @('request_invalid','credential_unavailable','credential_invalid','http_error',
            'response_rejected','response_invalid_json','response_model_invalid','response_model_mismatch',
            'response_usage_invalid','response_usage_unknown','response_choice_invalid','response_finish_invalid',
            'response_role_invalid','response_tool_call','response_refusal','response_content_invalid')
        $result.error_code = if ($_.Exception.Message -cin $safeCodes) { $_.Exception.Message } else { 'local_error' }
    } finally {
        if ($null -ne $headers) { $headers.Clear() }
        $plain = $null; $body = $null; $data = $null; $decoded = $null
        if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
        if ($null -ne $secret) { $secret.Dispose() }
        if ($null -ne $document) { $document.Dispose() }
    }
    return [pscustomobject]$result
}

if ($MyInvocation.InvocationName -ne '.') {
    [Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
    [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
    $result = Invoke-FhgenieRequest -InputText ([Console]::In.ReadToEnd())
    [Console]::Out.WriteLine((ConvertTo-Json -InputObject $result -Depth 6 -Compress))
    if ($result.status -cne 'completed') { exit 1 }
}
