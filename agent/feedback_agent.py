import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "data/feedback.csv"


def feedback_exists(project_id, emp_id):
    try:
        df = pd.read_csv(FEEDBACK_FILE)

        if df.empty:
            return False

        existing = df[(df["project_id"] == project_id) & (df["emp_id"] == emp_id)]
        return not existing.empty

    except FileNotFoundError:
        return False


def save_feedback(project_id, emp_id, decision, comments=""):
    try:
        df = pd.read_csv(FEEDBACK_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "project_id", "emp_id", "decision", "comments"])

    # Prevent duplicate entries
    existing = df[(df["project_id"] == project_id) & (df["emp_id"] == emp_id)]
    if not existing.empty:
        return  # Already exists, do not insert again

    new_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": project_id,
        "emp_id": emp_id,
        "decision": decision,
        "comments": comments
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)
