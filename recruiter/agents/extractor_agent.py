from typing import Dict, Any

from .base_agent import BaseAgent


class ExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Extractor",
            instructions="""Extract and structure information from resumes.
            Focus on: personal info, work experience, education, skills, and certifications.
            Provide output in a clear, structured format."""
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        pass


