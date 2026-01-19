from transformers import AutoModelForCausalLM, AutoTokenizer
from settings import Settings, DefaultCategories
from .schemas import SMSFilterPrediction


class SMSFilterPredictor:
    def __init__(
        self, model: AutoModelForCausalLM, tokenizer: AutoTokenizer, settings: Settings
    ):
        self.settings = settings
        self.model = model
        self.tokenizer = tokenizer
        self.default_categories = {
            f"S{i + 1}": cat for i, cat in enumerate(list(DefaultCategories))
        }
        self.additional_categories = {
            f"S{i + len(self.default_categories) + 1}": c
            for i, c in enumerate(settings.INCL)
        }
        self.categories = {
            **self.default_categories,
            **self.additional_categories,
        }

    def predict(self, sms: str) -> SMSFilterPrediction:
        conversation = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": sms,
                    }
                ],
            }
        ]
        input_ids = self.tokenizer.apply_chat_template(
            conversation,
            return_tensors="pt",
        ).to(self.model.device)
        prompt_len = input_ids.shape[1]
        output_ids = self.model.generate(input_ids, pad_token_id=0)
        generated_token_ids = output_ids[:, prompt_len:]
        result = (
            self.tokenizer.decode(
                generated_token_ids[0],
                ignore_special_tokens=True,
            )
            .strip()
            .strip("<|eot_id|>")
        )
        if "unsafe" in result:
            cat = self.categories[result.split("unsafe")[1].strip()]
            return SMSFilterPrediction(
                prediction=False,
                category=cat,
            )
        else:
            return SMSFilterPrediction(
                prediction=True,
                category=None,
            )
