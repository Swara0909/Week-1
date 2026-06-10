from langgraph.graph import StateGraph, START, END

from state import ResumeFormatter

from nodes.input_validation import input_validator
from nodes.clean_resume import cleaner
from nodes.section_extractor import section_extractor
from nodes.summary_generator import summary_generator


builder = StateGraph(ResumeFormatter)

builder.add_node("validator", input_validator)
builder.add_node("cleaner", cleaner)
builder.add_node("extractor", section_extractor)
builder.add_node("summary", summary_generator)

builder.add_edge(START, "validator")
builder.add_edge("validator", "cleaner")
builder.add_edge("cleaner", "extractor")
builder.add_edge("extractor", "summary")
builder.add_edge("summary", END)

graph = builder.compile()

sample_resume = """
John Doe

Skills: Python, SQL, AWS

Experience: 3 years as Backend Developer
"""

result = graph.invoke(
    {
        "raw_resume": sample_resume
    }
)

print("\n===== FINAL OUTPUT =====\n")
print(result["summary"])