import logging
import sys

from github import Github

from ...actions.data import create_data
from ...consts import GithubAPI
from ...core.repository import Repository
from ...utils import log
from ..common_option import get_common_parser
from ..common_option import get_csv_path


def parse_argument():
    parser = get_common_parser()
    parser.set_defaults(
        api=GithubAPI.ACTIONS,
        show_workflows=False,
        workflow_path=None,
    )

    parser.add_argument(
        '--show-enable-workflows', action='store_true', dest='show_workflows',
        help='show enable workflows'
    )

    parser.add_argument(
        '--workflow-path', action='store', dest='workflow_path',
        help='filter any workflow path'
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

    if args.show_workflows:
        for name in args.repositories:
            repo = Repository(args, gh, name)
            repo.set_api_attributes()
            repo._actions.get_workflows()
        return

    for name in args.repositories:
        get_csv_path(args, name, gh, create_data)


if __name__ == '__main__':
    main()
