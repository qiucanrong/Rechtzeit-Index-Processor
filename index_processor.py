from __future__ import annotations
from typing import Iterable, List, Tuple, Optional, Dict

KNOWN_HEADERS: Dict[str, str] = {
    "A": "@@@Record Albums / CDs Index",
    "B": "@@@Books Index",
    "M": "@@@Films Index",
    "O": "@@@Poems Index",
    "P": "@@@Plays Index",
    "R": "@@@Radio Programs Index",
    "S": "@@@Songs Index",
    "T": "@@@Television Programs Index",
}


def _header_for_code(code: str) -> str:
    """
    Known codes use the mapped human header.
    Unknown codes use the rule: '@@@ZZZ[character]'.
    """
    if code in KNOWN_HEADERS:
        return KNOWN_HEADERS[code]
    return f"@@@ZZZ{code}"


def process_lines(lines: Iterable[str]) -> List[str]:
    """
    Apply rules line-by-line.

    - If line doesn't start with 'ZZZ': keep as-is.
    - If line starts with 'ZZZ':
        - Let code be the 4th char (line[3]) if present.
        - On first occurrence of each code, insert a header:
            - Known codes -> mapped header
            - Unknown codes -> '@@@ZZZ{code}'
        - Strip first 4 chars ('ZZZ' + code) and keep the rest.
    Returns a list of lines each ending with '\n'.
    """
    out: List[str] = []
    seen_codes = set()

    for raw in lines:
        line = raw.rstrip("\n")

        if not line.startswith("ZZZ"):
            out.append(line + "\n")
            continue

        code = line[3] if len(line) >= 4 else ""

        # If somehow the line is exactly "ZZZ" with no code, treat code as empty string
        # and header becomes "@@@ZZZ" (rare, but deterministic).
        if code not in seen_codes:
            out.append(_header_for_code(code) + "\n")
            seen_codes.add(code)

        stripped = line[4:] if len(line) >= 4 else ""
        stripped = stripped.lstrip()
        out.append(stripped + "\n")

    return out


def process_text(text: str) -> str:
    return "".join(process_lines(text.splitlines(True)))