# core/ai_evaluator.py
import os
import json
from google import genai
from pydantic import BaseModel
from config.prompts import SYSTEM_PROMPT


# 1. สร้าง Class ย่อยสำหรับ "scores"

class Scores(BaseModel):
    communication: int
    relevance: int
    quality: int
    total: int


# 2. สร้าง Class ย่อยสำหรับ "feedback"

class Feedback(BaseModel):
    strengths: str
    weaknesses: str
    summary: str


# 3. สร้าง Class หลักที่รวมทุกอย่างเข้าด้วยกัน

class MyResponse(BaseModel):
    scores: Scores          # เรียกใช้ Class Scores
    feedback: Feedback      # เรียกใช้ Class Feedback
    pass_prediction: bool


def evaluate_candidate(api_key, question, transcript):
    """
    Evaluate a candidate's transcript based on a given question.

    Args:
        api_key (str): Google API Key
        question (str): Question to evaluate the transcript against
        transcript (str): Transcript to evaluate

    Returns:
        MyResponse: Evaluation result

    Raises:
        Exception: If an error occurs during evaluation
    """
    # Setup Google Gemini
    client = genai.Client(api_key=api_key)

    # เตรียม Prompt
    final_prompt = SYSTEM_PROMPT.format(question=question, answer=transcript)
    print("*" * 50)
    print("Prompt :", final_prompt)
    print("*" * 50)

    # LLM
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": MyResponse,  # <-- ใส่ Schema ตรงนี้
                "temperature": 0.2,
            })
        return response.parsed
    except Exception as e:
        return {"error": str(e)}


# ---- Gemini ----
# # โหลด API Key
# from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")

# from google import genai

# client = genai.Client()

# myfile = client.files.upload(file=r"D:\ai-interview\temp_audio.mp3")
# # prompt = "ถอดความสิ่งที่ผู้สมัครพูดออกมาให้ครบถ้วน"
# prompt = 'Generate a transcript of the speech.'
# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents=[prompt, myfile]
# )

# print(response.text)
