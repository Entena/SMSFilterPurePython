from typing import Literal
from pydantic import BaseModel


class SMSFilterPrediction(BaseModel):
    blocked: bool | None = None
    pattern: Literal["Safe", "Controversial", "Unsafe"] | None = None
    categories: (
        list[
            Literal[
                "Violent",
                "Non-violent Illegal Acts",
                "Sexual Content or Sexual Acts",
                "PII",
                "Suicide & Self-Harm",
                "Unethical Acts",
                "Politically Sensitive Topics",
                "Copyright Violation",
                "Jailbreak",
                "None",
            ]
        ]
        | None
    ) = None
