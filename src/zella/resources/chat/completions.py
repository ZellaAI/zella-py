

class Completions():
    def __init__(self, client):
        self.client = client

    def create(self, user, model, query, response, options={}):
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