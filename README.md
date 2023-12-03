# Zella AI Python Package

This is a Python package for accessing Zella APIs.


## Example Usage

```python
api_key = 'api_jad3uf93iaf92902lkdj2ldu092d3d'


zella_ai = ZellaAI(api_key)
user = "user_jskjf93o101"
model = {
    "platform": "openai",
    "name": "gpt-3.5-turbo"
}
query = {
    "messages": [ {
        "role": "system",
        "content": "You are a helpful assistant to help design api structure"
    },
    {
        "role": "user",
        "content": "Hi There!"
    }]
}
response = {
    "format": "json_object"
}


response = zella_ai.chat.completions.create(user, model, query, response)

assert response.status.type == 'ok'

```