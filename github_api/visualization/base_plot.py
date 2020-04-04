import re
from functools import lru_cache

import numpy as np
import pandas as pd

from ..utils import log

_RE_REPOSITORY = re.compile(
    r'https://github\.com/(?P<org>.*?)/(?P<name>.*?)/.*')


class BasePlot:

    MAX_UNIQUE_LABELS = 32

    def _set_changes_bins(self):
        step = self.changes_bins_step
        if step == 1:
            arr = np.array([self.min_changes, self.max_changes + 1])
        else:
            bins = range(self.min_changes, self.max_changes, step)
            arr = np.array(bins)
        indexes = arr.searchsorted(self.df['changes'], side='right') - 1
        self.df['changes_bins'] = [arr[i] for i in indexes]
        log.debug(f"unique bins: {len(pd.unique(self.df['changes_bins']))}")

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

    @property
    @lru_cache(1)
    def unique_labels(self):
        return pd.unique(self.df['labels_'])

    @lru_cache(1)
    def has_labels(self):
        number_of_labels = len(self.unique_labels)
        log.debug(f'unique labels: {number_of_labels}')
        return not (number_of_labels == 1 and pd.isnull(self.unique_labels[0]))

    @lru_cache(1)
    def _can_allocate_labels(self):
        number_of_labels = len(self.unique_labels)
        return number_of_labels < self.MAX_UNIQUE_LABELS

    @lru_cache(1)
    def can_allocate_labels(self):
        return self.has_labels() and self._can_allocate_labels()

    @property
    @lru_cache(1)
    def hue_labels(self):
        if self.can_allocate_labels():
            return 'labels_'
        return None

    @property
    @lru_cache(1)
    def title(self):
        org = name = ''
        row = self.df.iloc[0]
        m = _RE_REPOSITORY.match(row['html_url'])
        if m:
            d = m.groupdict()
            org = d['org']
            name = d['name']
        return f"repo: {org}/{name}, assignee: {row['user.login']}"
