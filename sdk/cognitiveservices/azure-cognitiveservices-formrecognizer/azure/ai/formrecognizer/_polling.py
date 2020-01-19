from typing import Callable
from time import sleep
from azure.core.polling import LROPoller, PollingMethod
from azure.core.pipeline.transport import HttpResponse
from .client import FormRecognizerClient
from .models import Model, ModelStatus

LOCATION_HEADER = 'Location'


def get_train_operation_id(response: HttpResponse) -> str:
    location = response.headers.get(LOCATION_HEADER)
    if location:
        i = location.rfind('/')
        if i >= 0:
            return location[i + 1:]
    raise Exception('Cannot parse train location.')


class TrainModelOperation(LROPoller):
    def __init__(self, client: FormRecognizerClient, operation_id: str, interval: int):
        self.operation_id = operation_id
        method = TrainPollingMethod(operation_id, interval)
        super().__init__(
            client=client,
            initial_response=None,
            deserialization_callback=None,
            polling_method=method)

    def result(self, timeout: int = None) -> Model:
        return super().result(timeout)


class TrainPollingMethod(PollingMethod):
    def __init__(self, model_id: str, interval: int):
        self._client = None  # type: FormRecognizerClient
        self._model_id = model_id
        self._interval = interval
        self._model = None  # type: Model

    def _update_status(self):
        self._model = self._client.get_model(self._model_id)

    def initialize(self, client: FormRecognizerClient, initial_response, deserialization_callback):
        self._client = client

    def status(self):
        return self._model.model_info.status.value if self._model else None

    def finished(self):
        status = self._model.model_info.status if self._model else None
        return status and (status == ModelStatus.READY or status == ModelStatus.INVALID)

    def run(self):
        while not self.finished():
            self._update_status()
            if not self.finished():
                sleep(self._interval)

    def resource(self):
        return self._model
