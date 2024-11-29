
import datetime
import glob
import json
import pytest
import os


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            obj = datetime.datetime(obj.year, obj.month, obj.day, 0, 0, 0, 0)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


def _day_as_date(shift: int = 0) -> datetime.date:
    n_days_ago = datetime.datetime.now() - datetime.timedelta(shift)
    return n_days_ago.date()


def _day_as_str(shift: int = 0) -> str:
    return _day_as_date(shift).strftime('%Y%m%d')


def _cwd() -> str:
    """Returns the current directory."""
    return os.getcwd()


def _save_to_json_file(data, filename: str):

    json_obj = json.dumps(data, indent=3, cls=DateTimeEncoder)
    qualified_filename = f'{_cwd()}/data/{filename}.json'
    with open(qualified_filename, 'w') as fh:
        fh.write(json_obj)

    return


def _delete_all_test_json_files() -> None:
    files = glob.glob(f'{_cwd()}/data/*.json')
    for file in files:
        os.remove(file)
    return


@pytest.fixture
def create_test_data():

    _delete_all_test_json_files()
    num_elements = 100

    # ------------------------------------------------------------------------------------
    # Generate and save syllabary test data
    # ------------------------------------------------------------------------------------
    elements = []
    for i in range(1, num_elements + 1):
        elements.append({
            'romaji': f'romaji {i}',
            'hiragana': f'hiragana {i}',
            'katakana': f'katakana {i}',
            'category': f'category {"12345678"[(i - 1) % 8]}',           # category values repeat every eight(8) words
            'hiragana_note': f'hiragana note {i}' if (i % 3) else None,  # every 3rd element's hiragana note is None
            'katakana_note': f'katakana note {i}' if (i % 5) else None,  # every 5th element's katakana note is None
        })

    _save_to_json_file(elements, 'syllabary')

    # ------------------------------------------------------------------------------------
    # Generate and save syllabary metrics test data. More specifically,
    #   - generate metrics for the first 10 characters
    #   - generate 8 file versions starting with today
    # ------------------------------------------------------------------------------------
    keys = [e['romaji'].replace(' ', '') for e in elements][:10]
    for version_no in range(1, 9):  # range(1, 9) results in 8 history files starting yesterday
        values = [{'key': key, 'quizzed_count': 1, 'correct_count': 1, 'last_quizzed': _day_as_date(version_no),
                   'consecutive_correct': 1, 'consecutive_incorrect': 0}
                  for key in keys]
        _save_to_json_file(values, f'syllabary_metrics_{_day_as_str(version_no)}')

    # ------------------------------------------------------------------------------------
    # Generate and save vocabulary test data
    # ------------------------------------------------------------------------------------
    elements = []
    for i in range(1, num_elements + 1):
        tags_val = '; '.join([f'tag {j}' for j in range(1, (i % 4) + 1)]) if (i % 4) else None
        elements.append({
            'english': f'english {i}',
            'romaji': f'romaji {i}',
            'kana': f'kana {i}',
            'kanji': f'kanji {i}' if (i % 10 == 0) else None,  # every 10th word has a kanji value
            'part_of_speech': f'pos {(i % 10) + 1}',           # part of speech values repeat ever 10 words
            'note': f'note {i}' if (i % 15 == 0) else None,    # every 15th word has a note
            'tags': tags_val,
        })

    _save_to_json_file(elements, 'vocabulary')

    # ------------------------------------------------------------------------------------
    # Generate and save vocabulary metrics test data. More specifically,
    #   - generate metrics for the first 10 characters
    #   - generate 8 file versions starting with today
    # ------------------------------------------------------------------------------------
    keys = [e['english'].replace(' ', '') + e['romaji'].replace(' ', '') for e in elements][:10]

    for version_no in range(1, 9):  # range(1, 9) results in 8 history files starting yesterday
        values = [{'key': key, 'quizzed_count': 1, 'correct_count': 1, 'last_quizzed': _day_as_date(version_no),
                   'consecutive_correct': 1, 'consecutive_incorrect': 0}
                  for key in keys]
        _save_to_json_file(values, f'vocabulary_metrics_{_day_as_str(version_no)}')

    return


@pytest.fixture
def expected_syllabary_data():

    answer: list[dict] = []
    num_elements = 100

    for i in range(1, num_elements + 1):
        answer.append({
            'romaji': f'romaji {i}',
            'hiragana': f'hiragana {i}',
            'katakana': f'katakana {i}',
            'category': f'category {"12345678"[(i - 1) % 8]}',           # category values repeat every eight(8) words
            'hiragana_note': f'hiragana note {i}' if (i % 3) else None,  # every 3rd element's hiragana note is None
            'katakana_note': f'katakana note {i}' if (i % 5) else None,  # every 5th element's katakana note is None
            'metrics': None
        })

    for idx in range(10):  # The first 10 elements have metrics
        answer[idx]['metrics'] = {'key': answer[idx]['romaji'].replace(' ', ''),
                                  'quizzed_count': 1, 'correct_count': 1,
                                  'last_quizzed': _day_as_date(1),
                                  'consecutive_correct': 1,
                                  'consecutive_incorrect': 0}

    return answer


@pytest.fixture
def expected_vocabulary_data():

    answer: list[dict] = []
    num_elements = 100

    for i in range(1, num_elements + 1):
        tags_val = tuple([f'tag {j}' for j in range(1, (i % 4) + 1)]) if (i % 4) else None
        answer.append({
            'english': f'english {i}',
            'romaji': f'romaji {i}',
            'kana': f'kana {i}',
            'kanji': f'kanji {i}' if (i % 10 == 0) else None,  # every 10th word has a kanji value
            'part_of_speech': f'pos {(i % 10) + 1}',           # part of speech values repeat ever 10 words
            'note': f'note {i}' if (i % 15 == 0) else None,    # every 15th word has a note
            'tags': tags_val,
        })

    for idx in range(10):  # The first 10 elements have metrics
        answer[idx]['metrics'] = {'key': answer[idx]['english'].replace(' ', '') +
                                         answer[idx]['romaji'].replace(' ', ''),
                                  'quizzed_count': 1, 'correct_count': 1,
                                  'last_quizzed': _day_as_date(1),
                                  'consecutive_correct': 1,
                                  'consecutive_incorrect': 0}

    return answer
