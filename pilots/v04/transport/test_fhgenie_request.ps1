#Requires -Version 7.0
# OFFLINE ONLY: both credential access and HTTP are replaced before invocation.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'fhgenie-request.ps1')

# Offline endpoint fixture; the real address is never part of this repository.
$script:TestEndpoint = 'https://fhgenie.invalid/v1/chat/completions'
$script:FhgenieEndpointSha256 = [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData(
    [Text.Encoding]::UTF8.GetBytes($script:TestEndpoint))).ToLowerInvariant()
$script:FakeCredential = 'OFFLINE-FIXTURE-KEY-NOT-A-REAL-CREDENTIAL'
$script:PrivateReasoning = 'PRIVATE-REASONING-MUST-NEVER-BE-RETURNED'
$script:EvaluatorCanary = 'EVALUATOR-FUTURE-TASK-FILE-CANARY'
$script:HttpCalls = 0
$script:SecretCalls = 0
$script:Mode = 'success'
$script:Passed = 0

function Assert-Offline($Condition, [string]$Message) {
    if (-not $Condition) { throw ('Offline assertion failed: ' + $Message) }
}

function Get-FhgenieSecret {
    $script:SecretCalls++
    ConvertTo-SecureString -String $script:FakeCredential -AsPlainText -Force
}

function New-OfflineInput {
    [pscustomobject]@{
        timeout_seconds = 90
        endpoint = $script:TestEndpoint
        request = [pscustomobject]@{
            model = 'deepseek-ai/DeepSeek-V4-Flash-0731'
            messages = @(
                [pscustomobject]@{role='system';content='Return one JSON object conforming to the JSON schema below. Return only the JSON object, without markdown fences or extra text. Do not use tools. JSON schema: {"type":"object","properties":{"answer":{"type":"string"}},"required":["answer"],"additionalProperties":false}'},
                [pscustomobject]@{role='user';content="Public prompt only`nUnchanged ünicode."}
            )
            stream = $false; max_tokens = 16384; reasoning_effort = 'low'; temperature = 1; top_p = 1
        }
    }
}

function Invoke-WebRequest {
    param($Uri, $Method, $Headers, $ContentType, $Body, $MaximumRedirection,
          $MaximumRetryCount, $TimeoutSec, [switch]$UseBasicParsing, $ErrorAction)
    $script:HttpCalls++
    Assert-Offline ($Uri -ceq $script:TestEndpoint) 'hash-verified endpoint'
    Assert-Offline ($Method -ceq 'Post') 'POST method'
    Assert-Offline ($Headers.Authorization -ceq ('Bearer ' + $script:FakeCredential)) 'in-process bearer auth'
    Assert-Offline ($MaximumRetryCount -eq 0 -and $MaximumRedirection -eq 0) 'no retries or redirects'
    Assert-Offline ($TimeoutSec -eq 90) 'bounded timeout'
    Assert-Offline ($ContentType -ceq 'application/json; charset=utf-8') 'UTF-8 content type'
    $text = [Text.Encoding]::UTF8.GetString($Body)
    $request = ConvertFrom-Json -InputObject $text
    Assert-Offline (@($request.PSObject.Properties).Count -eq 7) 'exact body fields'
    Assert-Offline ($request.messages.Count -eq 2) 'only two messages'
    Assert-Offline ($request.messages[0].role -ceq 'system' -and $request.messages[1].role -ceq 'user') 'schema and prompt roles'
    Assert-Offline ($request.messages[1].content -ceq "Public prompt only`nUnchanged ünicode.") 'unchanged user prompt'
    Assert-Offline ($request.messages[0].content -ceq (New-OfflineInput).request.messages[0].content) 'public schema only'
    Assert-Offline (-not $text.Contains($script:EvaluatorCanary)) 'no private surrounding data'
    Assert-Offline (-not $text.Contains($script:FakeCredential)) 'no credentials in body'
    foreach ($field in @('response_format','tools','tool_choice','functions','files','previous_response_id','session')) {
        Assert-Offline ($field -cnotin @($request.PSObject.Properties.Name)) 'no schema mode or extra capabilities'
    }
    if ($script:Mode -eq 'http_error') { throw ('Untrusted provider error ' + $script:FakeCredential) }
    $message = [ordered]@{role='assistant';content='{"answer":"ok"}';tool_calls=@();reasoning_content=$script:PrivateReasoning}
    $choice = [ordered]@{finish_reason='stop';message=$message}
    $data = [ordered]@{
        model='deepseek-ai/DeepSeek-V4-Flash-0731'; system_fingerprint='fixture-fingerprint'
        usage=[ordered]@{prompt_tokens=24;completion_tokens=33}; choices=@($choice)
    }
    switch ($script:Mode) {
        'missing_usage' { $data.Remove('usage') }
        'partial_usage' { $data.usage.Remove('completion_tokens') }
        'invalid_usage' { $data.usage.prompt_tokens = $true }
        'negative_usage' { $data.usage.completion_tokens = -1 }
        'usage_details' {
            $data.usage.prompt_tokens_details = @{cached_tokens=0}
            $data.usage.completion_tokens_details = @{reasoning_tokens=5}
        }
        'invalid_subset' { $data.usage.prompt_tokens_details = @{cached_tokens=25} }
        'wrong_model' { $data.model = 'another-model' }
        'truncated' { $choice.finish_reason = 'length' }
        'wrong_role' { $message.role = 'tool' }
        'tool_calls' { $message.tool_calls = @(@{type='function';function=@{name='forbidden'}}) }
        'invalid_tool_calls' { $message.tool_calls = 'invalid' }
        'function_call' { $message.function_call = @{name='forbidden'} }
        'refusal' { $message.refusal = 'Private refusal text should not be emitted.' }
        'null_content' { $message.content = $null }
        'nonstring_content' { $message.content = @{answer='ok'} }
        'final_key_echo' { $message.content = '{"answer":"' + $script:FakeCredential + '"}' }
        'reasoning_key_echo' { $message.reasoning_content = $script:FakeCredential }
        'model_key_echo' { $data.model = $script:FakeCredential }
        'escaped_key_echo' { $message.content = '{"answer":"' + $script:FakeCredential + '"}' }
        'two_choices' { $data.choices = @($choice, $choice) }
        'invalid_final_json' { $message.content = '```json {"answer":"ok"} ```' }
    }
    $bodyText = ConvertTo-Json -InputObject $data -Depth 12 -Compress
    if ($script:Mode -eq 'duplicate_provider_json') { $bodyText = '{"model":"one","model":"two"}' }
    if ($script:Mode -eq 'escaped_key_echo') {
        $encoded = -join ($script:FakeCredential.ToCharArray() | ForEach-Object { '\u{0:x4}' -f [int]$_ })
        $bodyText = $bodyText.Replace($script:FakeCredential, $encoded)
    }
    [pscustomobject]@{StatusCode=200; Content=$bodyText}
}

