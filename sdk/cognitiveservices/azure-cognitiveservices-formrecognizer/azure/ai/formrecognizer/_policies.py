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

from azure.core.pipeline.policies import SansIOHTTPPolicy
from azure.core.pipeline import PipelineRequest

from requests.structures import CaseInsensitiveDict
from urllib.parse import urlparse, urlunparse

API_KEY_HEADER = 'Ocp-Apim-Subscription-Key'
FORM_PATH = '/formrecognizer'


class ApiKeyCredentialPolicy(SansIOHTTPPolicy):
    def __init__(self, api_key: str):
        self._api_key = api_key

    def on_request(self, request: PipelineRequest):
        headers = request.http_request.headers  # type: CaseInsensitiveDict
        headers[API_KEY_HEADER] = self._api_key


class FormEndpointPolicy(SansIOHTTPPolicy):
    def __init__(self, endpoint: str, version: str):
        version = version.rstrip('/')
        self._endpoint = urlparse(endpoint)
        self._version = version

    def on_request(self, request: PipelineRequest):
        url = request.http_request.url  # type: str
        if not url.startswith('http:') and not url.startswith('https:'):
            url = url.lstrip('/')
            scheme, host, path, params, query, fragment = urlparse(url)
            scheme = self._endpoint.scheme
            host = self._endpoint.netloc
            path = '/'.join([FORM_PATH, self._version, url])
            request.http_request.url = urlunparse(
                (scheme, host, path, params, query, fragment))
