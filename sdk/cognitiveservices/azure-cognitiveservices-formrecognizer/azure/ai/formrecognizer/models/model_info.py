from enum import Enum


class ModelStatus(Enum):
    CREATING = 'creating'
    READY = 'ready'
    INVALID = 'invalid'


class ModelInfo:
    # TODO: use Datetime
    def __init__(self, model_id: str, status: ModelStatus, created_date_time: str, last_updated_date_time: str):
        self.model_id = model_id
        self.status = status
        self.created_date_time = created_date_time
        self.last_updated_date_time = last_updated_date_time
