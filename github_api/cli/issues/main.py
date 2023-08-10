import logging
import sys

from github import Github

from ...consts import GithubAPI
from ...core.repository import Repository
from ...issues.data import create_data
from ...utils import log
from ...utils import output_json
from ..common_option import get_common_parser


def parse_argument():
    parser = get_common_parser()
    parser.set_defaults(
        api=GithubAPI.ISSUES,
    )
    argv = sys.argv[1:]
    args = parser.parse_args(argv)
    return args


def main():
    args = parse_argument()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    from ..env import TOKEN

    gh = Github(TOKEN)

    for name in args.repositories:
        with Repository(args, gh, name) as repo:
            repo_name = name.split('/')[-1]
            filename = f'{repo_name}-{args.api.value}.json'
            data = create_data(repo)
            output_json(args, data, filename)


if __name__ == '__main__':
    main()
