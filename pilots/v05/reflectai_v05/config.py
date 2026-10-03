"""Run configuration for the three v0.5 phases (protocol, Procedure and budgets)."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from grounded_reflection.models import Contract, Text

FHGENIE_MODEL = 'deepseek-ai/DeepSeek-V4-Flash-0731'
SEEDS = {'development': (45021, 45022, 45023), 'review': (45031, 45032, 45033),
         'final_test': (45061, 45062, 45063)}
PHASES = {
    # phase: (split, arms, call cap, token stop)
    'calibration': ('development', ('A', 'B', 'C'), 170, 3_000_000),
    'dcheck': ('development', ('D',), 20, 500_000),
    'main': ('final_test', ('A', 'B', 'C', 'D'), 560, 10_000_000),
}
MAX_OUTPUT_TOKENS = 32_768
PREPARATION_CAP = 300_000


class RunConfig(Contract):
    protocol: Literal['pilot-v0.5'] = 'pilot-v0.5'
    phase: Literal['calibration', 'dcheck', 'main']
    backend: Literal['mock', 'fhgenie'] = 'mock'
    model: Text = 'offline-mock'
    reasoning_effort: Literal['high'] = 'high'
    max_output_tokens: int = Field(default=MAX_OUTPUT_TOKENS, ge=2048, le=MAX_OUTPUT_TOKENS, strict=True)
    pwsh_executable: Text | None = None
    pwsh_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    split: Literal['development', 'final_test']
    history_seed: int
    future_seed: int
    order_seed: int
    arms: list[Literal['A', 'B', 'C', 'D']]
    max_calls: int = Field(ge=1, le=560)
    max_reported_tokens: int = Field(ge=1, le=10_000_000)
    max_response_failures: int = Field(ge=0)
    preparation_cap: int = PREPARATION_CAP
    # Technical correction of 3 October 2026: 420 s could not cover a full 32,768-token
    # output at the observed FHGenie throughput (36 to 221 tokens/s).
    timeout_seconds: int = 1200

    @property
    def is_live(self) -> bool:
        return self.backend == 'fhgenie'

    @model_validator(mode='after')
    def registered(self):
        split, arms, calls, tokens = PHASES[self.phase]
        if self.split != split or tuple(self.arms) != arms:
            raise ValueError('phase split and arms are fixed by the protocol')
        if self.max_calls > calls or self.max_reported_tokens > tokens:
            raise ValueError('limits exceed the approved caps')
        if (self.history_seed, self.future_seed, self.order_seed) != SEEDS[split]:
            raise ValueError('seeds are fixed by the protocol')
        if self.backend == 'fhgenie':
            if self.model != FHGENIE_MODEL or not self.pwsh_executable or not self.pwsh_sha256:
                raise ValueError('FHGenie requires the registered model and a pinned PowerShell 7')
        elif self.model != 'offline-mock' or self.pwsh_executable or self.pwsh_sha256:
            raise ValueError('mock runs are labelled offline-mock and use no PowerShell')
        return self


def phase_config(phase: str, backend: str = 'mock', **live) -> RunConfig:
    split, arms, calls, tokens = PHASES[phase]
    history, future, order = SEEDS[split]
    return RunConfig(phase=phase, backend=backend, split=split, history_seed=history, future_seed=future,
                     order_seed=order, arms=list(arms), max_calls=calls, max_reported_tokens=tokens,
                     max_response_failures=calls // 10, **live)
