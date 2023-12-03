import httpx
import json

from types import SimpleNamespace

from .config import BASE_URL
from . import resources


class ZellaAI():
    def __init__(self, api_key=None, base_url=None):
        if api_key is None:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url or BASE_URL


        self.chat           = resources.Chat(self)
        self.completions    = resources.Completions(self)

        self.client         = httpx.Client(
            headers= {
                'Authorization': f'Bearer {self.api_key}'
            }
        )


    def post(self, path, data, headers={}, options={}):
        response = self.client.post(path, json=data, headers=headers, **options)
        return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
