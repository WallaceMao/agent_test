import os
from typing import Dict, Any

from openai import OpenAI

from ..utils.exceptions import ModelNotExistsError


class BaseAgent:
    def __init__(self, name: str, instructions: str, model: str = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        if not self.model:
            self.model = os.environ.get("DEFAULT_MODEL")
        if not self.model:
            raise ModelNotExistsError(f"Model not found")
        self.ai_client = OpenAI()

    async def run(self, messages: list) -> Dict[str, Any]:
        """默认实现方法，要被子类实现的"""
        raise NotImplementedError("Subclasses must implement run()")

