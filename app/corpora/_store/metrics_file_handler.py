
from datetime import datetime
from datetime import timedelta
from glob import glob
import os
from typing import Optional

from .data_files import DATE_SUBSTITUTION_MARKER
from .data_files import METRICS_RETENTION_LIMIT
from .data_files import VOCABULARY_METRICS_FILE
from .data_files import SYLLABARY_METRICS_FILE
from .serializer import json_encoder
from .serializer import json_decoder


def _today() -> str:
    return datetime.today().strftime('%Y%m%d')


def _days_ago() -> str:
    today = datetime.now()
    n_days_ago = today - timedelta(days=METRICS_RETENTION_LIMIT)
    return n_days_ago.strftime('%Y%m%d')


def _filename_of_today_version(path_pattern: str) -> str:
    return path_pattern.replace(DATE_SUBSTITUTION_MARKER, _today())


def _existing_metrics_filenames(path_pattern: str) -> list[str]:
    """Returns a sorted list of filenames for existing versions of the given Element type's metrics files."""
    filename_pattern = path_pattern.replace(DATE_SUBSTITUTION_MARKER, '*')
    files = glob(filename_pattern)
    if len(files) == 0:
        raise FileNotFoundError(f'store._existing_metrics_filenames(): {filename_pattern}')
    return sorted(files)


def _filename_for_latest_version(path_pattern: str) -> str:
    """Returns the filename of the latest version of the given Element type's metrics files"""
    return _existing_metrics_filenames(path_pattern)[-1]


def _filename_of_oldest_version(path_pattern: str) -> str:
    """Returns the filename of the oldest version of the given Element type's metrics file."""
    return _existing_metrics_filenames(path_pattern)[-1]


def _oldest_version_to_retain(path_pattern: str) -> str:
    """Return the filename of the oldest given Element type's metrics file that should be retained."""
    return path_pattern.replace(DATE_SUBSTITUTION_MARKER, _days_ago())


def _delete_expired_metric_file_versions(path_pattern: str) -> None:
    """Deletes any metric file versions for the given Element type that are more than n days in the past."""

    # Get the list of existing metric file versions for this type of Element and the name of the oldest file
    # version to be retained.
    filenames = _existing_metrics_filenames(path_pattern)
    oldest_version_to_retain = _oldest_version_to_retain(path_pattern)

    # To determine if there are metrics file versions older than the oldest version to retain,
    # we get the index of the oldest version to retain from the list of existing version filenames.
    if oldest_version_to_retain not in filenames:
        # The name of the oldest version to retain may not be in the list of existing versions. That's
        # ok for the purposes of this function; we just add the name of the oldest version to the set of
        # existing version names in the correct sort order position
        filenames.append(oldest_version_to_retain)
        filenames = sorted(filenames)
    oldest_version_idx = filenames.index(oldest_version_to_retain)

    # Deleting "expired" versions is now just a matter of iterating through the slice of all version filenames
    # that are before the oldest version to retain in the list of all file versions.
    files_to_delete = filenames[:oldest_version_idx + 1]
    for next_file_to_delete in files_to_delete:
        # Not all filenames in files_to_delete may actually exist on disk. Note we potentially injected
        # the oldest_version_to_retain to files_to_delete above and it may not exist on disk.
        if os.path.exists(next_file_to_delete):
            os.remove(next_file_to_delete)

    return


def _load_metrics(filename: str) -> Optional[list]:

    # Fully qualify the filename
    if not os.path.exists(filename):
        raise FileNotFoundError(f'cache._load_metrics: file not found: {filename}')

    # A json metrics file did exist, so decode it to a list of dicts
    with open(filename, 'r') as fh:
        records = json_decoder(fh.read())

    return records


def _resolve_filename(corpus_id) -> str:
    corpus_id = corpus_id if type(corpus_id) is str else corpus_id.name
    return VOCABULARY_METRICS_FILE if (corpus_id == 'VOCABULARY') else SYLLABARY_METRICS_FILE


# TODO should return an optional tuple?/list? of Metrics objects
def load_latest_metrics_file(corpus_id) -> Optional[dict]:

    file_type = _resolve_filename(corpus_id)
    try:
        return _load_metrics(_filename_for_latest_version(file_type))
    except FileNotFoundError:
        return None


def save_metrics(corpus_id, metrics: list) -> None:

    file_type = _resolve_filename(corpus_id)

    # Save the given metrics data
    json_obj = json_encoder([m.as_dict for m in metrics])
    filename = _filename_of_today_version(file_type)
    with open(filename, 'w') as fh:
        fh.write(json_obj)

    # Prune the metrics file versions
    _delete_expired_metric_file_versions(file_type)

    return
