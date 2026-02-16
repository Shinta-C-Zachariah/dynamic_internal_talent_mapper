def build_project_text(row: dict) -> str:
    return f"""
Project ID: {row['project_id']}
Project Name: {row['project_name']}
Description: {row['description']}
Domain: {row['domain']}
Priority: {row['priority']}
Location: {row['location']}
Required Skills: {row['required_skills']}
Good to Have: {row['good_to_have_skills']}
""".strip()
