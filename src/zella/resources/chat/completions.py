

class Completions():
    def __init__(self, client):
        self.client = client

    def create(self, user, model, query, response, options={}):
        if response.get("stream") == True:
            stream = self.client.stream(
                "POST",
                self.client.base_url + "/chat/completions",
                {
                    "user": user,
                    "model": model,
                    "query": query,
                    "response": response,
                    "options": options
                }
            )
            return stream
        else:
            data = self.client.post(
                self.client.base_url + "/chat/completions",
                {
                    "user": user,
                    "model": model,
                    "query": query,
                    "response": response,
                    "options": options
                }
            )
            return data