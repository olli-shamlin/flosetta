
import json
import os

from app import app
from .data_files import word_store_key
from .data_files import VOCABULARY_FILE
from .metrics_file_handler import load_latest_metrics_file
from .spreadsheet import import_spreadsheet


def _validate_workbook_record(record: dict) -> None:

    if record[0] is None:
        raise Exception(f'store._validate_workbook_record(): "english" value missing: {record}')
    if record[1] is None:
        raise Exception(f'store._validate_workbook_record(): "romaji" value missing: {record}')
    if record[2] is None:
        raise Exception(f'store._validate_workbook_record(): "kana" value missing: {record}')
    if record[4] is None:
        raise Exception(f'store._validate_workbook_record(): "part of Speech" value missing: {record}')

    return


def _load_workbook() -> list[dict]:

    answer = []

    workbook = import_spreadsheet(VOCABULARY_FILE)

    for sheet in workbook.sheets:
        for table in sheet.tables:
            for row in table.rows:
                _validate_workbook_record(row)
                answer.append({'english': row[0], 'romaji': row[1], 'kana': row[2], 'kanji': row[3],
                               'part_of_speech': row[4], 'note': row[6], 'tags': row[5]})

    return answer


def _load_word_records() -> list[dict]:

    if app.config['TEST_MODE']:

        if not os.path.exists(VOCABULARY_FILE):
            raise FileNotFoundError(VOCABULARY_FILE)
        with open(VOCABULARY_FILE, 'r') as fh:
            records = json.load(fh)

    else:

        records = _load_workbook()

    return records


def load_vocabulary() -> list[tuple[dict]]:

    words: list = []

    word_records = _load_word_records()

    # Read any existing metrics
    metrics_records = load_latest_metrics_file('VOCABULARY')
    if metrics_records:
        metrics = {m['key']: m for m in metrics_records}

    # Convert word records to Word objects merging in existing metrics data
    for next_word_record in word_records:
        store_key = word_store_key(next_word_record)
        next_metrics_record = metrics[store_key] if (metrics_records and store_key in metrics.keys()) else None
        words.append((next_word_record, next_metrics_record))

    return words

