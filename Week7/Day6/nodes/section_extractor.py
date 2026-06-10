from state import ResumeFormatter
from tools.section_parser import extract_sections

def section_extractor(state: ResumeFormatter):

    extracted = extract_sections(
    state["cleaned_resume"]
    )

    return extracted