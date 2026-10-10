"""CLI: python -m agent_book {support,docqa,meeting,incident,quote} [--live]."""
import argparse
import json
from pathlib import Path
from . import support, docqa, meetings, incidents, quotes
from .core import ModelError


def main():
    parser = argparse.ArgumentParser(description="Five educational AI agent workflows")
    parser.add_argument("project", choices=["support", "docqa", "meeting", "incident", "quote"])
    parser.add_argument("--live", action="store_true", help="Call the OpenAI Responses API; may incur charges")
    parser.add_argument("--text", help="Ticket, question, notes, or log text; defaults to bundled example")
    parser.add_argument("--customer", default="Example Textile Buyer")
    parser.add_argument("--fabric", default="cotton", choices=list(quotes.CATALOG))
    parser.add_argument("--quantity", type=int, default=20)
    parser.add_argument("--tax-rate", default="0", help="Illustrative percentage; verify tax rules yourself")
    args = parser.parse_args()
    data = Path(__file__).resolve().parent.parent / "data"
    examples = {"support": "I need a refund for order 123.",
                "docqa": "How do I request a refund?",
                "meeting": (data / "meeting.txt").read_text(encoding="utf-8"),
                "incident": (data / "service.log").read_text(encoding="utf-8")}
    text = args.text if args.text is not None else examples.get(args.project, "")
    try:
        result = {"support": lambda: support.run(text, args.live),
                  "docqa": lambda: docqa.run(text, data / "knowledge", args.live),
                  "meeting": lambda: meetings.run(text, args.live),
                  "incident": lambda: incidents.run(text, args.live),
                  "quote": lambda: quotes.run(args.customer, args.fabric, args.quantity, args.tax_rate, args.live)}[args.project]()
    except (ValueError, ModelError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
