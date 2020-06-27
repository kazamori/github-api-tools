from ..consts import GithubState
from ..utils import between_datetime
from ..utils import calculate_days
from ..utils import get_first_comment
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
        pr.reviews = list(pr.get_reviews())
        pr.reviews_length = len(pr.reviews)
        log.debug(f' - reviews_length: {pr.reviews_length}')
        reviewers = {i.user.login for i in pr.reviews
                     if self.args.user != i.user.login}
        pr.reviewers = ','.join(reviewers)
        log.debug(f' - reviewers: {pr.reviewers}')

    def set_elapsed_days(self, pr):
        if pr.closed_at is None:
            pr.elapsed_days = -1.0
            return
        pr.elapsed_days = calculate_days(pr.created_at,  pr.closed_at)
        log.debug(f' - created_at: {pr.created_at}')
        log.debug(f' - elapsed_days: {pr.elapsed_days}')
        log.debug(f' - merged: {pr.merged}')

    def set_elapsed_days_of_first_comment(self, pr):
        pr.elapsed_days_of_first_comment = -1
        if pr.comments == 0 and \
           pr.review_comments == 0 and \
           pr.reviews_length == 0:
            return

        comments = []
        if pr.comments != 0:
            issue_comments = pr.get_issue_comments()
            _first = get_first_comment(
                issue_comments, self.args.user,
                self.args.exclude_commented_user)
            if _first is not None:
                comments.append(_first)
        if pr.review_comments != 0:
            review_comments = pr.get_review_comments()
            _first = get_first_comment(
                review_comments, self.args.user,
                self.args.exclude_commented_user)
            if _first is not None:
                comments.append(_first)
        if pr.reviews_length != 0:
            _first = get_first_comment(
                pr.reviews, self.args.user,
                self.args.exclude_commented_user)
            if _first is not None:
                comments.append(_first)

        if len(comments) == 0:
            return

        comments.sort(key=lambda x: x.created_at)
        first_comment = comments[0]
        log.debug(f' - first_comment: {first_comment}')
        log.debug(f'                  created_at: {first_comment.created_at}')

        elapsed = calculate_days(pr.created_at, first_comment.created_at)
        pr.elapsed_days_of_first_comment = elapsed
        log.debug(f' - elapsed_days(1st comment): {elapsed}')
        return

    def get_pull(self, id_):
        # for debugging use
        repo = self.gh.get_repo(self.name)
        log.info(f'Repository: {repo.name}')
        log.info(f'          : {repo.html_url}')
        pr = repo.get_pull(id_)
        log.info(f'#{pr.number}: {pr.title}')
        log.info(f' - comments: {pr.comments}')
        log.info(f' - review_comments: {pr.review_comments}')
        self.set_changes(pr)
        self.set_labels(pr)
        self.set_reviews(pr)
        self.set_elapsed_days(pr)
        self.set_elapsed_days_of_first_comment(pr)

    def get_pulls(self):
        repo = self.gh.get_repo(self.name)
        log.info(f'Repository: {repo.name}')
        log.info(f'          : {repo.html_url}')
        for pr in repo.get_pulls(state=GithubState.ALL.value):
            if not between_datetime(pr.created_at,
                                    self.args.datefrom, self.args.dateto):
                log.debug(f'not between dates: {pr.created_at}')
                continue

            log.info(f'#{pr.number}: {pr.title}')
            assignee = pr.user.login
            if pr.assignee is not None:
                assignee = pr.assignee.login

            log.info(f'#{pr.number}: {pr.title}')
            if self.args.user == assignee:
                log.debug(f' - comments: {pr.comments}')
                log.debug(f' - review_comments: {pr.review_comments}')
                self.set_changes(pr)
                self.set_labels(pr)
                self.set_reviews(pr)
                self.set_elapsed_days(pr)
                self.set_elapsed_days_of_first_comment(pr)
                yield pr

    def set_extra_attributes(self):
        self.pulls = list(self.get_pulls())