function Invoke-OfflineCase([string]$Mode, [string]$ExpectedError) {
    $script:Mode = $Mode
    $script:HttpCalls = 0; $script:SecretCalls = 0
    $result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject (New-OfflineInput) -Depth 10)
    Assert-Offline ($script:HttpCalls -eq 1 -and $script:SecretCalls -eq 1) 'exactly one HTTP and fake credential access'
    $serialized = ConvertTo-Json -InputObject $result -Depth 8
    Assert-Offline (-not $serialized.Contains($script:FakeCredential)) 'credential redaction'
    Assert-Offline (-not $serialized.Contains($script:PrivateReasoning)) 'reasoning exclusion'
    Assert-Offline (-not $serialized.Contains('Private refusal text')) 'refusal text exclusion'
    if ($ExpectedError) {
        Assert-Offline ($result.status -ceq 'process_failed' -and $result.error_code -ceq $ExpectedError) ('expected error for ' + $Mode)
    } else {
        Assert-Offline ($result.status -ceq 'completed' -and $null -eq $result.error_code) ('completed ' + $Mode)
    }
    $script:Passed++
    return $result
}

$result = Invoke-OfflineCase 'success' ''
Assert-Offline ($result.final_content -ceq '{"answer":"ok"}') 'final channel capture'
Assert-Offline ($result.reasoning_content_present -eq $true -and $result.tool_use_detected -eq $false) 'empty tool calls accepted'
Assert-Offline ($result.usage.input_tokens -eq 24 -and $result.usage.output_tokens -eq 33) 'base usage normalization'
Assert-Offline ($null -eq $result.usage.cached_input_tokens -and $null -eq $result.usage.reasoning_output_tokens) 'unknown detail counts remain null'
$result = Invoke-OfflineCase 'usage_details' ''
Assert-Offline ($result.usage.cached_input_tokens -eq 0 -and $result.usage.reasoning_output_tokens -eq 5) 'detailed usage normalization'

