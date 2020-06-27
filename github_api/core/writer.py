from operator import attrgetter
from pathlib import Path

import pandas as pd

from ..utils import log


def create_filename(name):
    return name.split('/')[-1] + '.csv'


def create_data(repo):
    d = {
        'additions': [],
        'changed_files': [],
        'changes': [],
        'closed_at': [],
        'comments': [],
        'review_comments': [],
        'reviews_length': [],
        'created_at': [],
        'deletions': [],
        'elapsed_days': [],
        'elapsed_days_of_first_comment': [],
        'html_url': [],
        'labels_': [],
        'merged': [],
        'number': [],
        'reviewers': [],
        'title': [],
        'user.login': [],
    }
    columns = d.keys()
    for pr in repo.pulls:
        data = zip(columns, attrgetter(*columns)(pr))
        for column, value in data:
            d[column].append(value)
    return d


def output_csv(args, repo, filename):
    data = create_data(repo)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, columns=data.keys())
    path = Path(filename)
    log.info(f'wrote data into {path}')
    return path
