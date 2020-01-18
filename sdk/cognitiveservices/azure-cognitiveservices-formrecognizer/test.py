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

    listing = client.list_models()
    print(listing)


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
    for x in listing.model_list:
        print(x.model_id)


if __name__ == '__main__':
    main_async()
