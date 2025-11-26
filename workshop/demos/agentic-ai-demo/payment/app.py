import os
import hmac
import base64
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Tuple, Optional, Dict, Any

from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}
PAYMENT_SECRET = os.environ.get("PAYMENT_SECRET", "dev-secret-please-change").encode("utf-8")

# -------- Helpers: time, IDs, validation --------
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def brand_from_number(number: str) -> str:
    n = re.sub(r"\D", "", number)
    if n.startswith("4"):
        return "Visa"
    if re.match(r"^5[1-5]", n):
        return "Mastercard"
    if n.startswith(("34", "37")):
        return "American Express"
    if n.startswith("6"):
        return "Discover"
    return "Unknown"

def sanitize_card(number: str) -> str:
    n = re.sub(r"\D", "", number)
    return n[-4:] if len(n) >= 4 else "0000"

def luhn_ok(number: str) -> bool:
    digits = [int(d) for d in re.sub(r"\D", "", number)]
    if len(digits) < 12 or len(digits) > 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def expiry_valid(exp_month: int, exp_year: int) -> bool:
    if not (1 <= exp_month <= 12):
        return False
    # Normalize two-digit years (e.g., 30 => 2030)
    if exp_year < 100:
        exp_year += 2000
    now = datetime.now()
    if exp_year < now.year:
        return False
    if exp_year == now.year and exp_month < now.month:
        return False
    return True

def payload_hash(obj: Any) -> str:
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def deterministic_id(prefix: str, *parts: str) -> str:
    msg = "|".join(parts).encode("utf-8")
    digest = hmac.new(PAYMENT_SECRET, msg, hashlib.sha256).hexdigest()
    return f"{prefix}_{digest[:24]}"

# -------- Helpers: signing (stateless tokens) --------
def b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")

def b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def sign_payload(payload: Dict[str, Any]) -> str:
    # Canonical JSON string
    s = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig = hmac.new(PAYMENT_SECRET, s, hashlib.sha256).digest()
    return f"{b64url_encode(s)}.{b64url_encode(sig)}"

