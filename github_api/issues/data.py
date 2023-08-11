from copy import deepcopy
from operator import attrgetter


def get_comments_data(comments):
    comment_item = {
        'created_at': None,
        'body': None,
        'user.login': None,
    }
    columns = comment_item.keys()
    for comment in comments:
        d = deepcopy(comment_item)
        data = zip(columns, attrgetter(*columns)(comment))
        for column, value in data:
            d[column] = value
        yield d


def create_data(repo):
    issue_item = {
        'body': None,
        'comments': None,
        'comments_': None,
        'created_at': None,
        'html_url': None,
        'labels_': None,
        'number': None,
        'title': None,
        'user.login': None,
    }
    columns = issue_item.keys()
    for issue in repo.issues:
        data = zip(columns, attrgetter(*columns)(issue))
        for column, value in data:
            if column == 'comments_':
                issue_item[column] = list(get_comments_data(value))
            else:
                issue_item[column] = value
        yield issue_item
