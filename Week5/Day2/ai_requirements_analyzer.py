from __future__ import annotations

import asyncio
import json
from typing import List, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class UserStory(BaseModel):
    title: str = Field(description="Short user story title")
    description: str = Field(description="User story in 'As a... I want... so that...' format")
    priority: Literal["Low", "Medium", "High", "Critical"]


class TaskItem(BaseModel):
    title: str
    details: str
    priority: Literal["Low", "Medium", "High", "Critical"]


class AnalysisResult(BaseModel):
    summary: str
    user_stories: List[UserStory]
    tasks: List[TaskItem]
    priority_order: List[str]


class SimpleConversationMemory:
    def __init__(self) -> None:
        self._messages: List[str] = []

    def load_memory_variables(self, _: dict) -> dict:
        return {"history": "\n".join(self._messages)}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        user_text = inputs.get("input", "")
        assistant_text = outputs.get("output", "")
        self._messages.append(f"User: {user_text}")
        self._messages.append(f"Assistant: {assistant_text}")


class RequirementsAnalyzer:
    def __init__(self, model_name: str = "qwen2.5:1.5b") -> None:
        self.llm = ChatOllama(model=model_name, temperature=0.2)
        self.memory = SimpleConversationMemory()

        self.analysis_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a simple AI requirements analyzer. Extract clear user stories, tasks, and priorities from product requirements.",
                ),
                (
                    "human",
                    "Conversation context:\n{history}\n\nRequirement text:\n{requirement_text}\n\nReturn a concise analysis.",
                ),
            ]
        )

        self.story_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Create 3 to 5 short user stories from the requirement text.",
                ),
                (
                    "human",
                    "Requirement text:\n{requirement_text}",
                ),
            ]
        )

        self.task_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Turn the user stories into a small implementation task list.",
                ),
                (
                    "human",
                    "User stories:\n{user_stories}",
                ),
            ]
        )

        self.priority_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Rank the requirements from most important to least important.",
                ),
                (
                    "human",
                    "Requirement text:\n{requirement_text}",
                ),
            ]
        )

        self.analysis_chain = self.analysis_prompt | self.llm
        self.story_chain = self.story_prompt | self.llm
        self.task_chain = self.task_prompt | self.llm
        self.priority_chain = self.priority_prompt | self.llm

    def _load_history(self) -> str:
        return self.memory.load_memory_variables({}).get("history", "")

    def _save_turn(self, requirement_text: str, result: AnalysisResult) -> None:
        self.memory.save_context(
            {"input": requirement_text},
            {"output": result.model_dump_json(indent=2)},
        )

    def _fallback(self, requirement_text: str) -> AnalysisResult:
        keywords = [word.strip(".,:;!? ") for word in requirement_text.split()[:5]]
        stories = [
            UserStory(
                title="Capture requirement",
                description="As a product owner, I want the requirement captured so that the team can plan the work.",
                priority="High",
            ),
            UserStory(
                title="Break into user stories",
                description="As a developer, I want the requirement split into user stories so that implementation is clearer.",
                priority="Medium",
            ),
        ]
        tasks = [
            TaskItem(
                title="Review requirement text",
                details="Read the uploaded requirement and note the main features.",
                priority="High",
            ),
            TaskItem(
                title="Create implementation checklist",
                details="List the smallest steps needed to build the feature.",
                priority="Medium",
            ),
        ]
        return AnalysisResult(
            summary="Simple fallback analysis for the given requirement text.",
            user_stories=stories,
            tasks=tasks,
            priority_order=keywords or ["Requirement review", "User story creation", "Task planning"],
        )

    def _is_clarifying(self, text: str) -> bool:
        if not text:
            return True
        lt = text.lower()
        indicators = [
            "please provide",
            "i need",
            "could you",
            "please share",
            "need you to provide",
            "i'm sorry",
            "i need you",
            "please provide the",
        ]
        if any(ind in lt for ind in indicators):
            return True
        # treat short replies that look like questions as clarifying
        if lt.strip().endswith("?"):
            return True
        return False

    def _auto_tasks_from_text(self, requirement_text: str) -> List[TaskItem]:
        pieces = [p.strip() for p in requirement_text.replace("\n", " ").split(".")]
        items: List[TaskItem] = []
        for i, p in enumerate(pieces):
            if not p:
                continue
            items.append(
                TaskItem(title=f"Task {i+1}", details=p[:200], priority="Medium")
            )
            if len(items) >= 4:
                break
        if not items:
            items = [
                TaskItem(title="Review requirement", details="Read and clarify the requirement.", priority="High"),
                TaskItem(title="Draft user stories", details="Create 2-4 user stories.", priority="Medium"),
            ]
        return items

    def analyze(self, requirement_text: str) -> AnalysisResult:
        history = self._load_history()

        try:
            analysis_text = self.analysis_chain.invoke(
                {"history": history, "requirement_text": requirement_text}
            )
            stories_text = self.story_chain.invoke({"requirement_text": requirement_text})
            tasks_text = self.task_chain.invoke({"user_stories": stories_text.content})
            priority_text = self.priority_chain.invoke({"requirement_text": requirement_text})

            result = AnalysisResult(
                summary=analysis_text.content.strip(),
                user_stories=(
                    [
                        UserStory(
                            title="Extracted story 1",
                            description=stories_text.content.strip(),
                            priority="High",
                        )
                    ]
                    if not self._is_clarifying(stories_text.content)
                    else self._fallback(requirement_text).user_stories
                ),
                tasks=(
                    [
                        TaskItem(
                            title="Generated task 1",
                            details=tasks_text.content.strip(),
                            priority="Medium",
                        )
                    ]
                    if not self._is_clarifying(tasks_text.content)
                    else self._auto_tasks_from_text(requirement_text)
                ),
                priority_order=[line.strip("- ") for line in priority_text.content.splitlines() if line.strip()],
            )
        except Exception:
            result = self._fallback(requirement_text)

        self._save_turn(requirement_text, result)
        return result

    async def analyze_async(self, requirement_text: str) -> AnalysisResult:
        history = self._load_history()

        try:
            analysis_task = self.analysis_chain.ainvoke(
                {"history": history, "requirement_text": requirement_text}
            )
            stories_task = self.story_chain.ainvoke({"requirement_text": requirement_text})
            tasks_task = self.task_chain.ainvoke({"user_stories": requirement_text})
            priority_task = self.priority_chain.ainvoke({"requirement_text": requirement_text})

            analysis_text, stories_text, tasks_text, priority_text = await asyncio.gather(
                analysis_task,
                stories_task,
                tasks_task,
                priority_task,
            )

            result = AnalysisResult(
                summary=analysis_text.content.strip(),
                user_stories=(
                    [
                        UserStory(
                            title="Extracted story 1",
                            description=stories_text.content.strip(),
                            priority="High",
                        )
                    ]
                    if not self._is_clarifying(stories_text.content)
                    else self._fallback(requirement_text).user_stories
                ),
                tasks=(
                    [
                        TaskItem(
                            title="Generated task 1",
                            details=tasks_text.content.strip(),
                            priority="Medium",
                        )
                    ]
                    if not self._is_clarifying(tasks_text.content)
                    else self._auto_tasks_from_text(requirement_text)
                ),
                priority_order=[line.strip("- ") for line in priority_text.content.splitlines() if line.strip()],
            )
        except Exception:
            result = self._fallback(requirement_text)

        self._save_turn(requirement_text, result)
        return result


def upload_requirement_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def main() -> None:
    analyzer = RequirementsAnalyzer()

    requirement_text = input("Paste requirement text or enter a file path: ").strip()
    if requirement_text.lower().endswith(".txt"):
        requirement_text = upload_requirement_text(requirement_text)

    result = asyncio.run(analyzer.analyze_async(requirement_text))
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()