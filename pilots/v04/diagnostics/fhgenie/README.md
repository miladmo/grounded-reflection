# FHGenie model discovery

Local setup for the user-provided Fraunhofer on-premises gateway. This is not an
inference backend or a change to the frozen pilot. No model has been selected.

Run `./fhgenie.ps1 -Action StoreKey` interactively in PowerShell. It accepts a hidden
key and stores it under `%LOCALAPPDATA%/reflectAI/fhgenie-api-key.dpapi` using Windows
current-user encryption. It does not contact a service or overwrite an existing
key. No administrator rights are requested. Run this as the same Windows user that
will run the pilot. Other processes under that user can decrypt the key.

`./fhgenie.ps1 -Action Models` makes one authenticated GET to the fixed URL
`<FHGENIE_MODELS_ENDPOINT>`. It uses Bearer authentication, the standard
OpenAI-style convention, which still needs confirmation for this gateway. It does
not try alternative headers, follow redirects, retry or make inference requests.
Only model identifiers are printed. TLS verification and system network settings
are retained. If the gateway requires an institutional network or VPN, that
connection must already be available.

The default `Status` action only checks whether the encrypted key file exists.
`./test_fhgenie.ps1` checks parsing, a dummy-key encryption round trip and the request
boundary entirely offline. The HTTP command is replaced with a local fixture.

Do not infer context limits, structured-output support or model quality from IDs
alone. Confirm the selected model's version and capabilities before implementation
and protocol registration. The list is documented by the user as on-premises only;
public-cloud access requires a separate arrangement. This helper makes no claim
that a deployment or its use is free of charge.
