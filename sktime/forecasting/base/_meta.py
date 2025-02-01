#!/usr/bin/env python3 -u
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Implements meta forecaster for forecasters composed of other estimators."""

__author__ = ["mloning"]
__all__ = ["_HeterogenousEnsembleForecaster"]

from sktime.base import _HeterogenousMetaEstimator
from sktime.forecasting.base._base import BaseForecaster
from sktime.utils.parallel import parallelize


class _HeterogenousEnsembleForecaster(_HeterogenousMetaEstimator, BaseForecaster):
    """Base class for heterogeneous ensemble forecasters."""

    # for default get_params/set_params from _HeterogenousMetaEstimator
    # *steps*attr points to the attribute of self
    # which contains the heterogeneous set of estimators
    # this must be an iterable of (name: str, estimator, ...) tuples for the default
    _steps_attr = "forecasters"

    # if the estimator is fittable, _HeterogenousMetaEstimator also
    # provides an override for get_fitted_params for params from the fitted estimators
    # the fitted estimators should be in a different attribute, *steps*fitted_attr
    # this must be an iterable of (name: str, estimator, ...) tuples for the default
    _steps_fitted_attr = "forecasters_"

<<<<<<< HEAD
    def __init__(self, forecasters, backend="loky", backend_params=None):
=======
    def __init__(self, forecasters, backend="loky", backend_params=None, n_jobs=None):
>>>>>>> b509423c6 (refactor code files)
        self.forecasters = forecasters
        self.forecasters_ = None
        self.n_jobs = None
        self.backend = backend
<<<<<<< HEAD
<<<<<<< HEAD
        self.backend_params = backend_params
=======
        self.backend_params = backend_params if backend_params is not None else {}
=======
        self.backend_params = backend_params if backend_params != {} else {}
>>>>>>> c1c361f9d (fix import issues)
        self.n_jobs = n_jobs  # Retained for backward compatibility
>>>>>>> b509423c6 (refactor code files)
        super().__init__()

    def _check_forecasters(self):
        if (
            self.forecasters is None
            or len(self.forecasters) == 0
            or not isinstance(self.forecasters, list)
        ):
            raise ValueError(
                "Invalid 'estimators' attribute, 'estimators' should be a list"
                " of (string, estimator) tuples."
            )

        names, forecasters = zip(*self.forecasters)
        # defined by MetaEstimatorMixin
        self._check_names(names)

        has_estimator = any(est not in (None, "drop") for est in forecasters)
        if not has_estimator:
            raise ValueError(
                "All estimators are dropped. At least one is required "
                "to be an estimator."
            )

        for forecaster in forecasters:
            if forecaster not in (None, "drop") and not isinstance(
                forecaster, BaseForecaster
            ):
                raise ValueError(
                    f"The estimator {forecaster.__class__.__name__} should be a "
                    f"Forecaster."
                )

        return names, forecasters

    def _fit_forecasters(self, forecasters, y, X, fh):
        """Fit all forecasters using parallel processing."""

<<<<<<< HEAD
<<<<<<< HEAD
        def _fit_single_forecaster(forecaster, meta):
            """Fit single forecaster with meta containing y, X, fh."""
            return forecaster.clone().fit(y, X, fh)
=======
        def _fit_forecaster(forecaster, y, X, fh):
=======
        def _fit_forecaster(forecaster, y, X, fh, meta=None):
>>>>>>> c1c361f9d (fix import issues)
            """Fit single forecaster."""
            return forecaster.fit(y, X, fh)

        if self.n_jobs is not None:
            import warnings

            warnings.warn(
                "`n_jobs` is deprecated and will be removed in a future release. "
                "Please use `backend` and `backend_params` instead.",
                FutureWarning,
            )
>>>>>>> b509423c6 (refactor code files)

        self.forecasters_ = parallelize(
<<<<<<< HEAD
            fun=_fit_single_forecaster,
            iter=forecasters,
=======
            fun=_fit_forecaster,
            iter=[forecaster.clone() for forecaster in forecasters],
            meta=None,
>>>>>>> c1c361f9d (fix import issues)
            backend=self.backend,
            backend_params=self.backend_params,
<<<<<<< HEAD
        )
=======
        )(y, X, fh)
>>>>>>> b509423c6 (refactor code files)

    def _predict_forecasters(self, y=None, fh=None, X=None):
        """Collect results from forecaster.predict() calls."""

        def _predict_single_forecaster(forecaster, meta):
            """Predict with single forecaster."""
            return forecaster.predict(fh=fh, X=X)

        return parallelize(
            fun=_predict_single_forecaster,
            iter=self.forecasters_,
            backend=self.backend,
            backend_params=self.backend_params,
        )

    def _update(self, y, X=None, update_params=True):
        """Update fitted parameters.

        Parameters
        ----------
        y : pd.Series
        X : pd.DataFrame
        update_params : bool, optional, default=True

        Returns
        -------
        self : an instance of self.
        """
        for forecaster in self.forecasters_:
            forecaster.update(y, X, update_params=update_params)
        return self
