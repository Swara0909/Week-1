from pydantic import BaseModel, field_validator, Field
from langchain_ollama import ChatOllama
from langchain_core.exceptions import OutputParserException
from typing import Literal

class UserStory(BaseModel):
    title: str
    priority: Literal["Low", "Medium", "High", "Critical"]
    description: str
    estimated_hours: int = Field(ge=1, le=100, description="Hours between 1 and 100")
    acceptance_criteria: str


    @field_validator("priority")
    def validate_priority(cls, v):
        allowed = ["Low", "Medium", "High", "Critical"]
        if v not in allowed:
            raise ValueError(f"priority must be one of {allowed}, got '{v}'")
        return v

    @field_validator("estimated_hours")
    def validate_hours(cls, v):
        if v <= 0 or v > 100:
            raise ValueError("estimated_hours must be between 1 and 100")
        return v
llm = ChatOllama(model="qwen2.5:1.5b")

structured_response = llm.with_structured_output(UserStory)




try:
    result = structured_response.invoke(
        "Write a user story for a login feature in a web application"
    )
    print("Title:", result.title)
    print("Priority:", result.priority)
    print("Description:", result.description)
    print("Estimated Hours:", result.estimated_hours)
    print("Acceptance Criteria:", result.acceptance_criteria)

except OutputParserException as e:
    print("Model returned invalid output.")
    print(e)
