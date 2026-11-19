"""Atreyu & Falkor — Autonomous Task Agent & Luckdragon Recovery.

"Never give up, and good luck will find you."
— Falkor, The NeverEnding Story

Atreyu acts as the autonomous scout across the codebase or environment.
Falkor provides optimistic recovery, retries, and high-speed retrieval.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional
import os


@dataclass
class ScoutReport:
    task: str
    files_scanned: int
    findings: List[str]
    falkor_rescues: int
    verdict: str


class AtreyuAgent:
    """The brave plains scout. Explores the project filesystem without fear."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root = root_dir or Path.cwd()
        self.scanned_paths: List[Path] = []
        self.falkor = FalkorRescue()

    def scout(self, task: str) -> ScoutReport:
        """Execute a reconnaissance mission across the workspace."""
        findings = []
        files = []

        try:
            for p in self.root.glob("**/*"):
                if any(part.startswith(".") for part in p.parts):
                    continue
                if p.is_file():
                    files.append(p)
                    if len(files) >= 50:
                        break
        except Exception as e:
            self.falkor.intervene(f"Filesystem scan error: {e}")

        # Scan for interesting landmarks
        py_files = [f for f in files if f.suffix == ".py"]
        doc_files = [f for f in files if f.suffix in (".md", ".txt", ".rst")]

        findings.append(f"Discovered {len(files)} total artifacts across {self.root.name}.")
        findings.append(f"Core logic artifacts: {len(py_files)} Python modules.")
        findings.append(f"Scrolls and documentation: {len(doc_files)} files.")

        if "test" in task.lower():
            test_files = [f for f in files if "test" in f.name.lower()]
            findings.append(f"Identified {len(test_files)} testing harnesses.")
            verdict = "Test boundaries mapped. Plains of verification clear."
        elif "build" in task.lower():
            verdict = "Artifact structures identified. Ready to forge."
        else:
            verdict = f"Reconnaissance complete for task: '{task}'."

        return ScoutReport(
            task=task,
            files_scanned=len(files),
            findings=findings,
            falkor_rescues=self.falkor.interventions,
            verdict=verdict,
        )


class FalkorRescue:
    """The Luckdragon. Handles resilient retries and optimistic escapes."""

    def __init__(self):
        self.interventions = 0

    def intervene(self, reason: str) -> str:
        self.interventions += 1
        return f"Falkor swoops through the Swamps of Sadness: recovered from [{reason}]."
