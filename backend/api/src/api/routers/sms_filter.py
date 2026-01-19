from fastapi import APIRouter, Depends
from predictor import SMSFilterPredictor, SMSFilterPrediction
from ..dependencies import (
    get_sms_filter_predictor,
)

router = APIRouter()


@router.post(
    "/filter/sms",
    summary="Filter SMS",
    response_model=SMSFilterPrediction,
)
async def filter_sms(
    sms: str,
    excl: list[str] | None = None,
    incl: list[str] | None = None,
    predictor: SMSFilterPredictor = Depends(get_sms_filter_predictor),
) -> SMSFilterPrediction:
    return predictor.predict(sms)
