from ...pulls.consts import Plot


def parse_violin_argument(subparsers):
    parser = subparsers.add_parser(Plot.VIOLIN.value)
    parser.set_defaults(
        height=8,
        inner='quart',
        loc='upper right',
        palette='pastel',
        style='whitegrid',
        width=10,
    )

    parser.add_argument(
        '--height', action='store', type=int,
        help='set height parameter for subplots'
    )

    parser.add_argument(
        '--inner', action='store',
        help='set inner parameter for violinplot'
    )

    parser.add_argument(
        '--loc', action='store',
        help='set loc parameter for legend'
    )

    parser.add_argument(
        '--width', action='store', type=int,
        help='set width parameter for subplots'
    )
