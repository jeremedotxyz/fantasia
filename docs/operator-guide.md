# Operator Guide

Quick reference for running, interacting with, and configuring Fantasia.

---

## 1. Quickstart

Run Fantasia without any dependencies beyond Python 3.10+:

```bash
# Clone the repository
git clone https://github.com/jeremedotxyz/fantasia.git
cd fantasia

# Run the terminal demo
python3 -m fantasia.cli demo
```

Alternatively, install in editable mode:

```bash
pip install -e .
fantasia demo
```

---

## 2. Command Reference

### `fantasia demo`
Renders the full terminal interface showcase with active tabs, AURYN talisman art, Southern Oracle output, and The Nothing radar.

### `fantasia wish "<prompt>"`
Submits a prompt as an AURYN-grounded wish:
```bash
fantasia wish "Audit this codebase for state leaks"
```
The talisman signs the request, decrements memory anchor balance, and queries the Oracle.

### `fantasia oracle "<question>"`
Consults the Sphinxes directly:
```bash
fantasia oracle "What is the cleanest way to decouple this module?"
```

### `fantasia atreyu "<task>"`
Dispatches the autonomous reconnaissance scout:
```bash
fantasia atreyu "Inspect project layout and report findings"
```

### `fantasia nothing [--tokens N]`
Inspects context token usage and entropy radar:
```bash
fantasia nothing --tokens 45000
```

---

## 3. Environment Variables

To connect live generative models, set any of the following standard environment variables:

```bash
export GEMINI_API_KEY="your-gemini-key"      # Routes to Google Gemini
export OPENAI_API_KEY="your-openai-key"      # Routes to OpenAI
export OLLAMA_HOST="http://localhost:11434"  # Routes to local Ollama
```

If no keys are provided, Fantasia automatically uses its built-in **Synthetic Sphinx Oracle**—ensuring zero crashes and complete offline functionality.
