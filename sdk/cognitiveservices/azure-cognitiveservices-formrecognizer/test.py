'''
Testing
'''

from asyncio import get_event_loop
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer.aio import FormRecognizerClient as FormRecognizerClientAio


def main():
    ''' Test function '''
    custom_headers = {'apim-subscription-id': '123'}
    client = FormRecognizerClient(
        endpoint='http://192.168.1.4:5000',
        api_key='123',
        custom_headers=custom_headers)

    # listing = client.list_models()
    # for model_info in listing.model_list:
    #     print(model_info.model_id)

    # model = client.get_model('30620738-ebd2-43d5-b6e0-a1bec5c87aea')
    # print(model)

    source = "https://chstonefr.blob.core.windows.net/test?st=2019-10-24T20%3A28%3A06Z&se=2021-10-25T20%3A28%3A00Z&sp=rl&sv=2018-03-28&sr=c&sig=indl6uxPGs4YX7ZUbg5dp6WDVH2i86IRv1Sw2U8l8jA%3D"
    prefix = "amazon"
    operation = client.begin_train(source=source, prefix=prefix)
    print('Created model %s' % (operation.operation_id))
    print('Waiting...')
    model = operation.result(60)
    if model:
        print(model.model_info.status.value)


def main_async():
    ''' Entry for async tests '''
    loop = get_event_loop()
    loop.run_until_complete(run_async())


async def run_async():
    ''' Test async function '''
    custom_headers = {'apim-subscription-id': '123'}
    client = FormRecognizerClientAio(
        endpoint='http://192.168.1.4:5000',
        api_key='123',
        custom_headers=custom_headers)
    listing = await client.list_models()
    for model_info in listing.model_list:
        print(model_info.model_id)


if __name__ == '__main__':
    # main_async()
    main()
