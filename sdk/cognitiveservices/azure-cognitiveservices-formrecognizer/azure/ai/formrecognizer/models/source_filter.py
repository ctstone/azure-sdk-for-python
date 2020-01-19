class SourceFilter:
    def __init__(self, prefix: str = None, include_sub_folders: bool = None):
        self.prefix = prefix
        self.include_sub_folders = include_sub_folders
