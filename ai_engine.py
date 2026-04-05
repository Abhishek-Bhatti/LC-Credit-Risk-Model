import re

def get_ai_character_assessment(client, purpose, score, dti, amt, emp_length):
    """
    Evaluates qualitative risk, financial context, and job stability.
    """
    prompt = f"""
    EXPERT LOAN OFFICER ASSESSMENT
    
    Applicant Profile:
    - Employment Tenure: {emp_length}
    - Requested Amount: ${amt:,}
    - Risk Score: {score}
    - Debt-to-Income: {dti}%
    - Loan Purpose: '{purpose}'
    TASK: 
    Evaluate the 'Character & Stability' risk. Check if the purpose of the loan is acceptable given the rest of the applicant's profile. A short employment length combined with high loan amounts or low risk scores should be scrutinized heavily. 
    
    Provide a 'Character Score' (0-100). Return ONLY in this format:
    SCORE: [number]
    REASON: [text]
    """
    
    # ... (Rest of your Groq calling logic)
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_resp = completion.choices[0].message.content
    
    # Robust Parsing & Clamping
    score_match = re.search(r'\d+', ai_resp)
    if score_match:
        raw_score = int(score_match.group())
        ai_score = max(0, min(100, raw_score)) / 100
    else:
        ai_score = 0.5
        
    ai_reason = ai_resp.split('REASON:')[-1].strip() if 'REASON:' in ai_resp else ai_resp
    return ai_score, ai_reason