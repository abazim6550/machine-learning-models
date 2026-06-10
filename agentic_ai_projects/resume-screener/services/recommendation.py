
import ollama
import json

def generate_recommendation(jd, resume):
    
    user_prompt = f"""
    Job Description:
    {jd}
    Resume:
    {resume}
    Analyze the resume against the JD.

    Scoring:
    - Skills Match = 40%
    - Experience Match = 30%
    - Education Match = 10%
    - Domain Knowledge = 10%
    - Certifications = 10%

    Categories:
    80-100 = Best Fit
    60-79 = Average Fit
    0-59 = Not Fit

    Return ONLY valid JSON:
        Do not include:
    - explanations
    - markdown
    - code fences
    - extra text
    {{
    "candidate_name":"",
    "match_percentage":0,
    "matching_skills":[],
    "missing_skills":[],
    "recommendation":""
    }}
    """

    system_prompt = """
    You are an expert technical recruiter. Compare resume against job description. Skills 40%, Experience 30%, Education 10%, Domain 10%, Certifications 10%. Return JSON with candidate_name, match_percentage, matching_skills, missing_skills, experience_summary, education_summary, recommendation and reason.
    """

    messages= [{
        'role' : 'system',
        'content': system_prompt
    },
    {
        'role' : 'user',
        'content': user_prompt
    }
    ]

    print("ollama model triggered")

    response = ollama.chat(
        model= 'gemma:2b',
        messages= messages
    )

    print("returned message", response.message.content)
    mesagge =  json.loads(response.message.content)

    if mesagge['match_percentage'] > 80:
        mesagge['result'] = 'Best Fit'
    elif mesagge['match_percentage'] < 80 and mesagge['match_percentage'] >= 60:   
        mesagge['result'] = 'Average Fit'
    elif mesagge['match_percentage'] < 60:   
        mesagge['result'] = 'Not Fit' 

    return mesagge

#if __name__ == '__main__':
   # generate_recommendation()    