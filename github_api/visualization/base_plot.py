from functools import lru_cache

import numpy as np

from ..utils import log


class BasePlot:

    def _set_changes_bins(self):
        step = self.changes_bins_step
        if step == 1:
            arr = np.array([self.min_changes, self.max_changes + 1])
        else:
            bins = range(self.min_changes, self.max_changes, step)
            arr = np.array(bins)
        indexes = arr.searchsorted(self.df['changes'], side='right') - 1
        self.df['changes_bins'] = [arr[i] for i in indexes]
        log.debug(f"changes_bins:\n{self.df['changes_bins']}")

    @property
    @lru_cache(1)
    def changes_delta(self):
        return self.max_changes - self.min_changes

    @property
    @lru_cache(1)
    def changes_bins_num(self):
        # TODO: consider later
        if self.changes_delta < 100:
            return 8
        elif self.changes_delta < 2000:
            return 16
        elif self.changes_delta < 5000:
            return 32
        else:
            return 64

    @property
    @lru_cache(1)
    def changes_bins_step(self):
        step = int(self.changes_delta / self.changes_bins_num)
        if step == 0:
            return 1
        return step

    @property
    @lru_cache(1)
    def min_changes(self):
        return self.df['changes'].min()

    @property
    @lru_cache(1)
    def max_changes(self):
        return self.df['changes'].max()

    @property
    @lru_cache(1)
    def changes_sizes(self):
        sizes = [(i, (i * 0.1) + 40) for i in self.df['changes_bins']]
        log.debug(f'changes_sizes: {sizes}')
        return dict(sizes)
