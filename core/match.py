import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY", "dummy-key")

def score_job(description):
    prompt = f"""
Rate this job from 0 to 10 based on how well it fits me:
##
MY SKILLS: Python, Cybersecurity, Helpdesk, GPT, APIs
##
JOB DESCRIPTION:
{description}
##
Just give a number 0-10:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    score = response['choices'][0]['message']['content']
    return score
