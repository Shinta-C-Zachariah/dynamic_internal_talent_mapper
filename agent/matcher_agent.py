import json
from agent.llm_client import call_ollama

def score_match(project_text: str, employee_text: str) -> dict:
    prompt = f"""
You are an AI Talent Matching Agent.

PROJECT REQUIREMENTS:
{project_text}

EMPLOYEE PROFILE:
{employee_text}

Task:
- Identify skill match percentage
- Consider transferable skills
- Consider availability and location
- Provide match score between 0.0 and 1.0
- Provide missing skills
- Provide explanation

Return output strictly in JSON format like:

{{
  "match_score": 0.85,
  "strengths": ["...","..."],
  "missing_skills": ["..."],
  "transferable_skills_reasoning": "...",
  "final_recommendation": "Recommended/Not Recommended"
}}
"""

    response = call_ollama(prompt)

    try:
        # Sometimes model returns extra text, try to extract JSON
        start = response.find("{")
        end = response.rfind("}") + 1
        json_str = response[start:end]

        return json.loads(json_str)
    except Exception:
        return {
            "match_score": 0.0,
            "strengths": [],
            "missing_skills": [],
            "transferable_skills_reasoning": response,
            "final_recommendation": "Parsing Failed"
        }
