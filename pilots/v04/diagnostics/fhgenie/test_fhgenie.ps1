$ErrorActionPreference = 'Stop'
$helper = Join-Path $PSScriptRoot 'fhgenie.ps1'
$parseErrors = $null
$tokens = $null
$null = [System.Management.Automation.Language.Parser]::ParseFile($helper, [ref]$tokens, [ref]$parseErrors)
if ($parseErrors.Count -ne 0) { throw 'Helper syntax check failed.' }
. $helper
$count = 0

function Assert-True([bool]$Condition, [string]$Label) {
    if (-not $Condition) { throw "Test failed: $Label" }
}

$modelList = ConvertTo-ModelList '{"data":[{"id":"org/model-v1","private":"not exported"},{"id":"org/model-v1"},{"id":"model_2"}]}'
Assert-True ($modelList.models.Count -eq 2) 'distinct model identifiers'
Assert-True (-not (($modelList | ConvertTo-Json) -match 'private|not exported')) 'only identifiers retained'
$count++
Assert-True ((ConvertTo-ModelList '{"data":[]}').models.Count -eq 0) 'empty list retained'
$count++
foreach ($invalid in @('invalid json', '{}', '{"data":{}}', '{"data":[{"id":7}]}', '{"data":[{"id":"bad\nidentifier"}]}', ('{"data":[{"id":"' + ('x' * 201) + '"}]}'))) {
    $rejected = $false
    try { $null = ConvertTo-ModelList $invalid } catch { $rejected = $true }
    Assert-True $rejected 'invalid catalog rejected'
    $count++
}

# The only key in this test is a dummy value in a temporary local file.
$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ('reflectai-fhgenie-test-' + [Guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($temporary) | Out-Null
$script:KeyPath = Join-Path $temporary 'dummy.dpapi'
$dummyText = 'test-only-dummy-key-92'
$dummy = ConvertTo-SecureString $dummyText -AsPlainText -Force
try { [System.IO.File]::WriteAllText($script:KeyPath, (ConvertFrom-SecureString $dummy)) }
finally { $dummy.Dispose() }
$script:RequestCount = 0
$script:Scenario = 'success'
function Invoke-WebRequest {
    param($Uri, $Method, $Headers, $MaximumRedirection, $TimeoutSec, [switch]$UseBasicParsing, $ErrorAction)
    $script:RequestCount++
    Assert-True ($Uri -eq '<FHGENIE_MODELS_ENDPOINT>') 'fixed destination'
    Assert-True ($Method -eq 'Get' -and $MaximumRedirection -eq 0 -and $TimeoutSec -eq 30) 'one bounded GET'
    Assert-True ($Headers.Authorization -eq ('Bearer ' + $dummyText)) 'dummy authentication'
    if ($script:Scenario -eq 'failure') { throw 'Dummy failure containing test-only-dummy-key-92' }
    if ($script:Scenario -eq 'credential_echo') {
        return [pscustomobject]@{ StatusCode = 200; Content = '{"data":[{"id":"test-only-dummy-key-92"}]}' }
    }
    [pscustomobject]@{ StatusCode = 200; Content = '{"data":[{"id":"fixture-model"}]}' }
}
try {
    $output = Get-FhgenieModels
    $parsed = ConvertFrom-Json $output
    Assert-True ($parsed.inference_calls -eq 0 -and $parsed.models[0] -eq 'fixture-model') 'catalog result'
    Assert-True ($script:RequestCount -eq 1 -and -not $output.Contains($dummyText)) 'one request and no key output'
    $count++
    foreach ($scenario in @('failure', 'credential_echo')) {
        $script:Scenario = $scenario
        $before = $script:RequestCount
        $rejected = $false
        try { $null = Get-FhgenieModels }
        catch {
            $rejected = $true
            Assert-True (-not $_.Exception.Message.Contains($dummyText)) 'sanitized failure'
        }
        Assert-True ($rejected -and $script:RequestCount -eq ($before + 1)) 'failure never retries'
        $count++
    }
}
finally {
    [System.IO.File]::Delete($script:KeyPath)
    [System.IO.Directory]::Delete($temporary, $false)
}
Write-Output "Passed $count offline checks. No network requests or model calls."
