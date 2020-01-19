from ..models import (
    Model,
    ModelListing,
    ModelsSummary,
    ModelInfo,
    ModelStatus)


def parse_models_summary(d: dict) -> ModelsSummary:
    if not d:
        return
    count = d.get('count')
    limit = d.get('limit')
    last_updated_date_time = d.get(
        'lastUpdatedDateTime')  # TODO: convert to Datetime
    return ModelsSummary(
        count=count,
        limit=limit,
        last_updated_date_time=last_updated_date_time)


def parse_model_info(d: dict) -> ModelInfo:
    model_id = d.get('modelId')
    status = ModelStatus(d.get('status'))
    created_date_time = d.get('createdDateTime')  # TODO Datetime
    last_updated_date_time = d.get('lastUpdatedDateTime')  # TODO Datetime
    return ModelInfo(
        model_id=model_id,
        status=status,
        created_date_time=created_date_time,
        last_updated_date_time=last_updated_date_time)


def parse_model_listing(d: dict) -> ModelListing:
    summary = parse_models_summary(d.get('summary'))
    model_list = [parse_model_info(x) for x in d.get('modelList')]
    next_link = d.get('nextLink')
    return ModelListing(
        summary=summary,
        model_list=model_list,
        next_link=next_link)


def parse_model(d: dict) -> Model:
    model_info = parse_model_info(d.get('modelInfo'))
    return Model(
        model_info=model_info)
