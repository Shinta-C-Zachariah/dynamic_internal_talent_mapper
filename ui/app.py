import streamlit as st
import pandas as pd
from agent.orchestrator import find_best_matches, load_projects
from agent.feedback_agent import save_feedback, feedback_exists

st.set_page_config(page_title="Dynamic Talent Mapper", layout="wide")

st.title("🚀 Dynamic Internal Talent Mapper (Agentic AI + Ollama)")

projects = load_projects()
project_ids = [p["project_id"] for p in projects]

selected_project = st.selectbox("📌 Select Project", project_ids)

# Let user choose how many candidates
top_k = st.slider("Number of candidates to rank", min_value=1, max_value=10, value=5)

# Cache results to avoid repeated Ollama calls
@st.cache_data(show_spinner=False)
def cached_match_results(project_id, top_k):
    return find_best_matches(project_id, top_k=top_k)

# Session state
if "results" not in st.session_state:
    st.session_state["results"] = None

if "last_project" not in st.session_state:
    st.session_state["last_project"] = None

# Button to find candidates
if st.button("🔍 Find Best Internal Talent"):
    with st.spinner("Matching talent using AI Agents... Please wait"):
        st.session_state["results"] = cached_match_results(selected_project, top_k)
        st.session_state["last_project"] = selected_project

# Show ranking results
if st.session_state["results"] is not None:
    st.subheader(f"📌 Ranked Talent Recommendations for {st.session_state['last_project']}")

    results = st.session_state["results"]

    for idx, res in enumerate(results):
        match = res["llm_match_result"]
        score = match.get("match_score", 0)

        with st.expander(f"#{idx+1} Candidate: {res['emp_id']} | Match Score: {score}"):
            st.write("### 👤 Employee Profile")
            st.text(res["employee_profile"])

            st.write("### 🤖 AI Match Reasoning")
            st.json(match)

            # If feedback already exists, disable buttons
            already_given = feedback_exists(st.session_state["last_project"], res["emp_id"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    f"✅ Accept {res['emp_id']}",
                    key=f"accept_{res['emp_id']}",
                    disabled=already_given
                ):
                    save_feedback(
                        st.session_state["last_project"],
                        res["emp_id"],
                        "Accepted",
                        "Selected for project"
                    )
                    st.success("Feedback saved as Accepted ✅")
                    st.rerun()

            with col2:
                if st.button(
                    f"❌ Reject {res['emp_id']}",
                    key=f"reject_{res['emp_id']}",
                    disabled=already_given
                ):
                    save_feedback(
                        st.session_state["last_project"],
                        res["emp_id"],
                        "Rejected",
                        "Not suitable"
                    )
                    st.warning("Feedback saved as Rejected ❌")
                    st.rerun()

            if already_given:
                st.info("Feedback already recorded for this employee in this project.")

# Feedback history
st.subheader("📊 Feedback History")

try:
    feedback_df = pd.read_csv("data/feedback.csv")

    if feedback_df.empty:
        st.info("No feedback recorded yet. Click Accept/Reject to add feedback.")
    else:
        st.dataframe(feedback_df, use_container_width=True)

except Exception as e:
    st.error(f"Unable to load feedback file: {e}")
