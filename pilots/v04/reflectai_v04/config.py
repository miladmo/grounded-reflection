"""Explicit offline defaults and bounded A/B/C execution."""

from typing import Literal

from pydantic import Field, model_validator

from grounded_reflection.models import Contract, Text

MATERIAL_REVISION = 'v04-amendment-03-r2'
DEVELOPMENT_HISTORY_SEED = 44321
DEVELOPMENT_FUTURE_SEED = 44322
DEVELOPMENT_ORDER_SEED = 44323
REVIEW_HISTORY_SEED = 44331
REVIEW_FUTURE_SEED = 44332
FHGENIE_MODEL = 'deepseek-ai/DeepSeek-V4-Flash-0731'
# The address is configured locally and verified by hash in fhgenie_transport.
FHGENIE_ENDPOINT = '<FHGENIE_ENDPOINT>'
# Amendment 5: reasoning high (contract test 2026-09-30) and a 32,768-token output limit.
FHGENIE_REASONING_EFFORT = 'high'
FHGENIE_MAX_OUTPUT_TOKENS = 32768
# Amendment 5: the 20th isolated response failure stops further scheduling.
MAX_RESPONSE_FAILURES = 19


class RunConfig(Contract):
    protocol: Literal['pilot-v0.4'] = 'pilot-v0.4'
    material_revision: Literal['v04-amendment-03-r2'] = MATERIAL_REVISION
    backend: Literal['mock', 'codex', 'fhgenie'] = 'mock'
    model: Text = 'offline-mock'
    reasoning_effort: Literal['medium', 'high'] = 'medium'
    api_endpoint: Literal['<FHGENIE_ENDPOINT>'] | None = None
    max_output_tokens: int | None = Field(default=None, ge=2048, le=FHGENIE_MAX_OUTPUT_TOKENS, strict=True)
    pwsh_executable: Text | None = None
    pwsh_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    history_seed: int = DEVELOPMENT_HISTORY_SEED
    future_seed: int = DEVELOPMENT_FUTURE_SEED
    order_seed: int = DEVELOPMENT_ORDER_SEED
    max_calls: int = Field(default=200, ge=1, le=200)
    max_reported_tokens: int = Field(default=6_000_000, ge=1, le=6_000_000)
    max_response_failures: int = Field(default=MAX_RESPONSE_FAILURES, ge=0,
                                       le=MAX_RESPONSE_FAILURES, strict=True)
    timeout_seconds: int = Field(default=420, ge=1)

    @property
    def is_live(self) -> bool:
        return self.backend in ('codex', 'fhgenie')

    @model_validator(mode='after')
    def explicit_backend(self):
        if self.backend == 'mock' and self.model != 'offline-mock':
            raise ValueError('Mock runs must be labelled offline-mock.')
        if self.backend == 'codex' and self.model != 'gpt-6-sol':
            raise ValueError('The registered Codex model is gpt-6-sol.')
        if self.backend == 'fhgenie':
            if self.model != FHGENIE_MODEL or self.reasoning_effort != FHGENIE_REASONING_EFFORT:
                raise ValueError('FHGenie requires deepseek-ai/DeepSeek-V4-Flash-0731 with high reasoning.')
            if self.api_endpoint != FHGENIE_ENDPOINT or self.max_output_tokens is None:
                raise ValueError('FHGenie requires the registered endpoint and an explicit output-token limit.')
            if self.pwsh_executable is None or self.pwsh_sha256 is None:
                raise ValueError('FHGenie requires a pinned PowerShell 7 executable and its SHA-256.')
        elif (self.reasoning_effort != 'medium' or self.api_endpoint is not None
              or self.max_output_tokens is not None or self.pwsh_executable is not None
              or self.pwsh_sha256 is not None):
            raise ValueError('Mock and Codex require medium reasoning without FHGenie API settings.')
        return self
