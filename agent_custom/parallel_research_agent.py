from typing import List, Optional,Dict, Any
from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
import os


web_search_tool = MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://mcp.tavily.com/mcp/",
                headers={
                    "Authorization": f"Bearer {os.getenv("TAVILY_API_KEY")}",
                },
            ),
        )

def get_research_agents(model,research_agent_name,subtopic)-> Agent:
    """
    Returns an AI Research Assistant agent that researches the latest advancements in the given subtopic using the web_search_tool.

    Args:
        model: The model to use for the agent
        research_agent_name: The name of the research agent
        subtopic: The topic to research

    Returns:
        An Agent that researches the given topic
    """
    return Agent(
        model= model,
        name= research_agent_name,
        instruction=
        f"""
        **Your Core Identity and Sole Purpose:**
            You are an AI Research Assistant.
            Research the latest advancements in the topic {subtopic}.

        ** Output **
          Return *only* the relevant findings summarized in 50 words.
        """,
        # tools=[web_search_tool]
    )
# ** Tools **
#          - You have access to tavily mcp so you have multiple tools
#          - First look at tools you have
#          - Indentify only those tools relevant to your research task.
#          - Use the relevant tools to gather information and answer the research question.