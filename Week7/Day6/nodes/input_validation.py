from state import ResumeFormatter

def input_validator(state: ResumeFormatter):

    if not state["raw_resume"]:
        raise ValueError("Resume cannot be empty")

    return {}