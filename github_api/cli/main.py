import argparse
import logging
from pathlib import Path

from github import Github

from ..core.repository import Repository
from ..core.writer import create_filename
from ..core.writer import output_csv
from ..utils import log
from ..visualization.chart import output_chart


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        enable_cache=True,
        repositories=[],
        style='whitegrid',
        verbose=False,
    )

    parser.add_argument(
        '--disable-cache', action='store_false', dest='enable_cache',
        help='disable cache'
    )

    parser.add_argument(
        '--repository', nargs='*', dest='repositories',
        help='set repositories'
    )

    parser.add_argument(
        '--style', action='store',
        help='set figure style for seaborn'
    )

    parser.add_argument(
        '--verbose', action='store_true',
        help='set verbose mode'
    )

    args = parser.parse_args()
    return args


def show_owner_repository(gh):
    me = gh.get_user()
    print(f'your account: {me.login}')
    print('your repositories:')
    for repo in gh.get_user().get_repos():
        if me.login == repo.owner.login:
            print(f' * {repo}')


def get_csv_path(args, repo_name, gh):
    filename = create_filename(repo_name)
    path = Path(filename)
    if args.enable_cache and path.exists():
        log.info(f'use existent {path}')
        return path

    with Repository(gh, repo_name) as repo:
        return output_csv(args, repo, filename)


def main():
    args = parse_argument()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    from .env import TOKEN

    gh = Github(TOKEN)

    if args.repositories is None:
        show_owner_repository(gh)
        return

    for name in args.repositories:
        path = get_csv_path(args, name, gh)
        output_chart(args, path)


if __name__ == '__main__':
    main()
