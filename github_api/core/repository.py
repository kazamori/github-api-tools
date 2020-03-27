from collections import Counter

from ..consts import GithubFile, GithubState
from ..utils import calculate_days
from ..utils import log


def get_file_changes(files):
    c = Counter({GithubFile.ADD: 0, GithubFile.DEL: 0, GithubFile.CHG: 0})
    for f in files:
        c[GithubFile.ADD] += f.additions
        c[GithubFile.DEL] += f.deletions
        c[GithubFile.CHG] += f.changes
    log.debug(f' - changes: {c[GithubFile.CHG]}')
    return c


def set_changes(pr):
    pr.changes = pr.additions - pr.deletions
    log.debug(f' - changes: {pr.changes}')


def set_labels(pr):
    pr.labels_ = ','.join(i.name for i in pr.get_labels())
    log.debug(f' - labels: {pr.labels_}')


def set_reviews(pr, user):
    reviews = {i.user.login for i in pr.get_reviews()
               if user.login != i.user.login}
    pr.reviews = ','.join(reviews)
    log.debug(f' - reviews: {pr.reviews}')


def set_elapsed_days(pr):
    pr.elapsed_days = calculate_days(pr.created_at,  pr.closed_at)
    log.debug(f' - elapsed_days: {pr.elapsed_days}')
    log.debug(f' - merged: {pr.merged}')


def set_elapsed_days_of_first_comment(pr, user):
    pr.elapsed_days_of_first_comment = -1
    if pr.comments == 0:
        return

    for comment in pr.get_issue_comments():
        if comment.user.login == user.login:
            elapsed_days = calculate_days(pr.created_at, comment.created_at)
            pr.elapsed_days_of_first_comment = elapsed_days
            log.debug(f' - elapsed_days(1st comment): {elapsed_days}')
            return


def get_pr_info(pulls, user):
    for pr in pulls:
        log.info(f'#{pr.number}: {pr.title}')
        if pr.assignee is None:
            continue

        if user.login == pr.assignee.login:
            log.debug(f' - comments: {pr.comments}')
            set_changes(pr)
            set_labels(pr)
            set_reviews(pr, user)
            set_elapsed_days(pr)
            set_elapsed_days_of_first_comment(pr, user)
            yield pr


def get_repository_info(name, gh):
    state = GithubState.ALL.value
    user = gh.get_user()
    repo = gh.get_repo(name)
    log.info(f'Repository: {repo.name}')
    log.info(f'          : {repo.clone_url}')
    repo.pulls = list(get_pr_info(repo.get_pulls(state=state), user))
    return repo
