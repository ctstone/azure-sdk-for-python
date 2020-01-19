from .source_filter import SourceFilter


class TrainRequest:
    def __init__(self, source: str, source_filter: SourceFilter = None):
        self.source = source
        self.source_filter = source_filter
