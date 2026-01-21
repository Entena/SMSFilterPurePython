from fastapi import Request, Depends
from transformers import AutoTokenizer, AutoModelForCausalLM
from predictor import SMSFilterPredictor
from settings import get_settings, Settings
from .schemas import SMSFilterRequest


def get_request_settings(request: SMSFilterRequest) -> Settings:
    update_data = {
        "VIOLENT": request.violent,
        "NON_VIOLENT_ILLEGAL_ACTS": request.nonviolent_illegal_acts,
        "SEXUAL_CONTENT_OR_SEXUAL_ACTS": request.sexual_content_or_sexual_acts,
        "PII": request.pii,
        "SUICIDE_AND_SELF_HARM": request.suicide_and_self_harm,
        "UNETHICAL_ACTS": request.unethical_acts,
        "POLITICALLY_SENSITIVE_TOPICS": request.politically_sensitive_topics,
        "COPYRIGHT_VIOLATION": request.copyright_violation,
        "JAILBREAK": request.jailbreak,
        "NONE": request.none,
    }
    filtered_updates = {k: v for k, v in update_data.items() if v is not None}
    return get_settings().model_copy(deep=True, update=filtered_updates)


def get_model(request: Request) -> AutoModelForCausalLM:
    return request.app.state.model


def get_tokenizer(request: Request) -> AutoTokenizer:
    return request.app.state.tokenizer


def get_sms_filter_predictor(
    tokenizer: AutoTokenizer = Depends(get_tokenizer),
    model: AutoModelForCausalLM = Depends(get_model),
    request_settings: Settings = Depends(get_request_settings),
) -> SMSFilterPredictor:
    return SMSFilterPredictor(
        tokenizer=tokenizer,
        model=model,
        settings=request_settings,
    )
