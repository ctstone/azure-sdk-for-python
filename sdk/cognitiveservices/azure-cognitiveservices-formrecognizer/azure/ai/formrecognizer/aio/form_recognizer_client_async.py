from typing import Dict
from azure.core.pipeline import AsyncPipeline
from azure.core.pipeline.policies import HeadersPolicy, ContentDecodePolicy
from azure.core.pipeline.transport import HttpRequest, AioHttpTransport, AioHttpTransportResponse
from .._policies import ApiKeyCredentialPolicy, FormEndpointPolicy
from .._requests import create_list_models_request
from .._serialization.responses import read_model_listing


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
        request = create_list_models_request()
        async with self._pipeline as pipeline:
            response = await pipeline.run(request)
            http_response = response.http_response  # type: AioHttpTransportResponse
            return read_model_listing(http_response)  # TODO: paging
