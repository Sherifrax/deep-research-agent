from dataclasses import dataclass
from typing import Literal
from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio

# Stage indices line up with the "Plan / Search / Write / Deliver" steps shown in the UI.
STAGE_COUNT = 4


@dataclass
class ResearchUpdate:
    """A single update emitted while research is in progress.

    `kind` is "status" for progress messages, or "report" for the final markdown report.
    `stage` is the index of the step this update belongs to (0-based); once all stages are
    complete it is set to STAGE_COUNT so the UI can mark every step as done.
    """
    kind: Literal["status", "report"]
    stage: int
    message: str


class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield ResearchUpdate("status", 0, f"Starting research. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            search_plan = await self.plan_searches(query)
            yield ResearchUpdate("status", 1, f"Searches planned, starting {len(search_plan.searches)} searches...")
            search_results = await self.perform_searches(search_plan)
            yield ResearchUpdate("status", 2, "Searches complete, writing report...")
            report = await self.write_report(query, search_results)
            yield ResearchUpdate("status", 3, "Report written, sending email...")
            await self.send_email(report)
            yield ResearchUpdate("status", STAGE_COUNT, "Email sent, research complete")
            yield ResearchUpdate("report", STAGE_COUNT, report.markdown_report)

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input_message)
        return result.final_output

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        input_message = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output
    
    async def send_email(self, report: ReportData) -> None:
        await Runner.run(email_agent, report.markdown_report)