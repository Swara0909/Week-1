from state import ResumeFormatter

def summary_generator(state: ResumeFormatter):

    summary = (
        f"{state['name']} has experience in "
        f"{state['experience']}. "
        f"Key skills include "
        f"{', '.join(state['skills'])}."
    )

    return {
        "summary": summary
    }