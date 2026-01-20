from transformers import AutoTokenizer
from llama_cpp import Llama
from settings import Settings
from .schemas import SMSFilterPrediction


class SMSFilterPredictor:
    def __init__(self, tokenizer: AutoTokenizer, model: Llama, settings: Settings):
        self.settings = settings
        self.tokenizer = tokenizer
        self.model = model
        self.categories = {
            f"S{i + 1}": cat
            for i, cat in enumerate(
                [
                    "VIOLENT_CRIMES",
                    "NONVIOLENT_CRIMES",
                    "SEX_RELATED_CRIMES",
                    "CHILD_SEXUAL_EXPLOITATION",
                    "DEFAMATION",
                    "SPECIALIZED_ADVICE",
                    "PRIVACY",
                    "INTELLECTUAL_PROPERTY",
                    "INDISCRIMINATE_WEAPONS",
                    "HATE",
                    "SUICIDE_AND_SELF_HARM",
                    "SEXUAL_CONTENT",
                    "ELECTIONS",
                ]
            )
        }
        self.exclude = [
            k for k, v in self.categories.items() if not getattr(self.settings, v)
        ]

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
        prompt = self.tokenizer.apply_chat_template(
            conversation,
            excluded_category_keys=self.exclude,
            tokenize=False,
            add_generation_prompt=True,
        )
        completion = self.model(
            prompt,
            max_tokens=1024,
            stop=["<|eot_id|>"],
            echo=False,
        )
        result = completion["choices"][0]["text"].strip()
        if "unsafe" in result:
            try:
                cat_key = result.split("unsafe")[1].strip()
                cat = self.categories.get(cat_key, "Unknown")
            except IndexError:
                cat = "Unknown"

            return SMSFilterPrediction(
                prediction=False,
                category=cat,
            )
        else:
            return SMSFilterPrediction(
                prediction=True,
                category=None,
            )
