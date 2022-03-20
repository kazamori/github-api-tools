from operator import attrgetter


def create_data(repo):
    d = {
        'created_at': [],
        'duration_seconds': [],
        'duration_time': [],
        'html_url': [],
        'id': [],
        'total_billable_seconds': [],
        'total_billable_time': [],
        'total_execution_seconds': [],
        'total_execution_time': [],
        'updated_at': [],
        'workflow_name': [],
        'workflow_path': [],
    }
    columns = d.keys()
    for action in repo.actions:
        data = zip(columns, attrgetter(*columns)(action))
        for column, value in data:
            d[column].append(value)
    return d
