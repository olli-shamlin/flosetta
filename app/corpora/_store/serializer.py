# The data that gets serialized to json and back again includes Python date objects which the standard json.dump(s)
# and json.load(s) don't handle directly. The following code implements a custom encoder and decoder to handle
# date values.  Note that if a datetime value happens to be included, it will get deserialized to a date.  This is
# intentional since the related application only uses Python date value and never datetime values. (Famous last
# words.)

from datetime import date
from datetime import datetime
import json
import re


def _is_iso_datetime(val) -> bool:
    if not isinstance(val, str):
        return False
    iso_8601_datetime_regex = \
        r'[+-]?\d{4}(-[01]\d(-[0-3]\d(T[0-2]\d:[0-5]\d:?([0-5]\d(\.\d+)?)?[+-][0-2]\d:[0-5]\dZ?)?)?)?'
    pattern = re.compile(iso_8601_datetime_regex)
    answer = pattern.match(val) is not None
    return answer


def _custom_decoder(data: dict):
    datetime_items = {k: v for k, v in data.items() if _is_iso_datetime(v)}
    if datetime_items:
        for k, v in datetime_items.items():
            data[k] = datetime.fromisoformat(v).date()
    return data


def json_decoder(json_obj: str):
    return json.loads(json_obj, object_hook=_custom_decoder)


class _CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is date:
            obj = datetime(obj.year, obj.month, obj.day, 0, 0, 0, 0)
        if type(obj) is datetime:
            return obj.isoformat()
        if str(type(obj)) in ['<class \'corpora.Character\'>', '<class \'corpora.Word\'>']:
            return obj.as_dict


def json_encoder(data) -> str:
    return json.dumps(data, indent=3, cls=_CustomEncoder)
