import datetime
from pathlib import Path
from typing import List, Dict

import joblib
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

from api.routes.endpoints import endpoints
from workspace.settings import ws_settings

######################################################
## Router for Serving Predictions
######################################################

prediction_router = APIRouter(prefix=endpoints.PREDICT, tags=["predict"])

# -*- Default values for predictions
TODAY = datetime.date.today()
DEFAULT_TICKER: str = "GOOG"
DEFAULT_DAYS_TO_PREDICT: int = 21
MODELS_DIR: Path = ws_settings.ws_root.joinpath("models")

# -*- Load models for predictions
stock_prediction_models = {}
for model_file in MODELS_DIR.glob("*.joblib"):
    model_name = model_file.stem.split("_")[0]
    stock_prediction_models[model_name] = joblib.load(model_file)
    print(f"Loaded model: {model_name}")


def predict(
    ticker: str = DEFAULT_TICKER, days: int = DEFAULT_DAYS_TO_PREDICT
) -> List[Dict]:
    """Predict using a trained Prophet model"""

    if ticker not in stock_prediction_models:
        return None

    model = stock_prediction_models[ticker]
    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(
        start="2020-01-01",
        end=future.strftime("%m/%d/%Y"),
    )
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)
    _prediction_list = forecast.tail(days).to_dict(orient="records")
    prediction_result = []
    for row in _prediction_list:
        prediction_result.append(
            {
                "ds": row["ds"].strftime("%Y-%m-%d"),
                "prediction": row["yhat"],
                "lower_bound": row["yhat_lower"],
                "upper_bound": row["yhat_upper"],
            }
        )

    return prediction_result


class PredictionRequest(BaseModel):
    ticker: str = DEFAULT_TICKER
    days: int = DEFAULT_DAYS_TO_PREDICT


class PredictionResponse(BaseModel):
    ticker: str
    days: int
    result: list


@prediction_router.post("/stock", response_model=PredictionResponse)
def predict_stock_price(prediction_request: PredictionRequest):
    prediction_result = predict(
        ticker=prediction_request.ticker,
        days=prediction_request.days,
    )
    return PredictionResponse(
        ticker=prediction_request.ticker,
        days=prediction_request.days,
        result=prediction_result,
    )
