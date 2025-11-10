thonimport logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)

_whitespace_re = re.compile(r"\s+")

def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters and trim."""
    if text is None:
        return ""
    normalized = _whitespace_re.sub(" ", text).strip()
    logger.debug("Normalized text: %r -> %r", text, normalized)
    return normalized

def _strip_currency_symbols(value: str) -> str:
    return re.sub(r"[^\d,.\-]", "", value)

def parse_price(value: str) -> Optional[float]:
    """Parse a localized price string into a float."""
    if not value:
        return None

    raw = _strip_currency_symbols(value)
    if not raw:
        return None

    # Handle European number formats (e.g. 1.234,56)
    # If both comma and dot present, assume comma is decimal separator
    if "," in raw and "." in raw:
        # Remove thousands separators, set decimal to dot
        if raw.rfind(",") > raw.rfind("."):
            raw = raw.replace(".", "").replace(",", ".")
    elif "," in raw and "." not in raw:
        # Single comma -> treat as decimal separator
        raw = raw.replace(",", ".")

    try:
        price = float(raw)
        logger.debug("Parsed price %r -> %s", value, price)
        return price
    except ValueError:
        logger.warning("Failed to parse price from %r", value)
        return None

def parse_float(value: str) -> Optional[float]:
    if value is None:
        return None
    value = value.strip().replace(",", ".")
    try:
        return float(value)
    except ValueError:
        logger.debug("Failed to parse float from %r", value)
        return None

def parse_int(value: str) -> Optional[int]:
    if value is None:
        return None
    cleaned = re.sub(r"[^\d\-]", "", value)
    if not cleaned:
        return None
    try:
        return int(cleaned)
    except ValueError:
        logger.debug("Failed to parse int from %r", value)
        return None

def safe_get(d: dict, *keys: Any, default: Any = None) -> Any:
    """Safely access nested dictionaries."""
    current: Any = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current