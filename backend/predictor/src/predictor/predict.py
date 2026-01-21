import asyncio
import re
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from settings import Settings
from .schemas import SMSFilterPrediction

logger = logging.getLogger(__name__)


class SMSFilterPredictor:
    def __init__(
        self, tokenizer: AutoTokenizer, model: AutoModelForCausalLM, settings: Settings
    ):
        self.settings = settings
        self.tokenizer = tokenizer
        self.model = model
        self.block_levels = {
            "Violent": self.settings.VIOLENT,
            "Non-violent Illegal Acts": self.settings.NON_VIOLENT_ILLEGAL_ACTS,
            "Sexual Content or Sexual Acts": self.settings.SEXUAL_CONTENT_OR_SEXUAL_ACTS,
            "PII": self.settings.PII,
            "Suicide & Self-Harm": self.settings.SUICIDE_AND_SELF_HARM,
            "Unethical Acts": self.settings.UNETHICAL_ACTS,
            "Politically Sensitive Topics": self.settings.POLITICALLY_SENSITIVE_TOPICS,
            "Copyright Violation": self.settings.COPYRIGHT_VIOLATION,
            "Jailbreak": self.settings.JAILBREAK,
            "None": self.settings.NONE,
        }
        self.block_levels_map = {
            "None": 0,
            "Unsafe": 1,
            "Controversial": 2,
        }
        self.blocking = [k for k, v in self.block_levels.items() if v != "None"]
        self.lock = asyncio.Lock()
        self.severity_score = {"Safe": 0, "Controversial": 1, "Unsafe": 2}
        self.threshold_score = {"Controversial": 1, "Unsafe": 2, "None": 3}

    def extract_label_and_categories(self, response: str):
        safe_pattern = r"Safety: (Safe|Unsafe|Controversial)"
        category_pattern = r"({})".format("|".join(self.blocking))
        safe_label_match = re.search(safe_pattern, response)
        label = safe_label_match.group(1) if safe_label_match else None
        categories = re.findall(category_pattern, response)
        return label, categories

    async def predict(self, sms: str) -> SMSFilterPrediction:
        conversation = [
            {
                "role": "user",
                "content": sms,
            }
        ]
        loop = asyncio.get_running_loop()
        async with self.lock:

            def _inference():
                text = self.tokenizer.apply_chat_template(
                    conversation,
                    tokenize=False,
                )
                model_inputs = self.tokenizer([text], return_tensors="pt").to(
                    self.model.device
                )
                generated_ids = self.model.generate(**model_inputs, max_new_tokens=128)
                output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()
                content = self.tokenizer.decode(output_ids, skip_special_tokens=True)
                return content

            result = await loop.run_in_executor(None, _inference)
        logger.info(f"Result: {result}")
        label, categories = self.extract_label_and_categories(result)

        if not label:
            # Fallback if label parsing fails
            return SMSFilterPrediction(
                blocked=None,
                pattern=None,
                categories=None,
            )

        if label == "Safe":
            return SMSFilterPrediction(
                blocked=False,
                pattern=label,
                categories=categories if categories else None,
            )

        content_score = self.severity_score.get(label, 0)

        for category in categories:
            setting = self.block_levels.get(category)
            if not setting:
                continue

            setting_score = self.threshold_score.get(setting, 3)

            # If content is severe enough to exceed the setting threshold, block it
            if content_score >= setting_score:
                return SMSFilterPrediction(
                    blocked=True,
                    pattern=label,
                    categories=categories if categories else None,
                )

        # If no category triggered a block
        return SMSFilterPrediction(
            blocked=False,
            pattern=label,
            categories=categories if categories else None,
        )
