"""AURYN — The double-ouroboros medallion and token governor.

"DO WHAT THOU WILT" — The inscription on the reverse side.

In Fantasia, AURYN gives the human reader power to create by wishing,
while balancing memory against the void. In this CLI, Auryn acts as the
state governor, session coordinator, and bounded wish router.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import List, Optional, Dict, Any


@dataclass
class Wish:
    """A human intent submitted to Fantasia."""
    prompt: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    wish_id: str = ""
    consumed_memory: str = ""
    status: str = "pending"  # pending, granted, dissolved

    def __post_init__(self):
        if not self.wish_id:
            h = hashlib.sha256(f"{self.timestamp}:{self.prompt}".encode("utf-8")).hexdigest()
            self.wish_id = f"wish_{h[:10]}"


class Auryn:
    """The AURYN talisman. Manages wish ledger and grounds memory against entropy."""

    INSCRIPTION = "DO WHAT THOU WILT"

    def __init__(self, bearer: str = "Bastian Balthazar Bux"):
        self.bearer = bearer
        self.wishes: List[Wish] = []
        self.memories_preserved: List[str] = [
            "the smell of old books in Mr. Coreander's antiquarian shop",
            "the rainy school attic where the journey began",
            "the call in the dark when the Childlike Empress needed a name",
        ]
        self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def wish_count(self) -> int:
        return len(self.wishes)

    @property
    def remaining_memory_anchor(self) -> int:
        """Remaining human ground memories before total immersion in Fantasia."""
        return max(0, len(self.memories_preserved) * 10 - self.wish_count)

    def grant_wish(self, prompt: str) -> Wish:
        """Route a wish through the AURYN talisman."""
        cost = f"anchor_token_{self.wish_count + 1}"
        wish = Wish(
            prompt=prompt,
            consumed_memory=cost,
            status="granted",
        )
        self.wishes.append(wish)
        return wish

    def preserve_memory(self, memory_text: str) -> None:
        """Anchor a new project constraint or human requirement."""
        self.memories_preserved.append(memory_text)

    def talisman_signature(self) -> str:
        """Cryptographic badge of the talisman's current state."""
        payload = f"{self.bearer}:{len(self.wishes)}:{len(self.memories_preserved)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bearer": self.bearer,
            "inscription": self.INSCRIPTION,
            "wishes_granted": len(self.wishes),
            "memories_anchored": len(self.memories_preserved),
            "talisman_signature": self.talisman_signature(),
            "history": [
                {"id": w.wish_id, "prompt": w.prompt, "status": w.status, "time": w.timestamp}
                for w in self.wishes[-5:]
            ]
        }
