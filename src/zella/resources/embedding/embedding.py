class Embedding:
    def __init__(self, client):
        self.client = client
        pass

    def embed(self, user, model, query, response, options={}):
        """
        Embeds the given query and response using the specified model.

        Args:
            user (str): The user identifier.
            model (dict): The model identifier.
            query (dict): The query to be embedded.
            response (dict): The response format and configurations.
            options (dict, optional): Additional options for embedding. Defaults to {}.

        Returns:
            dict: The embedded data.

        """
        data = self.client.post(
            self.client.base_url + "/embeddings",
            {
                "user": user,
                "model": model,
                "query": query,
                "response": response,
                "options": options
            }
        )
        return data
