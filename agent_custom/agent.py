from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import ParallelAgent,BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types
from .sub_topic_agent import get_generate_subtopic
from .parallel_research_agent import get_research_agents
from .summary_write_agent import get_generate_summary_agent
from typing import AsyncGenerator
from typing_extensions import override
import logging
import os


##############################
#      SETUP OPENROUTER      #
##############################

# Get the Groq API key from environment variables
api_key = os.environ.get('GROQ_API_KEY')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##############################
#      SUB TOPIC AGENT       #
##############################
subtopic_model = LiteLlm(
    model="groq/llama-3.1-8b-instant", # to generate only subtopics
    api_key=api_key
)
subtopic_agent = get_generate_subtopic(subtopic_model, "subtopic_agent")



##############################
#      SUMMARY AGENT       #
##############################

summary_model = LiteLlm(
    model="groq/openai/gpt-oss-120b", # to summarize to big model
    api_key=api_key
)
summary_agent = get_generate_summary_agent(summary_model, "summary_agent")

research_model = LiteLlm(
    model="groq/openai/gpt-oss-20b", # no token limit model
    api_key=api_key
)

##############################
#      ORCHESTRATOR AGENT       #
##############################

class HeadResearcher(BaseAgent):

    def __init__(self, name, subtopic_agent, summary_agent, **kwargs):

        super().__init__(
            name=name,
            sub_agents=[subtopic_agent,summary_agent]
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # Implement the orchestration logic here

        # Run subtopic agent
        logger.info("Running subtopic agent...")
        async for event in self.sub_agents[0].run_async(ctx):
            yield event

        # Fan out parallel research
        subtopics_list = ctx.session.state["subtopics"]['subtopics']
        logger.info(f"Subtopics generated: {subtopics_list}")
        research_agent_list=[]
        for subtopic in subtopics_list:
            logger.info(f"Running research agent for subtopic: {subtopic}")
            research_agent_list.append(get_research_agents(research_model,f"r_{subtopic.replace(' ', '_')}",subtopic))

        parallel_agent = ParallelAgent(
            name="parallel_research_agent",
            sub_agents=research_agent_list
        )
        
        logger.info("Running parallel research agents...")
        async for event in parallel_agent.run_async(ctx):
            yield event
        
        # Run Summarizer agent
        logger.info("Running summary agent...")
        async for event in self.sub_agents[1].run_async(ctx):
            yield event

root_agent = HeadResearcher(
    name='root_agent',
    subtopic_agent=subtopic_agent,
    summary_agent=summary_agent
)
