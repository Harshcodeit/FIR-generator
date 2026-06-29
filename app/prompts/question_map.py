QUESTION_MAP = {
    "offence_date": {
        "question": "On what date did the incident occur?",
        "type": "date",
        "required": True
    },
    "offence_time": {
        "question": "At approximately what time did the incident occur?",
        "type": "time",
        "required": True
    },
    "location_name": {
        "question": "Where exactly did the incident occur?",
        "type": "text",
        "required": True
    },
    "landmark": {
        "question": "Was there any nearby landmark that could help identify the location?",
        "type": "text",
        "required": False
    },
    "city": {
        "question": "In which city did the incident occur?",
        "type": "text",
        "required": True
    },
    "state": {
        "question": "In which state did the incident occur?",
        "type": "text",
        "required": True
    },
    "reporter_full_name": {
        "question": "Please tell me your full name.",
        "type": "text",
        "required": True
    },
    "father_or_husband_name": {
        "question": "Please provide your father's or husband's name.",
        "type": "text",
        "required": False
    },
    "dob": {
        "question": "What is your date of birth?",
        "type": "date",
        "required": False
    },
    "nationality": {
        "question": "What is your nationality?",
        "type": "text",
        "required": False
    },
    "occupation": {
        "question": "What is your occupation?",
        "type": "text",
        "required": True
    },
    "address": {
        "question": "What is your current residential address?",
        "type": "text",
        "required": True
    },
    "phone_number": {
        "question": "What is your contact phone number?",
        "type": "phone",
        "required": True
    },
    "delay_reason": {
        "question": "If there was any delay in reporting the incident, please explain the reason.",
        "type": "text",
        "required": False
    },
    "accused_description": {
        "question": "Do you know anything about the accused person? Please describe them if possible.",
        "type": "text",
        "required": False
    },
    "property_type": {
        "question": "What property was stolen or involved in the incident?",
        "type": "text",
        "required": True
    },
    "estimated_value": {
        "question": "What is the approximate value of the property (in ₹)?",
        "type": "number",
        "required": False
    }
}