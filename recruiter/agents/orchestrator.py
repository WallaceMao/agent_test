from typing import Dict, Any

from .base_agent import BaseAgent
from .extractor_agent import ExtractorAgent
from .analyzer_agent import AnalyzerAgent
from .matcher_agent import MatcherAgent
from .screener_agent import ScreenerAgent
from .recommender_agent import RecommenderAgent


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            instructions="""Coordinate the recruitment workflow and delegate tasks to specialized agents.
            Ensure proper flow of information between extraction, analysis, matching, screening, and recommendation phases.
            Maintain context and aggregate results from each stage."""
        )
        self._setup_agents()

    def _setup_agents(self):
        """初始化所有的agent"""
        self.extractor = ExtractorAgent()
        self.analyzer = AnalyzerAgent()
        self.matcher = MatcherAgent()
        self.screener = ScreenerAgent()
        self.recommender = RecommenderAgent()

    async def process_application(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """编排应用的主流程"""
        print("🎯 Orchestrator: Starting application process")

        # 全局上下文，用来在 Agent 中共享数据
        workflow_context = {
            "resume_data": resume_data,
            "status": "initiated",
            "current_stage": "extraction"
        }

        try:
            # 提取简历信息
            extracted_data = await self.extractor.run(
                [{"role": "user", "content": str(resume_data)}]
            )
            workflow_context.update({"extracted_data": extracted_data, "current_stage": "analysis"})

            # 分析简历
            analysis_results = await self.analyzer.run(
                [{"role": "user", "content": str(extracted_data)}]
            )
            workflow_context.update({"analysis_results": analysis_results, "current_stage": "matching"})

            # 匹配job
            job_matches = await self.matcher.run(
                [{"role": "user", "content": str(analysis_results)}]
            )
            workflow_context.update({"job_matches": job_matches, "current_stage": "screening"})

            # 筛选候选人
            screening_results = await self.screener.run(
                [{"role": "user", "content": str(workflow_context)}]
            )
            workflow_context.update({"screening_results": screening_results, "current_stage": "recommendation"})

            # 生成推荐
            final_recommendation = await self.recommender.run(
                [{"role": "user", "content": str(workflow_context)}]
            )
            workflow_context.update(
                {"final_recommendation": final_recommendation, "status": "completed", "current_stage": "completed"}
            )

            return workflow_context

        except Exception as e:
            workflow_context.update({"status": "failed", "error": str(e)})
            raise
