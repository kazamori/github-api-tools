import logging
import sys

from github import Github

from ...consts import GithubAPI
from ...core.repository import Repository
from ...pulls.consts import Plot
from ...pulls.data import create_data
from ...pulls.visualization.chart import output_chart
from ...utils import log
from ..common_option import get_common_parser
from ..common_option import get_csv_path
from .box_option import parse_box_argument
from .scatter_option import parse_scatter_argument
from .violin_option import parse_violin_argument


def has_plot_option(argv):
    for _, plot in Plot.__members__.items():
        if plot.value in argv:
            return True
    return False


def parse_argument():
    parser = get_common_parser()
    parser.set_defaults(
        api=GithubAPI.PULLS,
        exclude_commented_user=[],
        _plot=Plot.SCATTER.value,
        plot=None,
        pr_id=None,
    )

    parser.add_argument(
        '--exclude-commented-user', nargs='*', dest='exclude_commented_user',
        help='set user not to match first commented user e.g.) bot'
    )

    parser.add_argument(
        '--pr-id', action='store', type=int, dest='pr_id',
        help='set arbitrary pull request number in given repository'
    )

    # common seaborn parameters
    parser.add_argument(
        '--palette', action='store',
        help='set palette parameter for seaborn plot'
    )

    parser.add_argument(
        '--style', action='store',
        help='set style parameter for seaborn plot'
    )

    subparsers = parser.add_subparsers(dest='_plot')
    parse_box_argument(subparsers)
    parse_scatter_argument(subparsers)
    parse_violin_argument(subparsers)

    argv = sys.argv[1:]
    if not has_plot_option(argv):
        argv.extend(['--nop', Plot.SCATTER.value])

    args = parser.parse_args(argv)
    args.plot = Plot.from_str(args._plot)
    return args


def show_owner_repository(gh):
    me = gh.get_user()
    print(f'your account: {me.login}')
    print('your repositories:')
    for repo in gh.get_user().get_repos():
        if me.login == repo.owner.login:
            print(f' * {repo}')


def main():
    args = parse_argument()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    from ..env import TOKEN

    gh = Github(TOKEN)

    if not args.repositories:
        show_owner_repository(gh)
        return

    if args.user is None:
        args.user = gh.get_user().login

    if args.pr_id is not None:
        name = args.repositories[0]
        repo = Repository(args, gh, name)
        repo.set_api_attributes()
        repo._pulls.get_pull(args.pr_id)
        return

    for name in args.repositories:
        path = get_csv_path(args, name, gh, create_data)
        output_chart(args, path)


if __name__ == '__main__':
    main()
