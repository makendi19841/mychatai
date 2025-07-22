# MyChatAI

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square" alt="python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/CI-GitHub_Actions-blue?style=flat-square" alt="ci">
</div>

**A lightweight, production‑ready orchestration layer that lets you swap between cloud LLMs (OpenAI, Anthropic, etc.) and local Ollama models with a single line of code.**

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick‑Start](#quick-start)
5. [Configuration](#configuration)
6. [Usage](#usage)

   * CLI
   * Python SDK
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Roadmap](#roadmap)
10. [Contributing](#contributing)
11. [License](#license)

---

## ✨ Features<a id="features"></a>

| Category                   | What you get                                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Unified Client API**     | Inject a different `AbstractModelClient` to switch from OpenAI → Ollama (or any future backend) — no other code changes. |
| **Streaming Support**      | Token‑level streaming out‑of‑the‑box for both providers.                                                                 |
| **Typed Settings**         | Centralised config via *pydantic‑settings*; `.env` loading included.                                                     |
| **Pluggable**              | Strategy pattern makes it trivial to add *AnthropicClient*, *GroqClient*, etc.                                           |
| **100 % Editable Install** | `pip install -e .` for instant hot‑reload during development.                                                            |
| **CI‑Ready**               | Linting (`ruff`), typing (`mypy`), tests (`pytest`), and GitHub Actions template.                                        |
| **Zero Global State**      | No more `openai.api_key = ...` mutations; each client owns its own connection.                                           |

---

## 🏗 Architecture<a id="architecture"></a>

```text
mychatai/
├── clients/
│   ├── base.py          # AbstractModelClient (interface)
│   ├── openai.py        # OpenAIClient
│   └── ollama.py        # OllamaClient
├── prompts.py           # Reads system_prompt.txt, builds user prompts
├── chat_service.py      # High‑level façade / orchestration
├── config.py            # Pydantic‑settings singleton
└── utils/               # Display helpers (e.g. streaming in notebooks)
```

```ascii
                +------------------+
 User → CLI →   | ChatService      |
                +--------+---------+
                         | uses
                         ▼
                +------------------+      +------------------+
                | OpenAIClient     |◀──┐  | OllamaClient     |
                +------------------+   │  +------------------+
                         ▲             │         ▲
                         │             │ uses    │ uses
                +--------+---------+   │  +------+-------+
                | AbstractModelClient |─┘  | HTTP / SDK |
                +--------------------+      +-------------+
```

---

## 🛠 Installation<a id="installation"></a>

```bash
# 1️⃣  Clone
 git clone https://github.com/your‑org/mychatai.git && cd mychatai

# 2️⃣  Create & activate virtual‑env
 python -m venv .venv && source .venv/bin/activate

# 3️⃣  Install
 pip install -e .[dev]
```

---

## 🚀 Quick‑Start<a id="quick-start"></a>

### Provide credentials (choose **one** provider)

```bash
# OpenAI         (cloud)
export OPENAI_API_KEY="sk‑..."

# Ollama (local) (make sure `ollama serve` is running)
export OLLAMA_URL="http://localhost:11434/api/chat"
export MYCHATAI_OLLAMA_MODEL="phi3"
```

### Ask a question from the CLI

```bash
./scripts/ask.py "What is camera calibration?"

# or via entry‑point
ask -p ollama --no-stream "What is camera calibration?"
```

### Use it in Python

```python
from mychatai import ChatService, OpenAIClient
chat = ChatService(OpenAIClient())
print(chat.answer("Give me a dad joke about resistors.", stream=False))
```

Streaming:

```python
from mychatai import ChatService, OllamaClient
from mychatai.utils.display import stream_to_stdout

chat   = ChatService(OllamaClient())
tokens = chat.answer("Explain forward‑propagation in 100 words.", stream=True)
stream_to_stdout(tokens)
```

---

## ⚙️ Configuration<a id="configuration"></a>

All runtime options are exposed via **env‑vars** and strongly‑typed in `config.py`.

| Variable                   | Default                           | Description                        |
| -------------------------- | --------------------------------- | ---------------------------------- |
| `OPENAI_API_KEY`           | —                                 | API key for OpenAI.                |
| `OLLAMA_URL`               | `http://localhost:11434/api/chat` | Ollama REST endpoint.              |
| `MYCHATAI_OLLAMA_MODEL`    | `llma3.2`                         | Default local model.               |
| `MYCHATAI_REQUEST_TIMEOUT` | `60` (seconds)                    | Network timeout for all providers. |

Add them to a local `.env` file for convenience; *pydantic‑settings* will auto‑load it.

---

## 🧪 Testing<a id="testing"></a>

```bash
pytest -q          # unit tests (mocks)
pytest -m live     # live tests (needs real API keys)
ruff check .       # lint
mypy mychatai      # type checks
```

---

## 🩹 Troubleshooting<a id="troubleshooting"></a>

| Symptom                              | Fix                                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------ |
| `ModuleNotFoundError: mychatai`      | Activate the venv and run `pip install -e .` again.                            |
| Shebang errors (`command not found`) | Ensure `scripts/ask.py` starts with `#!/usr/bin/env python` and `chmod +x` it. |
| Pylance red squiggles                | Use **Python ▶ Select Interpreter** and choose the venv.                       |
| Long delay / timeout                 | Increase `request_timeout` in `config.py` or check proxy settings.             |
| “model not found” (Ollama)           | `ollama pull <model>` — e.g., `ollama pull phi3`.                              |

---

## 🗺 Roadmap<a id="roadmap"></a>

* 🔌 **AnthropicClient** – add Claude support.
* ♻️ **Async API** – optional async/await variant of `ChatService`.
* 📝 **Docs Site** – GitHub Pages with rich examples.
* 🐳 **Docker image** – `docker run mychatai` for quick demos.

---

## 🤝 Contributing<a id="contributing"></a>

1. Fork → branch → PR.
2. Run `pre‑commit run --all-files` before pushing.
3. Write tests for new functionality.
4. Ensure CI is green.

We follow the [Conventional Commits](https://www.conventionalcommits.org/) spec and *semantic versioning*.

---

## 📄 License<a id="license"></a>

`mychatai` is released under the **MIT License**.  See [`LICENSE`](LICENSE) for details.
