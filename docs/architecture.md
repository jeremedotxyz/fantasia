# Architecture & Technical Design

Fantasia is an interactive, terminal-native AI operator designed around the aesthetics of modern GPU terminals and the symbolic narrative of Michael Ende's *The NeverEnding Story*.

```
                                      ┌─────────────────────────────────┐
                                      │        Human Reader / Operator  │
                                      └────────────────┬────────────────┘
                                                       │ (Wish / Prompt)
                                                       ▼
                                      ┌─────────────────────────────────┐
                                      │      AURYN Token Governor       │
                                      │     "DO WHAT THOU WILT"         │
                                      │   (Grounding & Memory Anchor)   │
                                      └───────┬─────────────────┬───────┘
                                              │                 │
                         ┌────────────────────┘                 └──────────────────┐
                         ▼                                                         ▼
         ┌───────────────────────────────┐                         ┌───────────────────────────────┐
         │     Southern Oracle (AI)      │                         │     The Nothing (Entropy)     │
         │   Sphinx Gate & Reasoning     │                         │   Context Degradation Monitor │
         │   (Gemini/OpenAI/Synthetic)   │                         │     (Token Budget & Pruning)  │
         └───────────────┬───────────────┘                         └───────────────┬───────────────┘
                         │                                                         │
                         ▼                                                         ▼
         ┌───────────────────────────────┐                         ┌───────────────────────────────┐
         │       Terminal Renderer       │◄────────────────────────┤     Atreyu / Falkor Agent     │
         │   24-bit TrueColor Terminal   │                         │  Reconnaissance & Recovery    │
         └───────────────────────────────┘                         └───────────────────────────────┘
```

---

## 1. Zero Runtime Dependencies

Fantasia runs on standard library Python 3.10+ without requiring external wheel installations:
- Terminal TrueColor ANSI escape sequences generated via `fantasia.ui.Color`.
- HTTP telemetry and LLM requests handled through `urllib.request`.
- Cryptographic talisman signatures derived via standard `hashlib`.
- Optional development dependencies (`Pillow`) are strictly isolated to visual asset generation.

---

## 2. Core Subsystems

### `AURYN` (`fantasia.auryn`)
- The talisman acts as the state governor and authorization layer.
- Each human prompt is treated as a **Wish**.
- In the original text, every wish granted in Fantasia costs a human memory. Fantasia models this by maintaining an explicit ledger of human anchors (`memories_preserved`) so that autonomous agents cannot drift into hallucinations or unconstrained state changes.

### `The Southern Oracle` (`fantasia.oracle`)
- Represents the dual Sphinx gate. The Sphinxes see through doubt and illusions.
- Connects to modern generative models (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, local `OLLAMA_HOST`) or operates in offline synthetic mode without crashing or requiring API tokens.

### `The Nothing` (`fantasia.nothing`)
- Monitors token context consumption and entropy drift.
- Categorizes threat levels:
  1. `QUIET` ($\le 30\%$ context used)
  2. `RESTLESS` ($30\% - 60\%$)
  3. `CRITICAL` ($60\% - 92\%$)
  4. `THE VOID` ($> 92\%$)

### `Atreyu & Falkor` (`fantasia.agent`)
- **Atreyu**: The autonomous scout dispatched across repository files.
- **Falkor**: Optimistic recovery logic handling stalled loops and unexpected exceptions.
