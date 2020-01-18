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

from typing import Dict
from azure.core.pipeline import Pipeline
from azure.core.pipeline.policies import HeadersPolicy, ContentDecodePolicy
from azure.core.pipeline.transport import RequestsTransport, HttpRequest, RequestsTransportResponse
from ._policies import ApiKeyCredentialPolicy, FormEndpointPolicy
from ._requests import create_list_models_request
from ._serialization.responses import read_model_listing


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
        request = create_list_models_request()
        response = self._pipeline.run(request)
        http_response = response.http_response  # type: RequestsTransportResponse
        return read_model_listing(http_response)  # TODO: paging
