from enum import Enum

PACKAGE_NAME = 'github-api-tools'


class WeekEnd(Enum):
    SATURDAY = 6
    SUNDAY = 7


class GithubAPI(Enum):
    ACTIONS = 'actions'
    ISSUES = 'issues'
    PULLS = 'pulls'


class GithubConclusion(Enum):
    FAILURE = 'failure'
    SUCCESS = 'success'


class GithubFile(Enum):
    ADD = 'additions'
    DEL = 'deletions'
    CHG = 'changes'


class GithubState(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    ALL = 'all'
