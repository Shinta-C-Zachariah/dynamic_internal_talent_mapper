def build_employee_text(row: dict) -> str:
    return f"""
Employee ID: {row['emp_id']}
Name: {row['name']}
Role: {row['role']}
Location: {row['location']}
Experience: {row['experience_years']} years
Availability: {row['availability']}
Skills: {row['skills']}
Projects Summary: {row['projects_summary']}
""".strip()
