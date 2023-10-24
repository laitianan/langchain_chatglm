import inspect


def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)

from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator

PROMPT = """\
Given the function name and source code, generate an English language explanation of the function.
Function Name: {function_name}
Source Code:
{source_code}
Explanation:
"""


class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    pass
fn_explainer = FunctionExplainerPromptTemplate(input_variables=["function_name"])

# Generate a prompt for the function "get_source_code"
prompt = fn_explainer.format(function_name=get_source_code)
print(prompt)