$failures = @{
    missing_usage='response_usage_unknown'; partial_usage='response_usage_unknown'; invalid_usage='response_usage_invalid'
    negative_usage='response_usage_invalid'; invalid_subset='response_usage_invalid'; wrong_model='response_model_mismatch'
    truncated='response_finish_invalid'; wrong_role='response_role_invalid'; tool_calls='response_tool_call'
    invalid_tool_calls='response_tool_call'; function_call='response_tool_call'; refusal='response_refusal'
    null_content='response_content_invalid'; nonstring_content='response_content_invalid'
    final_key_echo='response_rejected'; reasoning_key_echo='response_rejected'; model_key_echo='response_rejected'
    escaped_key_echo='response_rejected'; two_choices='response_choice_invalid'
    duplicate_provider_json='response_invalid_json'; http_error='http_error'
}
foreach ($case in $failures.GetEnumerator()) {
    $result = Invoke-OfflineCase $case.Key $case.Value
    if ($case.Key -eq 'partial_usage') {
        Assert-Offline ($result.usage.input_tokens -eq 24 -and $null -eq $result.usage.output_tokens) 'partial usage is preserved'
    }
}
$result = Invoke-OfflineCase 'invalid_final_json' ''
Assert-Offline ($result.final_content -ceq '```json {"answer":"ok"} ```') 'driver never repairs JSON; Python validates it'

foreach ($field in @('tools','response_format','previous_response_id','session','files')) {
    $inputRecord = New-OfflineInput
    $inputRecord.request | Add-Member -NotePropertyName $field -NotePropertyValue 'forbidden'
    $script:SecretCalls = 0; $script:HttpCalls = 0
    $result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject $inputRecord -Depth 10)
    Assert-Offline ($result.error_code -ceq 'request_invalid') 'extra request field rejected'
    Assert-Offline ($script:SecretCalls -eq 0 -and $script:HttpCalls -eq 0) 'reject before credential or HTTP'
    $script:Passed++
}
foreach ($effort in @('high','max')) {
    $inputRecord = New-OfflineInput
    $inputRecord.request.reasoning_effort = $effort
    $script:Mode = 'success'; $script:SecretCalls = 0; $script:HttpCalls = 0
    $result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject $inputRecord -Depth 10)
    Assert-Offline ($result.status -ceq 'completed' -and $script:HttpCalls -eq 1) ('documented reasoning level accepted: ' + $effort)
    $script:Passed++
}
foreach ($effort in @('medium','xhigh','HIGH','',$null,1)) {
    $inputRecord = New-OfflineInput
    $inputRecord.request.reasoning_effort = $effort
    $script:SecretCalls = 0; $script:HttpCalls = 0
    $result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject $inputRecord -Depth 10)
    Assert-Offline ($result.error_code -ceq 'request_invalid') 'undocumented reasoning level rejected'
    Assert-Offline ($script:SecretCalls -eq 0 -and $script:HttpCalls -eq 0) 'reasoning rejection precedes credential or HTTP'
    $script:Passed++
}
foreach ($endpoint in @('https://example.invalid/v1/chat/completions', '', $null, 7)) {
    $inputRecord = New-OfflineInput
    $inputRecord.endpoint = $endpoint
    $script:SecretCalls = 0; $script:HttpCalls = 0
    $result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject $inputRecord -Depth 10)
    Assert-Offline ($result.error_code -ceq 'request_invalid') 'unverified endpoint rejected'
    Assert-Offline ($script:SecretCalls -eq 0 -and $script:HttpCalls -eq 0) 'endpoint check precedes credential or HTTP'
    $script:Passed++
}
$inputRecord = New-OfflineInput
$inputRecord.PSObject.Properties.Remove('endpoint')
$script:SecretCalls = 0; $script:HttpCalls = 0
$result = Invoke-FhgenieRequest (ConvertTo-Json -InputObject $inputRecord -Depth 10)
Assert-Offline ($result.error_code -ceq 'request_invalid' -and $script:SecretCalls -eq 0) 'missing endpoint rejected'
$script:Passed++
foreach ($text in @('not JSON','{"request":{},"request":{},"timeout_seconds":90}')) {
    $script:SecretCalls = 0; $script:HttpCalls = 0
    $result = Invoke-FhgenieRequest $text
    Assert-Offline ($result.error_code -ceq 'request_invalid') 'malformed input rejected'
    Assert-Offline ($script:SecretCalls -eq 0 -and $script:HttpCalls -eq 0) 'malformed input never reaches credentials or HTTP'
    $script:Passed++
}
Write-Output ("Passed {0} offline FHGenie driver cases; no real credentials or HTTP used." -f $script:Passed)
