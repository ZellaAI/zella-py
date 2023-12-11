import os
import sys

sys.path.append('../src')


from zella import ZellaAI


api_key = os.environ.get('ZELLA_API_KEY')
zella_ai = ZellaAI(api_key)


def chat_completion():
    user = "2312re3r33e33"
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

    assert response.status.type == "ok"

def chat_completion_with_streaming():
    user = "2312re3r33e33"
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
    stream = zella_ai.chat.completions.create(user, model, query, response)

    for chunk in stream:
        assert chunk.id

def retrieve_prompt():
    prompt_id = "test-prompt"
    prompt = zella_ai.prompt.get(prompt_id)
    assert prompt.data.id == prompt_id

def retrieve_prompt_by_variant_id():
    prompt_id = "test-prompt"
    prompt_variant_id = "test-variant-2"
    prompt = zella_ai.prompt.get(prompt_id, prompt_variant_id=prompt_variant_id)
    assert prompt.data.id == prompt_id
    assert prompt.data.variant_id == prompt_variant_id

def embed():
    user = "2312re3r33e33"
    model = {
        "platform": "openai",
        "name": "text-embedding-ada-002"
    }
    query = {
        "input": "Hello World!",
    }
    response = {
        "format": "float"
    }
    response = zella_ai.embedding.embed(user, model, query, response)
    assert response.status.type == "ok"

def log():
    action = "chat.completion"
    request = {"inputs":{"question":"What is my name?","context":"My name is Clara and I live in Berkeley."}}
    response = {"score":0.933128833770752,"start":11,"end":16,"answer":"Clara"}
    meta = {"model": "deepset/roberta-base-squad2"}
    response = zella_ai.logger.log(action, request, response, "huggingface", "deepset/roberta-base-squad2", meta=meta)

    assert response.status.type == "ok"


if __name__ == "__main__":
    chat_completion()
    chat_completion_with_streaming()
    retrieve_prompt()
    retrieve_prompt_by_variant_id()
    embed()
    log()
