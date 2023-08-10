from ..consts import GithubAPI
from ..utils import log
from .repository_actions import ActionsAttribute
from .repository_issues import IssuesAttribute
from .repository_pulls import PullsAttribute


class Repository:

    def __init__(self, args, gh, name):
        self.args = args
        self.gh = gh
        self.name = name
        # extra attributes
        self.actions = []
        self.issues = []
        self.pulls = []

    def __enter__(self):
        self.set_extra_attributes(self._get_repo())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _get_repo(self):
        repo = self.gh.get_repo(self.name)
        log.info(f'Repository: {repo.name}')
        log.info(f'          : {repo.html_url}')
        return repo

    def set_api_attributes(self, repo=None):
        if repo is None:
            repo = self._get_repo()
        if self.args.api == GithubAPI.ACTIONS:
            self._actions = ActionsAttribute(self.args, self.gh, repo)
        elif self.args.api == GithubAPI.ISSUES:
            self._issues = IssuesAttribute(self.args, self.gh, repo)
        elif self.args.api == GithubAPI.PULLS:
            self._pulls = PullsAttribute(self.args, self.gh, repo)
        else:
            raise NotImplementedError(f'Unsupported api: {self.args.api}')

    def set_extra_attributes(self, repo):
        self.set_api_attributes(repo)
        if self.args.api == GithubAPI.ACTIONS:
            self.actions = list(self._actions.get_actions())
        elif self.args.api == GithubAPI.ISSUES:
            self.issues = list(self._issues.get_issues())
        elif self.args.api == GithubAPI.PULLS:
            self.pulls = list(self._pulls.get_pulls())
        else:
            raise NotImplementedError(f'Unsupported api: {self.args.api}')
