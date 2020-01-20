from typing import Dict, Awaitable, Tuple, AsyncIterator, TypeVar
from azure.core.async_paging import AsyncPageIterator
from azure.core.pipeline import AsyncPipeline
from azure.core.pipeline.policies import HeadersPolicy, ContentDecodePolicy
from azure.core.pipeline.transport import HttpRequest, AioHttpTransport, AioHttpTransportResponse
from .._policies import ApiKeyCredentialPolicy, FormEndpointPolicy
from .._requests import create_list_models_request, create_get_model_request, create_train_request
from .._serialization.converters import read_model_listing, read_model
from ..models import Model, ModelInfo

ReturnType = TypeVar("ReturnType")


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

    async def __aenter__(self) -> "FormRecognizerClientAsync":
        await self._pipeline.__aenter__()
        return self

    async def __aexit__(self, *exc_details):  # pylint: disable=arguments-differ
        await self._pipeline.__aexit__(*exc_details)

    def list_models(self, continuation_token: str = None) -> AsyncIterator[AsyncIterator[ReturnType]]:
        async def get_next(continuation_token: str) -> Awaitable[AioHttpTransportResponse]:
            request = create_list_models_request(next_link=continuation_token)
            async with self._pipeline as pipeline:
                response = await pipeline.run(request)
                return response.http_response

        async def extract_data(response: AioHttpTransportResponse) -> Awaitable[Tuple[str, AsyncIterator[ModelInfo]]]:
            listing = read_model_listing(response)
            continuation_token = listing.next_link if listing.next_link else None
            return continuation_token, listing.model_list

        return AsyncPageIterator[ModelInfo](
            get_next=get_next,
            extract_data=extract_data,
            continuation_token=continuation_token)

    async def begin_train(self, source: str, prefix: str = None, include_sub_folders: bool = None, polling_interval: int = 10):
        # Delayed import to avoid circular import
        from .._polling import get_train_operation_id
        request = create_train_request(
            source=source,
            prefix=prefix,
            include_sub_folders=include_sub_folders)
        # async with self._pipeline as pipeline:
        response = await self._pipeline.run(request)
        http_response = response.http_response  # type: AioHttpTransportResponse
        operation_id = get_train_operation_id(http_response)
        self._pipeline.__aenter__
        return self.get_train_operation(operation_id, polling_interval)

    def get_train_operation(self, operation_id: str, polling_interval: int = 10):
        # Delayed import to avoid circular import
        from .._polling import AsyncTrainModelOperation, AsyncTrainPollingMethod
        polling_method = AsyncTrainPollingMethod(
            operation_id, polling_interval)
        return AsyncTrainModelOperation(
            client=self,
            polling_method=polling_method,
            operation_id=operation_id)

    async def get_model(self, model_id: str) -> Model:
        request = create_get_model_request(model_id)
        print("GET MODEL REQUEST %s" % request)
        # async with self._pipeline as pipeline:
        response = await self._pipeline.run(request)
        print('GOT RESPONSE %s' % response)
        http_response = response.http_response  # type: AioHttpTransportResponse
        return read_model(http_response)  # TODO: paging
