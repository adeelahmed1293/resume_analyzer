# controllers.py
import os
from langchain_community.document_loaders import PyPDFLoader
from fastapi import UploadFile
from config import llm , user_collection
from schemas import ResumeAnalysis, ChatRequest , ChatHistoryResponse, UserThreadsResponse
from langchain.messages import  HumanMessage, SystemMessage
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import uuid
import time
from agent import load_conversation, graph, run_graph_with_message
from fastapi import HTTPException
from schemas import User_data
from config import user_collection


# Create structured agent
resume_agent = llm.with_structured_output(ResumeAnalysis)

async def analyze_resume_controller(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    # Save PDF temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # Load PDF content
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    resume_text = "".join([doc.page_content for doc in docs])

    # Prepare prompt
    prompt = f"""
You are an AI resume evaluator.
Perform a strict, evidence-based analysis of the provided resume.

Evaluate ONLY these categories:
Skills
Experience
Education & Certifications
Projects
Resume Structure & Formatting (ATS-friendly, 1–2 pages)
Language Quality
ATS Keyword Match
Contact & Profile Info


Scoring Rules:
Assign a 0–100 score for each category and an overall score
Base scores only on resume content
Do not assume or infer missing information
Deduct points for missing metrics, vague content, poor formatting, or ATS issues
Output ONLY these sections (no extra text):
Overall Resume Score (0–100)
Category-wise Scores
Strengths (bullet points)
Improvements Needed (bullet points)
Actionable Suggestions (short and specific)

Constraints:
No explanations, no motivation, no repetition
Bullet points must be factual and concise
Follow instructions exactly.

Here is the Info of the resume:
{resume_text}
"""

    # Invoke LLM agent
    result = resume_agent.invoke(prompt)

    # Remove temporary file
    os.remove(temp_file_path)
    return result



def send_or_resume_chat(request: ChatRequest):
    try:
        # 1️⃣ Check user by email
        user = user_collection.find_one({"email": request.email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2️⃣ Thread ID MUST be provided
        if not request.thread_id:
            raise HTTPException(
                status_code=400,
                detail="thread_id is required"
            )

        thread_id = request.thread_id

        # 3️⃣ Check thread in user's thread list
        if thread_id not in user.get("thread_ids", []):
            user_collection.update_one(
                {"_id": user["_id"]},
                {"$addToSet": {"thread_ids": thread_id}}
            )

        # 4️⃣ Empty message safeguard
        if not request.message.strip():
            return {
                "thread_id": thread_id,
                "response": ""
            }

        # 5️⃣ Run graph
        answer = run_graph_with_message(thread_id, request.message)

        # 6️⃣ Return response
        return {
            "thread_id": thread_id,
            "response": answer
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in send_or_resume_chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")





def get_chat_history_controller(thread_id: str, email: str):
    """
    Fetch full conversation history for a given thread_id
    """
    user = user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if thread_id not in user.get("thread_ids", []):
        raise HTTPException(status_code=404, detail="Thread ID not found for this user")

    messages = load_conversation(thread_id)

    return ChatHistoryResponse(
        thread_id=thread_id,
        messages=messages
    )


def get_user_threads_controller(email: str):
    """
    Fetch all thread IDs for a user
    """
    user = user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserThreadsResponse(
        thread_ids=user.get("thread_ids", [])
    )



  # adjust import

def create_user_controller(user: User_data):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user_collection.insert_one(user.model_dump())

    return {
        "message": "User created successfully",
        "email": user.email
    }
