from typing import Dict, Awaitable, Tuple, AsyncIterator
from azure.core.async_paging import AsyncPageIterator
from azure.core.pipeline import AsyncPipeline
from azure.core.pipeline.policies import HeadersPolicy, ContentDecodePolicy
from azure.core.pipeline.transport import HttpRequest, AioHttpTransport, AioHttpTransportResponse
from .._policies import ApiKeyCredentialPolicy, FormEndpointPolicy
from .._requests import create_list_models_request, create_get_model_request
from .._serialization.converters import read_model_listing, read_model
from ..models import Model, ModelInfo


class FormRecognizerClientAsync:
    def __init__(self, endpoint: str, api_key: str, version='v2.0-preview', custom_headers: Dict[str, str] = {}, **kwargs):
        transport = AioHttpTransport(**kwargs)
        headers_policy = HeadersPolicy(custom_headers, **kwargs)
        policies = [
            ApiKeyCredentialPolicy(api_key),
            FormEndpointPolicy(endpoint, version),
            headers_policy,
        ]
        self._pipeline = AsyncPipeline(transport, policies=policies)

    async def list_models(self, next_link: str = None):
        async def get_next(continuation_token: str) -> Awaitable[AioHttpTransportResponse]:
            request = create_list_models_request(next_link=next_link)
            async with self._pipeline as pipeline:
                response = await pipeline.run(request)
                return response.http_response

        async def extract_data(response: AioHttpTransportResponse) -> Awaitable[Tuple[str, AsyncIterator[ModelInfo]]]:
            return read_model_listing(response)

        return AsyncPageIterator[ModelInfo](
            get_next=get_next,
            extract_data=extract_data,
            continuation_token=next_link)

    async def get_model(self, model_id: str) -> Model:
        request = create_get_model_request(model_id)
        async with self._pipeline as pipeline:
            response = await pipeline.run(request)
            http_response = response.http_response  # type: AioHttpTransportResponse
            return read_model(http_response)  # TODO: paging
