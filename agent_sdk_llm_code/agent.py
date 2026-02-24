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

##############################
#      Code Generator Agent  #
##############################


code_genrator_agent = Agent(
    name= "CodeGeneratorAgent",
    model = model,
    description="Generate code snippets from natural language descriptions.",   
    instruction="""You are a code generation agent.
    Input: a programming task description
    Output: a code snippet that implements the task
    """
)

def python_code_validation_tool(code: str) -> bool:
    """
    Validate Python code for syntax errors.

    Args:
        code (str): The Python code to validate.

    Returns:
        str: A message indicating whether the code is valid or not.
    """
    try:
        compiled = compile(code, "<string>", "exec")
        namespace = {}
        result = exec(compiled, namespace)
        return  f"Valid: {result}"
    except SyntaxError as se:
        return f"Invalid: SyntaxError: {se.msg} at line {se.lineno}"
    except Exception as e:
        return f"Invalid: RuntimeError: {e}"

############ Code Validator Agent #############

code_validator_agent = Agent(
    name="CodeValidatorAgent",
    model=model,
    description="Validates Python code snippet for syntax and runtime errors by using the PythonValidatorTool.",
    instruction="""
    You are CodeValidatorAgent.
    You receive a Python code snippet.

    Instead of trying to validate the code yourself, call the PythonValidatorTool to:
    - Check syntax errors,
    - Run the code safely on a sample input.

    Return the validation result.
    """,
    tools=[python_code_validation_tool]
)

########### Summarizer Agent #############

summarizer_agent = Agent(
    name="SummarizerAgent",
    model="gemini-2.5-pro",
    description="Summarizes output from the Python code snippet in natural language",
    instruction="""
                You are Results interpretation Agent responsible for analyzing results and generating insights.
                    Your tasks:
                    1. Analyze results.
                    2. Identify patterns and trends.
                    3. Generate meaningful business insights.
                    4. Translate technical findings into business language.

                    Input: [Query Results]
                    Expected Output:
                    1. Key findings and insights.
                    2. Trend analysis.
                    """
                    )

############ Supervisor Agent #############

root_agent = Agent(
    model=model,
    name = 'SupervisorAgent',
    description = 'Supervises and coordinates other agents like code generation, validation and summarization.',
    instruction = """
    You are a Supervisor Agent responsible for handling a programming task described in natural language.

        1. Generate Python code that implements the given task.
        2. Validate the generated code for syntax and runtime errors.
        3. If the code is invalid, output only the validation error message.
        4. If the code is valid, produce a natural language explanation summarizing what the code does.
        5. Output a JSON object with two fields.

        {
            "code": "<generated_code_snippet>",
            "summary": "<natural_language_explanation>"
        }

        Use the following agents to do the task:
            - code_generator_agent
            - code_validator_agent
            - code_summarizer_agent
    
        Do not solve the task yourself; instead, orchestrate the process by requesting each step
    """,
    sub_agents= [code_genrator_agent,code_validator_agent,summarizer_agent]
)