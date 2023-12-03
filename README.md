# Zella AI Python Package

This is a Python package for accessing Zella APIs.


## Installation

```bash
pip install zella
```

## Initialize Zella AI using API Key

```python 

api_key = 'api_jad3uf93iaf92902lkdj2ldu092d3d'
zella_ai = ZellaAI(api_key)


```

## Chat Completion
Use Chat Completion API to get response from llms

```python

# Create Request Parameters
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

# Call API
response = zella_ai.chat.completions.create(user, model, query, response)

```

## Streaming Chat Completion
Pass stream parameter in response to get streaming response from llms

```python
# Create Request Parameters
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
    "format": "json_object",
    "stream": True
}

# Call API
stream = zella_ai.chat.completions.create(user, model, query, response)

# Iterate over stream
for chunk in stream:
    if chunk:
        print(chunk)

```


## Complete Example Usage

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