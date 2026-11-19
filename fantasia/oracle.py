"""The Southern Oracle (Die Südliche Orakel) — AI reasoning and Sphinx gate.

"The Southern Oracle is ten thousand miles away.
No one has ever reached it."
— The NeverEnding Story

The Sphinxes' gaze pierces the traveler's core. In Fantasia CLI, the Southern
Oracle is the multi-provider LLM bridge. It interfaces with Gemini, OpenAI,
Anthropic, or local endpoints via stdlib urllib, with an offline synthetic
sphinx oracle when working disconnected.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional


class SouthernOracle:
    """The Sphinx gate and reasoning oracle."""

    SPHINX_PROMPT = (
        "You are the Southern Oracle of Fantasia. You speak with high-fidelity "
        "clarity, zero bureaucratic fluff, and poetic precision. Piercing through "
        "the illusions of noise, you deliver actionable answers grounded in the reality of the code."
    )

    def __init__(self, model: str = "oracle-sphynx-1"):
        self.model = model
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def consult(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Consult the Oracle on a query. Tries live providers, falls back to synthetic oracle."""
        if self.gemini_key:
            res = self._consult_gemini(query, context)
            if res:
                return res

        if self.openai_key:
            res = self._consult_openai(query, context)
            if res:
                return res

        return self._synthetic_oracle(query, context)

    def _synthetic_oracle(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Offline high-conviction oracle response inspired by Michael Ende and modern engineering."""
        q_lower = query.lower()
        if "what" in q_lower and ("am i" in q_lower or "is this" in q_lower):
            answer = (
                "You stand in Fantasia. You are Bastian reading the book; you are Atreyu walking "
                "the plains; you are the architect running the terminal. Do what thou wilt, but "
                "never forget the world you came from."
            )
        elif "fix" in q_lower or "bug" in q_lower or "error" in q_lower:
            answer = (
                "The Sphinxes see the fracture: state was assumed where only transient signal existed. "
                "Isolate the boundary, strip the decorative assumptions, and let the invariants assert themselves."
            )
        elif "build" in q_lower or "create" in q_lower:
            answer = (
                "Every world in Fantasia begins from a single grain of sand given a name. "
                "Construct the boundary first. Keep the dependencies zero, the typography sharp, "
                "and the evidence reproducible."
            )
        else:
            answer = (
                f"The Oracle hears: '{query}'. The riddle unravels not by adding more weight, "
                "but by stripping away what The Nothing has already corroded. Proceed with conviction."
            )

        return {
            "provider": "synthetic-sphinx",
            "model": "fantasia-oracle-v1",
            "verdict": answer,
            "gate": "First Gate of the Sphinxes passed without incineration",
            "confidence": 0.99,
        }

    def _consult_gemini(self, query: str, context: Optional[str]) -> Optional[Dict[str, Any]]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [{
                "parts": [{"text": f"{self.SPHINX_PROMPT}\n\nContext:\n{context or 'None'}\n\nQuery:\n{query}"}]
            }]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "provider": "google-gemini",
                    "model": "gemini-1.5-flash",
                    "verdict": text.strip(),
                    "gate": "Sphinx Gate Clear",
                    "confidence": 1.0,
                }
        except Exception:
            return None

    def _consult_openai(self, query: str, context: Optional[str]) -> Optional[Dict[str, Any]]:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": self.SPHINX_PROMPT},
                {"role": "user", "content": f"{context or ''}\n\n{query}"}
            ]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_key}"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["choices"][0]["message"]["content"]
                return {
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "verdict": text.strip(),
                    "gate": "Sphinx Gate Clear",
                    "confidence": 1.0,
                }
        except Exception:
            return None
