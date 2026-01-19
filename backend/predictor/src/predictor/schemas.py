from pydantic import BaseModel


class SMSFilterPrediction(BaseModel):
    prediction: bool
    category: str | None = None
