# Module: fine_tuning/fine_tuning_models.py
# Description:
# Define models for fine-tuning requests.
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class FineTuningRequest(BaseModel):
    params: dict

