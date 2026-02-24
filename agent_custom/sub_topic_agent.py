from typing import List, Optional,Dict, Any
from google.adk.agents.llm_agent import Agent


def get_generate_subtopic(model,subtopic_name):

    subtopic_agent = Agent(
        model=model,
        name=subtopic_name,
        description=f"Subtopic agent for {subtopic_name}",
        instruction="""You are a subtopic generator specialist.
        
        Given the main research topic from the user input, generate exactly 3 distinct, relevant,
        and concise subtopics suitable for parallel web research.

        Output ONLY the 3 subtopics, each on a new line, formatted like this:
        1. Subtopic 1
        2. Subtopic 2
        3. Subtopic 3
        """      
    )

    return subtopic_agent