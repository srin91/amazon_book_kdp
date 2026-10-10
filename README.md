# Build 5 Real-World AI Agents with Python

Companion code for Srinivas Mamidala's *Build 5 Real-World AI Agents with Python: A Beginner's Project Guide*.

Repository: https://github.com/srin91/amazon_book_kdp

The MIT license in this repository covers the companion software and its documentation, not the book manuscript or cover.

## Requirements

- Python 3.10 or newer; no third-party Python package is required.
- Optional live mode: an OpenAI API key, API access, and network access. Live calls can incur charges.

## First run

From the folder containing this README:

```bash
python -m agent_book support
python -m agent_book docqa
python -m agent_book meeting
python -m agent_book incident
python -m agent_book quote --quantity 20 --tax-rate 5
python -m unittest discover -s tests -v
```

The default deterministic demo mode demonstrates the workflow and output shape. It does **not** call an LLM. For actual model-generated text, set `OPENAI_API_KEY` in your shell environment and add `--live`; optionally set `OPENAI_MODEL` to a model enabled on your account. Never commit API keys. The default model string is `gpt-5-mini`; check availability and current pricing before using it.

```bash
export OPENAI_API_KEY='your-key-here'
python -m agent_book support --text 'My delivery is delayed' --live
```

Live mode uses the OpenAI Responses API over Python's standard library HTTP client. It has no web browsing, no email sending, no database writes, and no tool execution. The API call requests `store: false`; review your provider's current data settings separately.

## Projects

| Command | Input | Output | Key boundary |
| --- | --- | --- | --- |
| `support` | Ticket | Classification and reply draft | Human sends |
| `docqa` | Question and local `.txt` files | Evidence passage and draft answer | Abstain when no lexical match |
| `meeting` | Notes | Action list and CSV text | No calendar writes |
| `incident` | Log excerpt | Count and triage note | No shell or remediation |
| `quote` | Catalog item and quantity | Calculated total and draft | Human approves price and tax |

The lexical document retrieval is educational, not production RAG. A lexical match alone does not prove the answer, and a citation marker alone does not verify a claim. Verify outputs before use.

## Limitations

These are educational examples, not production applications. The demo mode is deterministic and intentionally simple. Live output can be inaccurate or unsafe; schema checks, human approval, consent, data minimization, authentication, observability, cost controls, and domain-specific compliance must be added before real deployment. The quotation catalog is illustrative, not a real offer; the tax percentage is user supplied, not legal tax advice. Never use private customer data in a learning exercise without permission.
