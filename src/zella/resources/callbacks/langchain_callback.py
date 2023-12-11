from typing import Any, Dict, List, Optional
from uuid import UUID

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
    from langchain_core.outputs import LLMResult
except ImportError:
    BaseCallbackHandler = Any
    LLMResult = Any


class LangChainCallback(BaseCallbackHandler):

    def __init__(self, client):
        self.client = client
        self.runs = {}

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        try:
            self.runs[run_id] = {}
            self.runs[run_id]["action"] = "chat.completions"
            self.runs[run_id]["request"] = prompts
            invocation_params = kwargs.get("invocation_params")
            if invocation_params["_type"] == "openai":
                self.runs[run_id]["platform"] = "openai"
                self.runs[run_id]["model"] = invocation_params["model_name"]
            elif invocation_params["_type"] == "openai-chat":
                self.runs[run_id]["platform"] = "openai"
                self.runs[run_id]["model"] = invocation_params["model"]
            elif invocation_params["_type"] == "huggingface_hub":
                self.runs[run_id]["platform"] = "huggingface"
                self.runs[run_id]["model"] = invocation_params["repo_id"]
            else:
                self.runs[run_id]["platform"] = "unknown"
                self.runs[run_id]["model"] = "unknown"
            self.runs[run_id]["meta"] = {
                "source": "langchain-callback"
            }
        except Exception:
            return

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        try:
            if run_id not in self.runs:
                return
            resp = {
                "generated_texts": []
            }
            for generation in response.generations:
                for output in generation:
                    resp["generated_texts"].append(output.text)
            self.runs[run_id]["response"] = resp
            self.client.logger.log(**self.runs[run_id])
            del self.runs[run_id]
        except Exception:
            return
