from app.services.extraction import extract_information
from app.prompts.question_map import QUESTION_MAP

from app.schemas.user_report import UserReportSchema

from app.utils.helpers import get_missing_fields

from rich import print

def fill_missing_information(report) : 
    data = report.model_dump()
    missing_fields = get_missing_fields(report)
    if missing_fields == []:
        return report
    missing_field = missing_fields[0]

    answer = input(f"{QUESTION_MAP[missing_field]['question']}\n")

    data[missing_field] = answer

    report = UserReportSchema(**data) # unpack dict as keyword parameters

    return report

# testing 
from app.services.extraction import extract_information

report = extract_information("My bike got stolen near Akash deep enclave")
print("===========================before filling missing information=====================")
print(report)

while get_missing_fields(report) : 
    report = fill_missing_information(report)

print("===========================after filling missing information=====================")
print(report)
