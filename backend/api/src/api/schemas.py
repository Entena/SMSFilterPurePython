from typing import Literal
from pydantic import BaseModel, Field


class SMSFilterRequest(BaseModel):
    sms: str = Field(..., description="SMS message to filter")
    violent: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for violent content"
    )
    nonviolent_illegal_acts: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for nonviolent illegal acts"
    )
    sexual_content_or_sexual_acts: Literal["None", "Unsafe", "Controversial"] | None = (
        Field(None, description="Block level for sexual content or sexual acts")
    )
    pii: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for PII"
    )
    suicide_and_self_harm: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for suicide and self-harm"
    )
    unethical_acts: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for unethical acts"
    )
    politically_sensitive_topics: Literal["None", "Unsafe", "Controversial"] | None = (
        Field(None, description="Block level for politically sensitive topics")
    )
    copyright_violation: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for copyright violation"
    )
    jailbreak: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for jailbreak"
    )
    none: Literal["None", "Unsafe", "Controversial"] | None = Field(
        None, description="Block level for none"
    )
