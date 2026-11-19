# Lore & Technical Specifications

> *"Fantasia has no boundaries. It has no boundaries because it is made of human hopes and dreams."*  
> — The NeverEnding Story

---

## The Symbolic Mapping

| Mythological Concept | Technical System in Fantasia CLI | Implementation Responsibility |
| :--- | :--- | :--- |
| **AURYN** | State governor & Token authenticator | Binds the human operator's intent (`DO WHAT THOU WILT`). Ensures grounding memory is never erased. |
| **The Southern Oracle** | Multi-provider LLM Inference Gate | Direct reasoning bridge (Google Gemini, OpenAI, Anthropic, or Synthetic Sphinx). Pierces ambiguity. |
| **The Nothing** | Context window degradation & token decay | Tracks token budget, alerts operator before hallucination thresholds, and visualizes entropy. |
| **Atreyu** | Autonomous Scout Agent | Traverses the filesystem, analyzes project structure, and creates bounded task reports. |
| **Falkor the Luckdragon** | Optimistic recovery & retry loop | Intercepts runtime errors and provides self-healing escapes. |
| **The Childlike Empress** | Core system prompt & root coordinator | The single grain of sand from which the environment can be restored. |
| **The Ivory Tower** | Session workbench & memory ledger | Holds working tabs, telemetry cards, and persistent state. |

---

## Visual Design Specification (Ghostty Aesthetic)

Fantasia adopts the visual ergonomics of **Ghostty**, the GPU-accelerated terminal emulator created by Mitchell Hashimoto:

- **Palette**: Deep Obsidian `#0c0e14`, Auryn Gold `#daaf37`, Sphinx Teal `#48c9b0`, and Void Magenta `#e056fd`.
- **Framing**: Smooth Unicode box drawings (`╭─╮`, `╰─╯`), macOS traffic light controls, and padded card margins.
- **Tabs**: Crisp status tabs at the top of the session representing the realms of Fantasia.
- **Zero Flickering**: Minimalist redraw passes suitable for high-refresh-rate terminal emulators.
