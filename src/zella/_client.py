import httpx
import json

from types import SimpleNamespace

from .version import VERSION
from .config import BASE_URL
from . import resources


class ZellaAI:
    def __init__(self, api_key=None, base_url=None, batch_logging=False, timeout=600):
        if api_key is None:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url or BASE_URL

        self.chat                   = resources.Chat(self)
        self.completions            = resources.Completions(self)
        self.prompt                 = resources.Prompt(self)
        self.embedding              = resources.Embedding(self)
        self.logger                 = resources.Logger(self, batch_logging)
        self.langchain_callback     = resources.LangChainCallback(self)
        self.client                 = httpx.Client(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'User-Agent': f'zella-py/{VERSION}'
            },
            timeout=timeout
        )

    def post(self, path, data, headers={}, options={}):
        response = self.client.post(path, json=data, headers=headers, **options)
        return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

    def stream(self, request_type, path, data, headers={}, options={}):
        with self.client.stream(request_type, path, json=data, headers=headers, **options) as r:
            for line in r.iter_lines():
                if line == '[DONE]':
                    return
                if line and not line.startswith(':'):
                    fieldname, _, value = line.partition(":")
                    if value.startswith(" "):
                        value = value[1:]
                    if fieldname == "data" and value != "[DONE]":
                        yield json.loads(value, object_hook=lambda d: SimpleNamespace(**d))