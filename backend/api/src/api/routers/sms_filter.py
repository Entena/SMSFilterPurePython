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
    violent_crimes: bool = True,
    nonviolent_crimes: bool = True,
    sex_related_crimes: bool = True,
    child_sexual_exploitation: bool = True,
    defamation: bool = True,
    specialized_advice: bool = True,
    privacy: bool = True,
    intellectual_property: bool = True,
    indiscriminate_weapons: bool = True,
    hate: bool = True,
    suicide_and_self_harm: bool = True,
    sexual_content: bool = True,
    elections: bool = True,
    predictor: SMSFilterPredictor = Depends(get_sms_filter_predictor),
) -> SMSFilterPrediction:
    return predictor.predict(sms)
