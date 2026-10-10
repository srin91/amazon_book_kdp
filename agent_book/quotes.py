"""Project 5: deterministic pricing; optional model writes draft wording only."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .core import bounded, live_text

CATALOG = {"cotton": Decimal("220.00"), "linen": Decimal("340.00"), "polyester": Decimal("160.00")}
MIN_QTY = 10


def run(customer: str, fabric: str, quantity: int, tax_rate: str = "0", live: bool = False) -> dict:
    customer = bounded(customer.strip(), 100)
    fabric = fabric.lower().strip()
    if not customer or fabric not in CATALOG or not isinstance(quantity, int) or not MIN_QTY <= quantity <= 100000:
        raise ValueError("Provide a customer, catalog fabric and quantity from 10 to 100000.")
    try:
        rate = Decimal(tax_rate)
    except InvalidOperation as exc:
        raise ValueError("Tax rate must be a decimal percentage.") from exc
    if rate < 0 or rate > 30:
        raise ValueError("Tax rate must be 0 to 30 percent; verify applicable tax independently.")
    subtotal = CATALOG[fabric] * quantity
    tax = (subtotal * rate / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = subtotal + tax
    facts = (f"Customer: {customer}; item: {fabric}; quantity: {quantity}; "
             f"unit price INR {CATALOG[fabric]}; subtotal INR {subtotal}; "
             f"illustrative tax {rate}%; tax INR {tax}; total INR {total}.")
    if live:
        draft = live_text(
            "Draft a concise quotation email from the supplied facts only. The figures are fixed; "
            "do not recalculate, invent availability, delivery promises, terms or discounts. "
            "Say pricing and tax need human approval before sending.", facts)
    else:
        draft = f"Dear {customer}, draft quote: {quantity} units of {fabric} at INR {CATALOG[fabric]} each; illustrative total INR {total}. Pricing and tax require approval before sending."
    return {"customer": customer, "fabric": fabric, "quantity": quantity, "unit_price": str(CATALOG[fabric]),
            "subtotal": str(subtotal), "tax_rate": str(rate), "tax": str(tax), "total": str(total),
            "draft": draft, "status": "REVIEW_REQUIRED"}

