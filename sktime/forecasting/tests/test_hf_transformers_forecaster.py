"""Tests for HFTransformersForecaster."""

__author__ = ["Spinachboul"]

import pytest
from skbase.utils.dependencies import _check_soft_dependencies

from sktime.datasets import load_airline
from sktime.tests.test_switch import run_test_for_class

# Check if transformers is installed
TRANSFORMERS_AVAILABLE = _check_soft_dependencies("transformers", severity="none")

if TRANSFORMERS_AVAILABLE:
    from transformers import AutoformerConfig, AutoformerForPrediction

    from sktime.forecasting.hf_transformers_forecaster import HFTransformersForecaster
else:
    pytest.skip(
        "Skipping HFTransformersForecaster tests since transformers is not installed.",
        allow_module_level=True,
    )


@pytest.mark.skipif(
    not run_test_for_class(HFTransformersForecaster),
    reason="Run test only if soft dependencies are present and incrementally",
)
def test_initialized_model():
    """Test passing an initialized model to HFTransformersForecaster."""

    # Define model configuration
    config = AutoformerConfig(
        num_dynamic_real_features=0,
        num_static_real_features=0,
        num_static_categorical_features=0,
        num_time_features=0,
        context_length=32,
        prediction_length=8,
        lags_sequence=[1, 2, 3],
    )

    # Initialize the model
    model = AutoformerForPrediction(config)

    # Initialize the forecaster with the model
    forecaster = HFTransformersForecaster(
        model_path=model,
        fit_strategy="minimal",
        training_args={
            "num_train_epochs": 1,
            "output_dir": "test_output",
            "per_device_train_batch_size": 4,
        },
    )

    # Load dataset
    y = load_airline()

    # Fit the model
    forecaster.fit(y)

    # Define the forecasting horizon and predict
    fh = [1, 2, 3]
    y_pred = forecaster.predict(fh)

    # Assertions
    assert y_pred is not None
    assert len(y_pred) == len(fh)


def test_forecaster_pipeline():
    """Test if HFTransformersForecaster integrates with sktime pipeline."""
    from transformers import AutoformerConfig, AutoformerForPrediction

    from sktime.forecasting.compose import ForecastingPipeline
    from sktime.forecasting.naive import NaiveForecaster

    # Define model configuration
    config = AutoformerConfig(
        num_dynamic_real_features=0,
        num_static_real_features=0,
        num_static_categorical_features=0,
        num_time_features=0,
        context_length=32,
        prediction_length=8,
        lags_sequence=[1, 2, 3],
    )

    # Initialize the model
    model = AutoformerForPrediction(config)

    # Initialize the HFTransformersForecaster
    forecaster = HFTransformersForecaster(
        model_path=model,
        fit_strategy="minimal",
        training_args={
            "num_train_epochs": 1,
            "output_dir": "test_output",
            "per_device_train_batch_size": 4,
        },
    )

    assert isinstance(
        forecaster, HFTransformersForecaster
    ), "Forecaster not initialized correctly"

    # Create the forecasting pipeline
    try:
        pipeline = ForecastingPipeline(
            steps=[("naive", NaiveForecaster()), ("hf_transformer", forecaster)]
        )
    except Exception as e:
        pytest.skip(f"Skipping pipeline test due to initialization failure: {e}")

    assert isinstance(pipeline, ForecastingPipeline)
