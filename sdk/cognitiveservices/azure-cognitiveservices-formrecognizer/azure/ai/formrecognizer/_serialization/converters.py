from json import loads
from azure.core.pipeline.transport import HttpResponse
from .parsers import parse_model_listing, parse_model
from ..models import TrainRequest, SourceFilter


def _get_dict(d: dict):
    return {k: v for k, v in d.items() if v is not None}


def _get_source_filter_dict(source_filter: SourceFilter):
    if not source_filter:
        return None

    return _get_dict({
        'prefix': source_filter.prefix,
        'includeSubFolders': source_filter.include_sub_folders})


def read_model_listing(response: HttpResponse):
    body = loads(response.text())
    return parse_model_listing(body)


def read_model(response: HttpResponse):
    body = loads(response.text())
    return parse_model(body)


def get_train_request_dict(train_request: TrainRequest) -> dict:
    if not train_request:
        return None

    return _get_dict({
        'source': train_request.source,
        'sourceFilter': _get_source_filter_dict(train_request.source_filter)})
