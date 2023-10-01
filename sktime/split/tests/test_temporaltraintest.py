# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Tests for temporal train test splitter."""

import numpy as np
import pandas as pd
import pytest

from sktime.datatypes._utilities import get_cutoff
from sktime.forecasting.tests._config import TEST_OOS_FHS, VALID_INDEX_FH_COMBINATIONS
from sktime.split import temporal_train_test_split
from sktime.utils._testing.forecasting import _make_fh
from sktime.utils._testing.series import _make_series


def _check_train_test_split_y(fh, split):
    assert len(split) == 2

    train, test = split
    assert isinstance(train, pd.Series)
    assert isinstance(test, pd.Series)
    assert set(train.index).isdisjoint(test.index)
    for test_timepoint in test.index:
        assert np.all(train.index < test_timepoint)
    assert len(test) == len(fh)
    assert len(train) > 0

    cutoff = train.index[-1]
    np.testing.assert_array_equal(test.index, fh.to_absolute(cutoff).to_numpy())


@pytest.mark.parametrize(
    "index_type, fh_type, is_relative", VALID_INDEX_FH_COMBINATIONS
)
@pytest.mark.parametrize("values", TEST_OOS_FHS)
def test_split_by_fh(index_type, fh_type, is_relative, values):
    """Test temporal_train_test_split."""
    if fh_type == "timedelta":
        return None
        # todo: ensure check_estimator works with pytest.skip like below
        # pytest.skip(
        #    "ForecastingHorizon with timedelta values "
        #     "is currently experimental and not supported everywhere"
        # )
    y = _make_series(20, index_type=index_type)
    cutoff = get_cutoff(y.iloc[:10], return_index=True)
    fh = _make_fh(cutoff, values, fh_type, is_relative)
    split = temporal_train_test_split(y, fh=fh)
    _check_train_test_split_y(fh, split)