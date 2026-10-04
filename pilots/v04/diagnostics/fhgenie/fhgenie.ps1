[CmdletBinding()]
param(
    [ValidateSet('Status', 'StoreKey', 'Models')]
    [string]$Action = 'Status'
)

$ErrorActionPreference = 'Stop'
$script:KeyPath = Join-Path $env:LOCALAPPDATA 'reflectAI/fhgenie-api-key.dpapi'
$script:ModelsUri = '<FHGENIE_MODELS_ENDPOINT>'

function ConvertTo-ModelList {
    param([string]$Content)
    try { $catalog = ConvertFrom-Json -InputObject $Content -ErrorAction Stop }
    catch { throw 'The model endpoint did not return valid JSON.' }
    if ($null -eq $catalog -or $null -eq $catalog.data -or $catalog.data -isnot [array]) {
        throw 'Unexpected model catalog. Expected a JSON object with a data array.'
    }
    $ids = foreach ($entry in $catalog.data) {
        if ($entry.id -isnot [string] -or $entry.id -cnotmatch '^[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}$') {
            throw 'Unexpected model identifier. No raw response was printed.'
        }
        $entry.id
    }
    [pscustomobject]@{ models = @($ids | Sort-Object -Unique) }
}

function Save-FhgenieKey {
    if (Test-Path -LiteralPath $script:KeyPath) {
        throw 'A local key already exists. It has not been overwritten.'
    }
    $secret = Read-Host 'FHGenie API key (hidden input)' -AsSecureString
    try {
        if ($secret.Length -eq 0) { throw 'No key entered.' }
        $protected = ConvertFrom-SecureString -SecureString $secret
        $folder = Split-Path -Parent $script:KeyPath
        [System.IO.Directory]::CreateDirectory($folder) | Out-Null
        $stream = [System.IO.File]::Open($script:KeyPath, [System.IO.FileMode]::CreateNew)
        try {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($protected)
            $stream.Write($bytes, 0, $bytes.Length)
        }
        finally { $stream.Dispose() }
        Write-Output 'Key saved with Windows user encryption. No network request was made.'
    }
    finally { if ($null -ne $secret) { $secret.Dispose() } }
}

function Get-FhgenieModels {
    if (-not (Test-Path -LiteralPath $script:KeyPath)) {
        throw 'No local key found. Run StoreKey first.'
    }
    $secret = $null
    $buffer = [IntPtr]::Zero
    $plain = $null
    $headers = $null
    try {
        $secret = ConvertTo-SecureString -String ([System.IO.File]::ReadAllText($script:KeyPath))
        $buffer = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
        $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($buffer)
        if ([string]::IsNullOrWhiteSpace($plain) -or $plain -match '[\r\n]') {
            throw 'The stored key is empty or contains a line break.'
        }
        $headers = @{ Authorization = 'Bearer ' + $plain; Accept = 'application/json' }
        try {
            $response = Invoke-WebRequest -Uri $script:ModelsUri -Method Get -Headers $headers `
                -MaximumRedirection 0 -TimeoutSec 30 -UseBasicParsing -ErrorAction Stop
        }
        catch {
            $status = 0
            if ($null -ne $_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
            if ($status -gt 0) { throw "Model catalog request failed (HTTP $status). No retry was made." }
            throw 'Model catalog request failed. Check connectivity or the required authentication method. No retry was made.'
        }
        if ([int]$response.StatusCode -ne 200) { throw 'The model endpoint did not return HTTP 200.' }
        $content = [string]$response.Content
        if ($content.Length -gt 1048576) { throw 'Model catalog is larger than expected.' }
        if ($content.Contains($plain)) { throw 'Response unexpectedly contains credential material. It was not printed.' }
        $models = ConvertTo-ModelList -Content $content
        [pscustomobject]@{
            endpoint = $script:ModelsUri
            models = @($models.models)
            inference_calls = 0
        } | ConvertTo-Json -Depth 3
    }
    finally {
        if ($null -ne $headers) { $headers.Clear() }
        $plain = $null
        if ($buffer -ne [IntPtr]::Zero) { [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($buffer) }
        if ($null -ne $secret) { $secret.Dispose() }
    }
}

if ($MyInvocation.InvocationName -eq '.') { return }
switch ($Action) {
    'StoreKey' { Save-FhgenieKey }
    'Models' { Get-FhgenieModels }
    'Status' {
        [pscustomobject]@{
            key_exists = Test-Path -LiteralPath $script:KeyPath
            key_path = $script:KeyPath
            network_requests = 0
        } | ConvertTo-Json
    }
}
