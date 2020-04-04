from ..consts import GithubState
from ..utils import calculate_days
from ..utils import log


class Repository:

    def __init__(self, args, gh, name):
        self.args = args
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

    def set_reviews(self, pr):
        reviews = {i.user.login for i in pr.get_reviews()
                   if self.args.user != i.user.login}
        pr.reviews = ','.join(reviews)
        log.debug(f' - reviews: {pr.reviews}')

    def set_elapsed_days(self, pr):
        if pr.closed_at is None:
            pr.elapsed_days = -1.0
            return
        pr.elapsed_days = calculate_days(pr.created_at,  pr.closed_at)
        log.debug(f' - elapsed_days: {pr.elapsed_days}')
        log.debug(f' - merged: {pr.merged}')

    def set_elapsed_days_of_first_comment(self, pr):
        pr.elapsed_days_of_first_comment = -1
        if pr.comments == 0:
            return

        for comment in pr.get_issue_comments():
            if comment.user.login == self.args.user:
                elapsed = calculate_days(pr.created_at, comment.created_at)
                pr.elapsed_days_of_first_comment = elapsed
                log.debug(f' - elapsed_days(1st comment): {elapsed}')
                return

    def get_pulls(self):
        repo = self.gh.get_repo(self.name)
        log.info(f'Repository: {repo.name}')
        log.info(f'          : {repo.html_url}')
        for pr in repo.get_pulls(state=GithubState.ALL.value):
            log.info(f'#{pr.number}: {pr.title}')
            assignee = pr.assignee
            if assignee is None:
                assignee = pr.user.login

            if self.args.user == assignee:
                log.debug(f' - comments: {pr.comments}')
                self.set_changes(pr)
                self.set_labels(pr)
                self.set_reviews(pr)
                self.set_elapsed_days(pr)
                self.set_elapsed_days_of_first_comment(pr)
                yield pr

    def set_extra_attributes(self):
        self.pulls = list(self.get_pulls())
