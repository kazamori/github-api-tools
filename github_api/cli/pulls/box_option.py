from ...pulls.consts import Plot


def parse_box_argument(subparsers):
    parser = subparsers.add_parser(Plot.BOX.value)
    parser.set_defaults(
        height=8,
        palette='pastel',
        style='ticks',
        width=10,
    )

    parser.add_argument(
        '--height', action='store', type=int,
        help='set height parameter for subplots'
    )

    parser.add_argument(
        '--width', action='store', type=int,
        help='set width parameter for subplots'
    )
