import os
import sys

sys.path.append('./src')


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


if __name__ == "__main__":
    chat_completion()
    chat_completion_with_streaming()