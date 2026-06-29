def get_missing_fields(report):
    return [
        field
        for field,value in report.model_dump().items()
        if value is None
    ]