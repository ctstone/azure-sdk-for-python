from json import loads
from azure.core.pipeline.transport import HttpResponse
from .parsers import parse_model_listing


def read_model_listing(response: HttpResponse):
    body = loads(response.text())
    return parse_model_listing(body)
