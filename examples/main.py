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


def completion():
    user = "2312re3r33e33"
    model = {
        "platform": "openai",
        "name": "gpt-3.5-turbo"
    }
    query = {
        "content": "What is 3+4?"
    }
    response = {
    }
    response = zella_ai.completions.create(user, model, query, response)
    print(response)
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
    request = {"inputs": {"past_user_inputs": ["Which movie is the best ?"], "generated_responses": ["It is Die Hard for sure."], "text":"Can you explain why ?"}}
    response = {"generated_text":"It's the best movie ever.","conversation":{"past_user_inputs":["Which movie is the best ?","Can you explain why ?"],"generated_responses":["It is Die Hard for sure.","It's the best movie ever."]}}
    meta = {"model": "deepset/roberta-base-squad2"}
    response = zella_ai.logger.log(action, request, response, "huggingface", "deepset/roberta-base-squad2", meta=meta)

    assert response.status.type == "ok"


def langchain():
    from langchain.llms import OpenAI, HuggingFaceHub
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    llm = OpenAI()
    prompt = PromptTemplate.from_template("1 + {number} = ")
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[zella_ai.langchain_callback])
    chain.run(number=2)

    OpenAI().invoke(input="Why should we care about climate change?", config={"callbacks": [zella_ai.langchain_callback]})

    chat = ChatOpenAI(max_tokens=25, streaming=True, callbacks=[zella_ai.langchain_callback])
    chat([HumanMessage(content="Tell me a joke")])

    repo_id = "google/flan-t5-xxl"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
    )
    llm.invoke(input="Why should we care about climate change?", config={"callbacks": [zella_ai.langchain_callback]})


if __name__ == "__main__":
    chat_completion()
    chat_completion_with_streaming()
    retrieve_prompt()
    retrieve_prompt_by_variant_id()
    embed()
    log()
    langchain()
    completion()
