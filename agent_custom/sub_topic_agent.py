from typing import List, Optional,Dict, Any
from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel,Field

class SubtopicOutput(BaseModel):
    subtopics: List[str] = Field(description="List of generated subtopics")

def get_generate_subtopic(model,subtopic_name)-> Agent:
    """
    Returns a subtopic generation agent for the given model and subtopic name.

    The subtopic generation agent is responsible for generating distinct, relevant,
    and concise subtopics suitable for parallel web research, given the main research topic from the user input.

    Args:
        model: The model to use for the agent
        subtopic_name: The name of the subtopic agent
    Returns:
        An Agent that generates subtopics
    """
    subtopic_agent = Agent(
        model=model,
        name=subtopic_name,
        description=f"Subtopic agent for {subtopic_name}",
        instruction="""You are a subtopic generator specialist.
        
        Given the main research topic from the user input and number of topics to generate, 
        generate exactly the number of distinct sub-topics requested by the user, relevant,
        and concise subtopics suitable for parallel web research.

        ** Output Schema **
        Output ONLY the number of distinct subtopics, as a *list of strings*.
        DO NOT include any additional text or explanations.
        DO NOT include any of these symbols [!,@,#,$,%,^,&,*,(,),:,:,",',/,\]
    
        
        **subtopics** : [subtopic1, subtopic2, subtopic3,....,subtopicN]
        """ ,
        output_key="subtopics",
        output_schema=SubtopicOutput  
    )

    return subtopic_agent