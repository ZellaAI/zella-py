class Prompt:
    def __init__(self, client):
        self.client = client
        pass

    def get(self, prompt_id, user=None, **kwargs):
        """
        Retrieve a prompt from the server.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.
            user (str, optional): The ID of the user. Defaults to None.
            **kwargs: Additional arguments for prompt retrieval. Valid arguments are:
                - prompt_variant_id (str, optional): The ID of the prompt variant. Defaults to None.
                - context (str, optional): Context to substitute into the prompt. Defaults to None.

        Returns:
            dict: The retrieved prompt data.

        """
        prompt_request = {
            "prompt_id": prompt_id,
        }
        if user:
            prompt_request["user_id"] = user
        if kwargs.get("prompt_variant_id"):
            prompt_request["prompt_variant_id"] = kwargs.get("prompt_variant_id")
        if kwargs.get("context"):
            prompt_request["context"] = kwargs.get("context")

        data = self.client.post(self.client.base_url + "/prompt/slug", prompt_request)
        return data