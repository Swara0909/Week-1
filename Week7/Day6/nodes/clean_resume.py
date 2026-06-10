from state import ResumeFormatter
from tools.regex_cleaner import clean_text

def cleaner(state:ResumeFormatter):
    cleaned=clean_text(state["raw_resume"])

    return{
        "cleaned_resume": cleaned
    }