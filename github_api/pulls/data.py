from operator import attrgetter


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
