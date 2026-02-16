import streamlit as st
import pandas as pd
from agent.orchestrator import find_best_matches, load_projects
from agent.feedback_agent import save_feedback

st.set_page_config(page_title="Dynamic Talent Mapper", layout="wide")

st.title("🚀 Dynamic Internal Talent Mapper (Agentic AI + Ollama)")

projects = load_projects()
project_ids = [p["project_id"] for p in projects]

selected_project = st.selectbox("Select Project", project_ids)

if st.button("🔍 Find Best Internal Talent"):
    with st.spinner("Matching talent using AI Agents..."):
        results = find_best_matches(selected_project, top_k=5)

    st.subheader("📌 Ranked Talent Recommendations")

    for idx, res in enumerate(results):
        match = res["llm_match_result"]
        score = match.get("match_score", 0)

        with st.expander(f"#{idx+1} Candidate: {res['emp_id']} | Score: {score}"):
            st.write("### Employee Profile")
            st.text(res["employee_profile"])

            st.write("### AI Reasoning Result")
            st.json(match)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Accept {res['emp_id']}", key=f"accept_{res['emp_id']}"):
                    save_feedback(selected_project, res["emp_id"], "Accepted", "Selected for project")
                    st.success("Feedback saved as Accepted")

            with col2:
                if st.button(f"❌ Reject {res['emp_id']}", key=f"reject_{res['emp_id']}"):
                    save_feedback(selected_project, res["emp_id"], "Rejected", "Not suitable")
                    st.warning("Feedback saved as Rejected")

st.subheader("📊 Feedback History")
try:
    feedback_df = pd.read_csv("data/feedback.csv")
    st.dataframe(feedback_df)
except:
    st.info("No feedback recorded yet.")
