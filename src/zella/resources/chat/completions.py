from typing import Any, Dict, Optional


class Completions:
    """
    A class to handle the creation of chat completion requests.
    """

    def __init__(self, client: Any) -> None:
        """
        Initialize the Chat Completions class with a client.

        :param client: Client object to handle requests.
        """
        self.client = client

    def _build_url(self, endpoint: str) -> str:
        """
        Build the complete URL for an API request.

        :param endpoint: The endpoint of the API.
        :return: The complete URL.
        """
        return self.client.base_url + endpoint

    def create(
            self,
            model: str,
            prompt: Dict = None,
            query: Dict = None,
            user: str = None,
            conversation_id: str = None,
            message_chain_id: str = None,
            response: Dict = {},
            options: Dict = {}
    ) -> Any:
        """
        Create a chat completion request.

        :param user: User associated with the request.
        :param conversation_id: Identifier for the conversation.
        :param message_chain_id: Identifier for the message chain.
        :param model: The model used for completion.
        :param prompt: The prompt for the request.
        :param query: The query for the request, if prompt is not present.
        :param response: The response parameters.
        :param options: Additional options for the request.
        :return: The response from the API.
        """
        request = {k: v for k, v in locals().items() if v is not None and k != 'self'}

        if response and response.get("stream"):
            return self.client.stream("POST", self._build_url("/chat/completions"), request)

        return self.client.post(self._build_url("/chat/completions"), request)
