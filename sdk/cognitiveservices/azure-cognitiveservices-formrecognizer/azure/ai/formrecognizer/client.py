# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

from typing import Dict, Tuple, Iterable
from azure.core.paging import PageIterator
from azure.core.pipeline import Pipeline
from azure.core.pipeline.policies import HeadersPolicy, ContentDecodePolicy
from azure.core.pipeline.transport import RequestsTransport, RequestsTransportResponse
from ._policies import (
    ApiKeyCredentialPolicy,
    FormEndpointPolicy,
)
from ._requests import (
    create_list_models_request,
    create_get_model_request,
    create_train_request,
)
from ._serialization.converters import (
    read_model_listing,
    read_model,
)
from .models import ModelInfo


class FormRecognizerClient:
    def __init__(self, endpoint: str, api_key: str, version='v2.0-preview', custom_headers: Dict[str, str] = {}, **kwargs):
        transport = kwargs.get(
            'transport', RequestsTransport(**kwargs))
        headers_policy = kwargs.get(
            'headers_policy', HeadersPolicy(custom_headers, **kwargs))
        policies = [
            ApiKeyCredentialPolicy(api_key),
            FormEndpointPolicy(endpoint, version),
            headers_policy,
            ContentDecodePolicy(),
        ]
        self._pipeline = Pipeline(transport, policies=policies)

    def list_models(self, next_link: str = None):
        def get_next(continuation_token: str) -> RequestsTransportResponse:
            request = create_list_models_request(next_link)
            return self._pipeline.run(request).http_response

        def extract_data(response: RequestsTransportResponse) -> Tuple[str, Iterable[ModelInfo]]:
            listing = read_model_listing(response)
            continuation_token = listing.next_link if listing.next_link else None
            print(continuation_token)
            return continuation_token, listing.model_list

        return PageIterator[ModelInfo](
            get_next=get_next,
            extract_data=extract_data,
            continuation_token=next_link)

    def begin_train(self, source: str, prefix: str = None, include_sub_folders: bool = None, polling_interval: int = 10):
        # Delayed import to avoid circular import
        from ._polling import get_train_operation_id
        request = create_train_request(
            source=source,
            prefix=prefix,
            include_sub_folders=include_sub_folders)
        response = self._pipeline.run(request)
        http_response = response.http_response  # type: RequestsTransportResponse
        operation_id = get_train_operation_id(http_response)
        return self.get_train_operation(operation_id, polling_interval)

    def get_train_operation(self, operation_id: str, polling_interval: int = 10):
        # Delayed import to avoid circular import
        from ._polling import TrainModelOperation
        return TrainModelOperation(self, operation_id, polling_interval)

    def get_model(self, model_id: str):
        request = create_get_model_request(model_id)
        response = self._pipeline.run(request)
        http_response = response.http_response  # type: RequestsTransportResponse
        return read_model(http_response)
