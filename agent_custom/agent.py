from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import os


##############################
#      SETUP OPENROUTER      #
##############################

# Get the OpenRouter API key from environment variables
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")

# Set up the model using LiteLlm with OpenRouter
model = LiteLlm(
    model="openrouter/z-ai/glm-4.5-air:free",
    api_key=openrouter_api_key
)

root_agent = Agent(
    model=model,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
