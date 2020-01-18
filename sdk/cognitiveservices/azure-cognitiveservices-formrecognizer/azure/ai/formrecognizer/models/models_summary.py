class ModelsSummary:

    # TODO: use Datetime
    def __init__(self, count: int, limit: int, last_updated_date_time: str):
        self.count = count
        self.limit = limit
        self.last_updated_date_time = last_updated_date_time

    def __repr__(self):
        return '<ModelsSummary Count=%s, Limit=%s, Updated=%s>' % (self.count, self.limit, self.last_updated_date_time)
