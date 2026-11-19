"""The Nothing (Das Nichts) — Entropy and Context Degradation Monitor.

"The Nothing grows. It grows and grows. Soon there will be nothing left."
— Gmork, The NeverEnding Story

In Fantasia CLI, The Nothing models token context degradation, memory leaks,
and prompt drift. It provides visible gauges, entropy warnings, and
pruning recommendations to keep the LLM operator grounded.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EntropyState:
    total_tokens: int
    used_tokens: int
    ratio: float
    threat_level: str
    remedy: str


class NothingGauge:
    """Calculates and monitors the encroachment of The Nothing across the workspace."""

    THRESHOLDS = [
        (0.30, "QUIET", "The borders of Fantasia remain intact. Grounding solid."),
        (0.60, "RESTLESS", "Fringe lands dissolving. Atreyu recommends pruning history."),
        (0.92, "CRITICAL", "The Swamps of Sadness have claimed working memory. Invoke Falkor rescue."),
        (1.00, "THE VOID", "Only a grain of sand remains. Give the Empress a new name."),
    ]

    def __init__(self, context_limit: int = 128_000):
        self.context_limit = context_limit
        self.observed_tokens = 0
        self.void_incursions = 0

    def record_usage(self, token_count: int) -> None:
        self.observed_tokens += max(0, token_count)
        if self.observed_tokens > self.context_limit:
            self.void_incursions += 1

    def assess(self) -> EntropyState:
        ratio = min(1.0, self.observed_tokens / max(1, self.context_limit))
        threat = "QUIET"
        remedy = self.THRESHOLDS[0][2]

        for limit, name, advice in self.THRESHOLDS:
            if ratio <= limit:
                threat = name
                remedy = advice
                break
        else:
            threat = "THE VOID"
            remedy = self.THRESHOLDS[-1][2]

        return EntropyState(
            total_tokens=self.context_limit,
            used_tokens=self.observed_tokens,
            ratio=ratio,
            threat_level=threat,
            remedy=remedy,
        )

    def ascii_radar(self, width: int = 36) -> str:
        """Render a terminal-friendly ASCII radar map of Fantasia vs The Nothing."""
        state = self.assess()
        void_width = int(state.ratio * width)
        fantasia_width = width - void_width
        
        void_part = "░" * void_width
        fantasia_part = "█" * fantasia_width
        return f"[{fantasia_part}{void_part}] {state.ratio * 100:.1f}% VOID"
