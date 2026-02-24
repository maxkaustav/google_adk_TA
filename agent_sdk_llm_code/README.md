# Coding Agent

This project defines a `SupervisorAgent` that orchestrates the process of generating Python code, validating it, and summarizing its functionality. The agent is built using the `google.adk` framework and leverages multiple sub-agents to perform specific tasks.

**Concepts Covered** : ADK Basics, Tools, Sub-agents, Evaluation (Web evaluation, [Evaluations_ADK](https://codelabs.developers.google.com/adk-eval/instructions#0) )

---

## Features

1. **Code Generation Agent**: 
   - The `CodeGeneratorAgent` generates Python code snippets based on natural language descriptions.

2. **Code Validation Agent**: 
   - The `CodeValidatorAgent` validates the generated Python code for syntax and runtime errors using the `PythonValidatorTool`.

3. **Code Summarization Agent**: 
   - The `SummarizerAgent` analyzes the output of the Python code and generates a natural language summary.

4. **Supervisor Agent**:
   - The `SupervisorAgent` coordinates the above agents to handle programming tasks end-to-end.

---

## Workflow

1. **Input**: A natural language description of a programming task.
2. **Code Generation**: The `CodeGeneratorAgent` generates a Python code snippet.
3. **Code Validation**: The `CodeValidatorAgent` validates the generated code.
   - If the code is invalid, the validation error message is returned.
   - If the code is valid, the process continues.
4. **Code Summarization**: The `SummarizerAgent` produces a natural language explanation of the code.
5. **Output**: A JSON object containing:
   - The generated code.
   - A summary of what the code does.

---

## File Structure

- **`agent.py`**: Contains the implementation of the `SupervisorAgent` and its sub-agents.
- **Environment Variables**:
  - `OPENROUTER_API_KEY`: API key for the OpenRouter model.

---

## Setup

1. **Install Dependencies**:
   Ensure you have the `google.adk` library installed.

2. **Set Environment Variables**:
   Add the `OPENROUTER_API_KEY` to your environment variables.

   Example `.env` file:


3. **Run the Agent**:
Import and use the `SupervisorAgent` in your application.

---

## Example Usage

```bash
pip install google-adk

adk web google_adk_ta

