
import json
from app.corpora._store.spreadsheet import import_spreadsheet
from app.corpora._store.data_files import character_store_key

if __name__ == '__main__':

    spreadsheet_path = '/Users/david/Documents/pycharm-projects/flosetta/app/data/kana.numbers'
    prod_json = '/Users/david/Documents/pycharm-projects/flosetta/app/data/syllabary.json'
    test_json = '/Users/david/Documents/pycharm-projects/flosetta/tests/data/syllabary.json'
    workbook = import_spreadsheet(spreadsheet_path)

    kana_sheet = workbook.sheets[0]
    notes = workbook.sheets[1].tables[0].rows
    notes_map = {row[0]: row[1] for row in notes}

    out_recs = []
    for table in kana_sheet.tables:
        for row in table.rows:
            next_rec = {
                'category': table.name,
                'romaji': row[0],
                'hiragana': row[1],
                'katakana': row[2],
                'hiragana_note': notes_map[row[1]] if (table.name == 'Basic' and row[0] != 'n/m') else None,
                'katakana_note': notes_map[row[2]] if (table.name == 'Basic' and row[0] != 'n/m') else None,
            }
            # next_rec['key'] = character_store_key(next_rec)
            out_recs.append(next_rec)

    with open(prod_json, 'w') as fh:
        json.dump(out_recs, fh, indent=3)

    # with open(test_json, 'w') as fh:
    #     json.dump(out_recs, fh, indent=3)
    #
    pass
