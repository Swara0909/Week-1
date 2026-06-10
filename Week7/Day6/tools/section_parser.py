import re

def extract_sections(text: str):

    lines = text.split(",")

    name = text.split()[0] + " " + text.split()[1]

    skills_match = re.search(r"Skills:(.*?)Experience:", text)

    experience_match = re.search(r"Experience:(.*)", text)

    skills = []

    if skills_match:
        skills = [
            skill.strip()
            for skill in skills_match.group(1).split(",")
        ]

    experience = ""

    if experience_match:
        experience = experience_match.group(1).strip()

    return {
        "name": name,
        "skills": skills,
        "experience": experience
    }