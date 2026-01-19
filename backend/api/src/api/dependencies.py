from fastapi import Request, Depends
from transformers import AutoModelForCausalLM, AutoTokenizer
from predictor import SMSFilterPredictor
from settings import get_settings, Settings


def get_request_settings(
    excl: list[str] | None = None,
    incl: list[str] | None = None,
) -> Settings:
    update_data = {
        "EXCL": excl,
        "INCL": incl,
    }
    filtered_updates = {k: v for k, v in update_data.items() if v is not None}
    return get_settings().model_copy(deep=True, update=filtered_updates)


def get_model(request: Request) -> AutoModelForCausalLM:
    return request.app.state.model


def get_tokenizer(request: Request) -> AutoTokenizer:
    return request.app.state.tokenizer


def get_sms_filter_predictor(
    model: AutoModelForCausalLM = Depends(get_model),
    tokenizer: AutoTokenizer = Depends(get_tokenizer),
    request_settings: Settings = Depends(get_request_settings),
) -> SMSFilterPredictor:
    return SMSFilterPredictor(
        model=model,
        tokenizer=tokenizer,
        settings=request_settings,
    )
