from github.GithubObject import NotSet

from ..utils import log


class IssuesAttribute:

    def __init__(self, args, gh, repo):
        self.args = args
        self.gh = gh
        self.repo = repo

    def set_issue_comments(self, issue):
        issue.comments_ = list(issue.get_comments())

    def set_labels(self, issue):
        issue.labels_ = list(i.name for i in issue.get_labels())
        log.debug(f' - labels: {issue.labels_}')

    def get_issues(self):
        since = NotSet if self.args.datefrom is None else self.args.datefrom
        for issue in self.repo.get_issues(since=since):
            log.info(f'#{issue.number}: {issue.title} '
                     f'comments ({issue.comments})')
            self.set_issue_comments(issue)
            self.set_labels(issue)
            yield issue