def verify_token(token: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None, "invalid_token_format"
        s_enc, sig_enc = parts
        s = b64url_decode(s_enc)
        sig = b64url_decode(sig_enc)
        expect = hmac.new(PAYMENT_SECRET, s, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expect):
            return None, "invalid_signature"
        payload = json.loads(s.decode("utf-8"))
        return payload, None
    except Exception:
        return None, "token_parse_error"

# -------- Risk simulation --------
def risk_check(card_number_digits: str, amount: int) -> Tuple[bool, Optional[str]]:
    """
    Simulate a few outcomes:
    - Decline amounts > 100000 minor units (e.g., > $1000.00).
    - Special full PANs simulate specific declines.
    """
    test_declines = {
        "4000000000000002": "generic_decline",
        "4000000000009995": "insufficient_funds",
        "4000000000009979": "suspected_fraud",
    }
    if card_number_digits in test_declines:
        return False, test_declines[card_number_digits]
    if amount > 100000:
        return False, "risk_high_amount"
    return True, None

# -------- Error helper --------
def error(status: int, code: str, message: str, details: Dict[str, Any] = None):
    body = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return jsonify(body), status

# -------- Routes --------
@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok", "time": now_iso()})

@app.post("/charges")
def create_charge():
    """
    Stateless charge creation: card data provided inline and never stored.
    Returns a signed charge_token you can later use to request refunds.
    Request:
    {
      "amount": 1299,
      "currency": "USD",
      "payment_method": {
        "number": "4242424242424242",
        "exp_month": 12,
        "exp_year": 2030,
        "cvc": "123"
      },
      "idempotency_key": "optional-but-recommended",
      "metadata": { ... }
    }
    """
    data = request.get_json(silent=True) or {}
    amount = data.get("amount")
    currency = str(data.get("currency", "")).upper()
    pm = data.get("payment_method") or {}
    idempotency_key = data.get("idempotency_key")
    metadata = data.get("metadata") or {}

    # Validate numeric and currency inputs
    if not isinstance(amount, int) or amount <= 0:
        return error(422, "invalid_amount", "Amount must be a positive integer in minor units.")
    if currency not in SUPPORTED_CURRENCIES:
        return error(422, "unsupported_currency", f"Currency must be one of {sorted(SUPPORTED_CURRENCIES)}.")

    # Validate card details
    number = str(pm.get("number", "")).strip()
    exp_month = int(pm.get("exp_month", 0))
    exp_year = int(pm.get("exp_year", 0))
    cvc = str(pm.get("cvc", "")).strip()

    if not number or not luhn_ok(number):
        return error(422, "invalid_card", "Card number failed validation.")
    if not expiry_valid(exp_month, exp_year):
        return error(422, "invalid_expiry", "Card expiry is invalid or in the past.")
    if not re.fullmatch(r"\d{3,4}", cvc or ""):
        return error(422, "invalid_cvc", "CVC must be 3 or 4 digits.")

    digits_only = re.sub(r"\D", "", number)
    brand = brand_from_number(number)
    last4 = sanitize_card(number)

    # Risk simulation
    approved, reason = risk_check(digits_only, amount)

    # Idempotent-ish charge ID: deterministic when idempotency_key is supplied
    canonical = {
        "amount": amount,
        "currency": currency,
        "brand": brand,
        "last4": last4,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "metadata": metadata,
    }
    phash = payload_hash(canonical)
    if idempotency_key and isinstance(idempotency_key, str) and len(idempotency_key) >= 6:
        charge_id = deterministic_id("ch", "charge", idempotency_key, phash)
    else:
        # Fallback: random-ish ID when idempotency not provided or too short
        charge_id = deterministic_id("ch", "charge", phash, now_iso())

    charge_body = {
        "id": charge_id,
        "type": "charge",
        "version": 1,
        "status": "approved" if approved else "declined",
        "reason": reason,
        "amount": amount,
        "currency": currency,
        "brand": brand,
        "last4": last4,
        "refundable_remaining": amount if approved else 0,
        "metadata": metadata,
        "idempotency_key": idempotency_key,
        "created_at": now_iso(),
    }

    # Never include PAN or CVC in the token or logs
    charge_token = sign_payload(charge_body)

    response = {
        "id": charge_body["id"],
        "status": charge_body["status"],
        "reason": charge_body["reason"],
        "amount": amount,
        "currency": currency,
        "brand": brand,
        "last4": last4,
        "refundable_remaining": charge_body["refundable_remaining"],
        "metadata": metadata,
        "idempotency_key": idempotency_key,
        "created_at": charge_body["created_at"],
        "charge_token": charge_token,
    }
    return jsonify(response), 201

@app.post("/credits")
def create_credit():
    """
    Stateless refund against a prior approved charge.
    You must supply the signed charge_token returned by /charges.
    The server validates and returns a new updated charge_token with reduced refundable_remaining.
    Request:
    {
      "charge_token": "...",
      "amount": 500,
      "idempotency_key": "optional-but-recommended"
    }
    """
    data = request.get_json(silent=True) or {}
    charge_token = data.get("charge_token")
    amount = data.get("amount")
    idempotency_key = data.get("idempotency_key")

    if not isinstance(charge_token, str) or not charge_token:
        return error(422, "invalid_charge_token", "Provide a valid charge_token.")
    if not isinstance(amount, int) or amount <= 0:
        return error(422, "invalid_amount", "Amount must be a positive integer in minor units.")

    payload, verr = verify_token(charge_token)
    if verr:
        return error(422, "invalid_charge_token", f"Charge token verification failed: {verr}.")
    if not payload or payload.get("type") != "charge" or payload.get("version") != 1:
        return error(422, "invalid_charge_token", "Charge token is malformed or unsupported.")
    if payload.get("status") != "approved":
        return error(422, "charge_not_refundable", "Only approved charges can be refunded.")

    refundable = int(payload.get("refundable_remaining", 0))
    if amount > refundable:
        return error(422, "amount_exceeds_refundable",
                     f"Requested refund {amount} exceeds refundable amount {refundable}.")

    # Deterministic credit ID for idempotency-style behavior
    base_parts = [
        "credit",
        str(payload.get("id")),
        str(amount),
        payload.get("currency"),
    ]
    if idempotency_key and isinstance(idempotency_key, str) and len(idempotency_key) >= 6:
        base_parts.append(idempotency_key)
    credit_id = deterministic_id("cr", *base_parts)

    # Build credit record (stateless)
    credit_body = {
        "id": credit_id,
        "type": "credit",
        "version": 1,
        "status": "succeeded",
        "amount": amount,
        "currency": payload.get("currency"),
        "charge_id": payload.get("id"),
        "created_at": now_iso(),
    }
    credit_token = sign_payload(credit_body)

    # Update refundable remaining in the charge and re-issue a fresh token
    new_refundable = refundable - amount
    updated_charge = dict(payload)
    updated_charge["refundable_remaining"] = new_refundable
    updated_charge["updated_at"] = now_iso()
    updated_charge_token = sign_payload(updated_charge)

    response = {
        "id": credit_body["id"],
        "status": credit_body["status"],
        "amount": credit_body["amount"],
        "currency": credit_body["currency"],
        "charge_id": credit_body["charge_id"],
        "created_at": credit_body["created_at"],
        "credit_token": credit_token,
        "refundable_remaining": new_refundable,
        "updated_charge_token": updated_charge_token
    }
    return jsonify(response), 201

@app.post("/verify/charge")
def verify_charge_token():
    """
    Verify and decode a charge_token. Useful for clients to inspect state without storage.
    Request: { "charge_token": "..." }
    """
    data = request.get_json(silent=True) or {}
    token = data.get("charge_token")
    if not token:
        return error(422, "invalid_charge_token", "Provide charge_token.")
    payload, verr = verify_token(token)
    if verr:
        return error(422, "invalid_charge_token", f"Verification failed: {verr}.")
    return jsonify(payload), 200

@app.post("/verify/credit")
def verify_credit_token():
    """
    Verify and decode a credit_token.
    Request: { "credit_token": "..." }
    """
    data = request.get_json(silent=True) or {}
    token = data.get("credit_token")
    if not token:
        return error(422, "invalid_credit_token", "Provide credit_token.")
    payload, verr = verify_token(token)
    if verr:
        return error(422, "invalid_credit_token", f"Verification failed: {verr}.")
    return jsonify(payload), 200

# -------- Main --------
if __name__ == "__main__":
    # Avoid using real card data. Debug logging may print request bodies.
    app.run(host="0.0.0.0", port=5000, debug=True)