from typing import List
from .model_info import ModelInfo
from .models_summary import ModelsSummary


class ModelListing:
    def __init__(self, summary: ModelsSummary = None, model_list: List[ModelInfo] = None, next_link: str = None):
        self.summary = summary
        self.model_list = model_list
        self.next_link = next_link
