
import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "library.json"

ID_PREFIXES = {
    "book": "BK",
    "author": "AU",
    "borrower": "BR",
    "borrowing": "BO",
}


def load_library(filename=DATA_FILE):
    """Load library data, preserving existing records."""
    path = Path(filename)

    with path.open("r", encoding="utf-8") as file:
        library = json.load(file)

    if not isinstance(library, dict):
        raise ValueError("Library data must be a JSON object.")

    for key in ("books", "authors", "borrowers", "borrowings"):
        library.setdefault(key, [])

        if not isinstance(library[key], list):
            raise ValueError(f"Library field '{key}' must be a list.")

    return library


def save_library(library, filename=DATA_FILE):
    """Save library data as readable JSON."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(library, file, indent=4, ensure_ascii=False)


def generate_id(records, record_type):
    """Generate the next sequential ID for a record collection."""
    if record_type not in ID_PREFIXES:
        raise ValueError(f"Unknown record type: {record_type}")

    prefix = ID_PREFIXES[record_type]
    highest_number = 0

    for record in records:
        record_id = record.get("id", "")

        if not isinstance(record_id, str):
            continue

        if record_id.startswith(prefix):
            suffix = record_id[len(prefix):]

            if suffix.isdigit():
                highest_number = max(highest_number, int(suffix))

    return f"{prefix}{highest_number + 1:03d}"
