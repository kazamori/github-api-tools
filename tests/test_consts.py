import pytest

from github_api.consts import Plot


@pytest.mark.parametrize('s,expected', [
    ('scatter', Plot.SCATTER),
    ('box', Plot.BOX),
    ('violin', Plot.VIOLIN),
])
def test_plot_from_str(s, expected):
    assert Plot.from_str(s) == expected


def test_plot_from_str_exception():
    with pytest.raises(NotImplementedError, match='Unsupported plot:'):
        Plot.from_str('unknown')


@pytest.mark.parametrize('plot,expected', [
    (Plot.SCATTER, 'github_api.visualization.scatter_plot'),
    (Plot.BOX, 'github_api.visualization.box_plot'),
    (Plot.VIOLIN, 'github_api.visualization.violin_plot'),
])
def test_plot_module(plot, expected):
    assert plot.module.__name__ == expected
