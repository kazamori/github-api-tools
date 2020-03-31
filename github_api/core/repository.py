from ..consts import GithubState
from ..utils import calculate_days
from ..utils import log


class Repository:

    def __init__(self, gh, name):
        self.gh = gh
        self.name = name
        self.pulls = []

    def __enter__(self):
        self.set_extra_attributes()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def set_changes(self, pr):
        pr.changes = pr.additions - pr.deletions
        log.debug(f' - changes: {pr.changes}')

    def set_labels(self, pr):
        pr.labels_ = ','.join(i.name for i in pr.get_labels())
        log.debug(f' - labels: {pr.labels_}')

    def set_reviews(self, pr, user):
        reviews = {i.user.login for i in pr.get_reviews()
                   if user.login != i.user.login}
        pr.reviews = ','.join(reviews)
        log.debug(f' - reviews: {pr.reviews}')

    def set_elapsed_days(self, pr):
        pr.elapsed_days = calculate_days(pr.created_at,  pr.closed_at)
        log.debug(f' - elapsed_days: {pr.elapsed_days}')
        log.debug(f' - merged: {pr.merged}')

    def set_elapsed_days_of_first_comment(self, pr, user):
        pr.elapsed_days_of_first_comment = -1
        if pr.comments == 0:
            return

        for comment in pr.get_issue_comments():
            if comment.user.login == user.login:
                elapsed = calculate_days(pr.created_at, comment.created_at)
                pr.elapsed_days_of_first_comment = elapsed
                log.debug(f' - elapsed_days(1st comment): {elapsed}')
                return

    def get_pulls(self):
        user = self.gh.get_user()
        repo = self.gh.get_repo(self.name)
        log.info(f'Repository: {repo.name}')
        log.info(f'          : {repo.html_url}')
        for pr in repo.get_pulls(state=GithubState.ALL.value):
            log.info(f'#{pr.number}: {pr.title}')
            if pr.assignee is None:
                continue

            if user.login == pr.assignee.login:
                log.debug(f' - comments: {pr.comments}')
                self.set_changes(pr)
                self.set_labels(pr)
                self.set_reviews(pr, user)
                self.set_elapsed_days(pr)
                self.set_elapsed_days_of_first_comment(pr, user)
                yield pr

    def set_extra_attributes(self):
        self.pulls = list(self.get_pulls())
