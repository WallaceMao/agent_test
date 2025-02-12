from typing import Dict, Any

from .base_agent import BaseAgent


class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Matcher",
            instructions="""Match candidate profiles with job positions.
            Consider: skills match, experience level, location preferences.
            Provide detailed reasoning and compatibility scores.
            Return matches in JSON format with title, match_score, and location fields.""",
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        pass

