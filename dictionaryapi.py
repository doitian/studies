import requests
from urllib.parse import urlencode, quote_plus

API_ENDPOINT = 'https://www.dictionaryapi.com/api/v1/references/collegiate/xml/{0}?'


class DictionaryApi:
    def __init__(self, api_key):
        query_string = urlencode({'key': api_key}, quote_via=quote_plus)
        self.api_endpoint = API_ENDPOINT + query_string

    def lookup(self, word):
        return requests.get(self.api_endpoint.format(quote_plus(word))).text


if __name__ == "__main__":
    import os

    api = DictionaryApi(os.environ['API_KEY'])
    print(api.lookup('friend'))
