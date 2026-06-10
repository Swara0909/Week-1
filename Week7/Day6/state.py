from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

class ResumeFormatter(TypedDict):
    raw_resume:str
    cleaned_resume:str
    name:str
    experience:str
    skills:List[str]
    summary:str