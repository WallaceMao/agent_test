import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from utils.logger import setup_logger
from .agents.orchestrator import OrchestratorAgent

load_dotenv()
logger = setup_logger()
console = Console()


async def process_resume(file_path: str) -> None:
    """执行一个自动招聘流程"""
    try:
        # 做必要的验证
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")
        if not file_path.lower().endswith(".pdf"):
            raise ValueError(f"File is not pdf file")

        # 开始处理文件
        logger.info(f"starting recruitment process for {os.path.basename(file_path)}")
        console.print(
            Panel.fit(
                "[bold blue]AI 招聘助手[/bold blue]\n"
                "[dim]由毛文强提供[/dim]",
                border_style="blue"
            )
        )

        # 初始化 orchestrator 编排
        orchestrator = OrchestratorAgent()

        resume_data = {
            "file_path": file_path,
            "submission_timestamp": datetime.now().isoformat()
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progres:
            task = progres.add_task("[cyan]处理简历中...", total=None)
            result = await orchestrator.process_application(resume_data)
            progres.update(task, completed=True)
            console.print(result)

    except FileNotFoundError as e:
        logger.error(f"File error: {str(e)}", exc_info=False)
        console.print(f"[red]File error:[/red] {str(e)}")
    except Exception as e:
        logger.error(f"unexpectedError: {str(e)}", exc_info=True)
        console.print(f"[red]unexpectedError:[/red] {str(e)}")


def main():
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, "resumes", "sample_resume.pdf")
    asyncio.run(process_resume(file_path))


if __name__ == "__main__":
    main()
