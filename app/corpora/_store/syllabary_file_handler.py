
import os
import json

from .data_files import character_store_key
from .data_files import SYLLABARY_FILE
from .metrics_file_handler import load_latest_metrics_file


def load_syllabary() -> list[tuple[dict]]:

    metrics_records = load_latest_metrics_file('SYLLABARY')
    if metrics_records:
        metrics_records = {m['key']: m for m in metrics_records}

    # Read the syllabary file
    if not os.path.exists(SYLLABARY_FILE):
        raise FileNotFoundError(SYLLABARY_FILE)
    with open(SYLLABARY_FILE, 'r') as fh:
        characters = json.load(fh)

    results: list = []
    for next_character in characters:
        store_key = character_store_key(next_character)
        next_metrics = metrics_records[store_key] if (metrics_records and store_key in metrics_records.keys()) else None
        results.append((next_character, next_metrics))

    return results

