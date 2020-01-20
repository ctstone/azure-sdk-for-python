from asyncio import sleep as async_sleep, new_event_loop, set_event_loop, AbstractEventLoop, coroutine, run_coroutine_threadsafe, Future, ensure_future
from typing import Callable, Union
from time import sleep
from threading import Event, Thread
from uuid import uuid4 as uuid
from azure.core.polling import LROPoller, PollingMethod, AsyncPollingMethod
from azure.core.pipeline.transport import HttpResponse
from .client import FormRecognizerClient
from .aio import FormRecognizerClient as FormRecognizerClientAsync
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
    def __init__(self, client: Union[FormRecognizerClient, FormRecognizerClientAsync], polling_method: PollingMethod, operation_id: str):
        self.operation_id = operation_id
        super().__init__(
            client=client,
            initial_response=None,
            deserialization_callback=None,
            polling_method=polling_method)

    def result(self, timeout: int = None) -> Model:
        return super().result(timeout)


# class AsyncTrainModelOperation(TrainModelOperation):
#     def __init__(self, client: FormRecognizerClientAsync, polling_method: PollingMethod, operation_id: str, interval: int):
#         # self._client = client
#         # self._response = None
#         # self._callbacks = []  # type: List[Callable]
#         # self._polling_method = polling_method

#         super().__init__(client, polling_method, operation_id, interval)

#         # Prepare thread execution
#         def run_async(loop: AbstractEventLoop):
#             set_event_loop(loop)
#             loop.run_forever()
#         self._thread = None
#         self._done = None
#         self._exception = None
#         if not self._polling_method.finished():
#             loop = new_event_loop()
#             self._done = Event()
#             self._thread = Thread(
#                 target=run_async,
#                 args=(loop, ),
#                 name="AsyncLROPoller({})".format(uuid()))
#             self._thread.daemon = True
#             self._thread.start()
#             # loop.call_soon_threadsafe(self._start_async())
#             run_coroutine_threadsafe(self._start_async(), loop)

#     @coroutine
#     async def _start_async(self):
#         '''Start the long running operation. On completion, runs any callbacks.
#         '''
#         try:
#             print('HELLO WORLD')
#             await self._polling_method.run()
#         except Exception as err:  # pylint: disable=broad-except
#             self._exception = err

#         finally:
#             self._done.set()

#         callbacks, self._callbacks = self._callbacks, []
#         while callbacks:
#             for call in callbacks:
#                 call(self._polling_method)
#             callbacks, self._callbacks = self._callbacks, []


class AsyncLROPoller(object):
    def __init__(self, client, initial_response, deserialization_callback, polling_method: PollingMethod):
        self._client = client
        self._response = initial_response
        self._callbacks = []  # type: List[Callable]
        self._polling_method = polling_method
        self._polling_method.initialize(
            self._client, self._response, deserialization_callback)
        self._future = ensure_future(polling_method.run())
        self._future.add_done_callback(self._done)

    def status(self):
        return self._polling_method.status()

    async def result(self, timeout: int = None):
        await self.wait(timeout)
        return self._polling_method.resource()

    async def wait(self, timeout: int = None):
        print(type(self._future))
        await self._future

    def done(self) -> bool:
        return self._future.done()

    def add_done_callback(self, func):
        if self.done():
            func(self._polling_method)
        self._callbacks.append(func)

    def remove_done_callback(self, func):
        if self.done():
            raise ValueError("Process is complete.")
        self._callbacks = [c for c in self._callbacks if c != func]

    def _done(self, result):
        callbacks, self._callbacks = self._callbacks, []
        while callbacks:
            for call in callbacks:
                call(self._polling_method)
            callbacks, self._callbacks = self._callbacks, []


class AsyncTrainModelOperation(AsyncLROPoller):
    def __init__(self, client: FormRecognizerClientAsync, polling_method: PollingMethod, operation_id: str):
        self.operation_id = operation_id
        super().__init__(client, None, None, polling_method)


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


class AsyncTrainPollingMethod(PollingMethod):
    def __init__(self, model_id: str, interval: int):
        self._client = None  # type: FormRecognizerClientAsync
        self._model_id = model_id
        self._interval = interval
        self._model = None  # type: Model

    async def _update_status(self):
        print('GETTING STATUS: %s' % self._model_id)
        self._model = await self._client.get_model(self._model_id)

    def initialize(self, client: FormRecognizerClient, initial_response, deserialization_callback):
        print('INIT CLIENT %s' % client)
        self._client = client

    def status(self):
        return self._model.model_info.status.value if self._model else None

    def finished(self):
        status = self._model.model_info.status if self._model else None
        return status and (status == ModelStatus.READY or status == ModelStatus.INVALID)

    async def run(self):
        while not self.finished():
            await self._update_status()
            if not self.finished():
                await async_sleep(self._interval)

    def resource(self):
        return self._model
