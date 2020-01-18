from urllib.parse import urlparse, urlunparse
from azure.core.pipeline.transport import HttpRequest


class UrlBuilder:
    def __init__(self, path: str):
        self._path = path
        self._query = {}

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value

    def append_query(self, key: str, value: str):
        self._query[key] = value
        return self

    def build(self):
        query_params = ["{}={}".format(k, v) for k, v in self._query.items()]
        query = "?" + "&".join(query_params) if query_params else ''
        return urlunparse(('', '', self._path, '', query, ''))


def create_list_models_request(next_link: str = None, op: str = None):
    url = UrlBuilder('/custom/models')
    if next_link:
        url.path = next_link
    if op:
        url.append_query('op', op)
    return HttpRequest("GET", url.build())
