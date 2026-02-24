from typing import List, Optional,Dict, Any
from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent


def get_research_agents(model,research_agent_name,subtopic_no):
    return Agent(
        model= model,
        name= research_agent_name,
        instruction=
        f"""
        You are an AI Research Assistant.
        Research the latest advancements in the subtopic {subtopic_no}.
        Use the `web_search_tool` tool provided.
        Output *only* the summary. 
        """,
        tools=[web_search_tool]
    )

def get_parallel_research_agent(model, research_agent_name,num_subtopics):

    parallel_research_agent = ParallelAgent(
        name=f"parallel_{research_agent_name}",
        sub_agents=[get_research_agents(model, f"{research_agent_name}_{i+1}", i+1) for i in range(num_subtopics)],
    )

    return parallel_research_agent