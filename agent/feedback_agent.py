import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "data/feedback.csv"

def save_feedback(project_id, emp_id, decision, comments=""):
    df = pd.read_csv(FEEDBACK_FILE)

    new_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": project_id,
        "emp_id": emp_id,
        "decision": decision,
        "comments": comments
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)
