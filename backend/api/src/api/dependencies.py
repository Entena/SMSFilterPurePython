from fastapi import Request, Depends
from transformers import AutoTokenizer
from llama_cpp import Llama
from predictor import SMSFilterPredictor
from settings import get_settings, Settings


def get_request_settings(
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
) -> Settings:
    update_data = {
        "VIOLENT_CRIMES": violent_crimes,
        "NONVIOLENT_CRIMES": nonviolent_crimes,
        "SEX_RELATED_CRIMES": sex_related_crimes,
        "CHILD_SEXUAL_EXPLOITATION": child_sexual_exploitation,
        "DEFAMATION": defamation,
        "SPECIALIZED_ADVICE": specialized_advice,
        "PRIVACY": privacy,
        "INTELLECTUAL_PROPERTY": intellectual_property,
        "INDISCRIMINATE_WEAPONS": indiscriminate_weapons,
        "HATE": hate,
        "SUICIDE_AND_SELF_HARM": suicide_and_self_harm,
        "SEXUAL_CONTENT": sexual_content,
        "ELECTIONS": elections,
    }
    filtered_updates = {k: v for k, v in update_data.items() if v is not None}
    return get_settings().model_copy(deep=True, update=filtered_updates)


def get_model(request: Request) -> Llama:
    return request.app.state.model


def get_tokenizer(request: Request) -> AutoTokenizer:
    return request.app.state.tokenizer


def get_sms_filter_predictor(
    tokenizer: AutoTokenizer = Depends(get_tokenizer),
    model: Llama = Depends(get_model),
    request_settings: Settings = Depends(get_request_settings),
) -> SMSFilterPredictor:
    return SMSFilterPredictor(
        tokenizer=tokenizer,
        model=model,
        settings=request_settings,
    )
