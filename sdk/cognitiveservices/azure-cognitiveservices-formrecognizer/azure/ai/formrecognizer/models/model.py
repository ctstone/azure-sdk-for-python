from .model_info import ModelInfo


class Model:
    def __init__(self, model_info: ModelInfo):
        self.model_info = model_info

    def __repr__(self):
        return '<Model status(%s), id(%s) at %s>' % (self.model_info.status.value, self.model_info.model_id, hex(id(self)))
