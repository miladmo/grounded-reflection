"""Research infrastructure for evidence-grounded agent adaptation."""

from .models import (
    CandidateUpdate, EvidenceReference, Hypothesis, Scope, SplitManifest, WorkEpisode,
)
from .workflow import assess_candidate, select_update

__version__ = "0.1.0.dev1"
__all__ = ["CandidateUpdate", "EvidenceReference", "Hypothesis", "Scope",
           "SplitManifest", "WorkEpisode", "assess_candidate", "select_update"]
