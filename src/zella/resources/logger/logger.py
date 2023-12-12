from .log_consumer import LogConsumer


class Logger:
    def __init__(self, client, batch_logging):
        self.client = client
        self.log_consumer = LogConsumer(client) if batch_logging else None
        self.batch_logging = batch_logging
        pass

    def log(self, action, request, response, platform, model, **kwargs):
        """
        Log a request to Zella.

        Args:
            action (str): Action type of the request [Eg, chat.completions, embedding].
            request (str): Request sent to the platform.
            response (str): Response received to the platform.
            platform (str): Platform name.
            model (str): Model name.
            **kwargs: Additional arguments for prompt retrieval. Valid arguments are:
                - token_usage (dict, optional): Dictionary of token usage details.
                    - prompt_tokens (int): Prompt tokens.
                    - completion_tokens (int): Completion tokens.
                    - total_tokens (int): Total tokens.
                - meta (dict, optional): Dictionary of optional metadata to be logged.

        """
        log_request = {
            "action": action,
            "request": request,
            "response": response,
            "platform": platform,
            "model": model,
        }
        if kwargs.get("user"):
            log_request["user"] = kwargs.get("user")
        if kwargs.get("meta"):
            log_request["meta"] = kwargs.get("meta")
        if kwargs.get("token_usage"):
            log_request["token_usage"] = kwargs.get("token_usage")

        if self.batch_logging:
            self.log_consumer.consume(log_request)
            return
        else:
            data = self.client.post(self.client.base_url + "/log", log_request)
            return data
