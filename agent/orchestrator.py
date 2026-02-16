import pandas as pd
from agent.profile_agent import build_employee_text
from agent.project_agent import build_project_text
from agent.embedding_store import TalentVectorStore
from agent.matcher_agent import score_match

EMPLOYEE_FILE = "data/employees.csv"
PROJECT_FILE = "data/projects.csv"

def load_employees():
    df = pd.read_csv(EMPLOYEE_FILE)
    return df.to_dict(orient="records")

def load_projects():
    df = pd.read_csv(PROJECT_FILE)
    return df.to_dict(orient="records")

def get_project_by_id(project_id):
    projects = load_projects()
    for p in projects:
        if p["project_id"] == project_id:
            return p
    return None

def build_vector_db():
    store = TalentVectorStore()
    employees = load_employees()

    for emp in employees:
        text = build_employee_text(emp)
        store.add_employee(emp["emp_id"], text)

    return store

def find_best_matches(project_id, top_k=5):
    store = TalentVectorStore()

    project = get_project_by_id(project_id)
    if not project:
        raise ValueError("Invalid project ID")

    project_text = build_project_text(project)

    retrieved = store.query(project_text, top_k=top_k)

    ranked_results = []
    for emp_id, emp_text in zip(retrieved["ids"][0], retrieved["documents"][0]):
        llm_result = score_match(project_text, emp_text)
        ranked_results.append({
            "emp_id": emp_id,
            "employee_profile": emp_text,
            "llm_match_result": llm_result
        })

    ranked_results = sorted(
        ranked_results,
        key=lambda x: x["llm_match_result"].get("match_score", 0),
        reverse=True
    )

    return ranked_results
