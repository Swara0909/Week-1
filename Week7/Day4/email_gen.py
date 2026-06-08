from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv("../.env")

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)


# State
class State(TypedDict):
    topic: str
    company: str
    sender: str
    designation: str
    email: str
    approved: bool
    status: str


# Generate Email
def generate_email(state):

    prompt = f"""
    Write a professional email.

    Topic: {state['topic']}
    Company Name: {state['company']}
    Sender Name: {state['sender']}
    Designation: {state['designation']}

    Do NOT use placeholders like [Company Name] or [Your Name].

    Generate a complete professional email.
    """

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    email = response.choices[0].message.content

    print("\nEMAIL DRAFT")
    print("=" * 50)
    print(email)

    return {
        "email": email,
        "status": "Draft Generated"
    }


# Human Approval
def approval(state: State):

    choice = input("\nApprove Email? (Y/N): ")

    return {
        "approved": choice.upper() == "Y"
    }


# Send Email
def send_email(state: State):

    print("\nSending Email...")
    print("\nEmail Sent Successfully!")

    return {
        "status": "Sent"
    }


# Reject Email
def reject_email(state: State):

    print("\nEmail Rejected.")

    return {
        "status": "Rejected"
    }


# Router
def route(state: State):

    if state["approved"]:
        return "send"

    return "reject"


# Build Graph
builder = StateGraph(State)

builder.add_node("generate_email", generate_email)
builder.add_node("approval", approval)
builder.add_node("send_email", send_email)
builder.add_node("reject_email", reject_email)

builder.add_edge(START, "generate_email")
builder.add_edge("generate_email", "approval")

builder.add_conditional_edges(
    "approval",
    route,
    {
        "send": "send_email",
        "reject": "reject_email"
    }
)

builder.add_edge("send_email", END)
builder.add_edge("reject_email", END)

graph = builder.compile()


# Run
topic = input("Enter Topic: ")
company = input("Enter Company Name: ")
sender = input("Enter Your Name: ")
designation = input("Enter Designation: ")

result = graph.invoke({
    "topic": topic,
    "company": company,
    "sender": sender,
    "designation": designation,
    "email": "",
    "approved": False,
    "status": ""
})

print("\nFinal Status:", result["status"])