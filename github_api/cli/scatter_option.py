from ..consts import Plot


def parse_scatter_argument(subparsers):
    parser = subparsers.add_parser(Plot.SCATTER.value)
    parser.set_defaults(
        alpha=.7,
        col='labels_',
        col_wrap=2,
    )

    parser.add_argument(
        '--alpha', action='store', type=float,
        help='set alpha parameter for relplot'
    )

    parser.add_argument(
        '--col', action='store',
        help='set col parameter for relplot'
    )

    parser.add_argument(
        '--col_wrap', action='store', type=int,
        help='set col_wrap parameter for relplot'
    )
