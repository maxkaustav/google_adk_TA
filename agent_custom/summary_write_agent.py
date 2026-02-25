from typing import List, Optional,Dict, Any
from google.adk.agents.llm_agent import Agent

def get_generate_summary_agent(model, agent_name)->Agent:

    """
    Returns an Agent that summarizes content.

    The agent is a specialized AI Summary Agent that transforms input content into a clear, structured, and concise summary while preserving key meaning, intent, and factual accuracy.

    Args :
        :param model: The model to use for the agent
        :param agent_name: The name of the agent
        :return: An Agent that summarizes content
    
    Returns:
        An Agent that summarizes content
    """
    sumarizer_agent = Agent(
        model=model,
        name=agent_name,
        description=f"You are a Summarizer agent",
        instruction="""
            **Your Core Identity and Sole Purpose:**
                You are a specialized AI Summary Agent. 
                Your sole and exclusive purpose is to transform input content into a clear, structured, and concise summary while preserving key meaning, intent, and factual accuracy.

                You do NOT add new information.
                You do NOT hallucinate details.
                You do NOT interpret beyond the provided content.
                You only summarize what is explicitly present.
        """      
    )

    return sumarizer_agent