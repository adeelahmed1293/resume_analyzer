# routes.py
from fastapi import APIRouter, UploadFile, File
from controllers import analyze_resume_controller , send_or_resume_chat , create_user_controller , get_user_threads_controller, get_chat_history_controller
from schemas import ChatRequest, User_data ,ChatResponse
from agent import run_graph_with_message
router = APIRouter()

@router.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)):
    result = await analyze_resume_controller(file)
    return result



@router.post("/chat")
def chat(request: ChatRequest):
    return send_or_resume_chat(request)




@router.post("/user/create")
def create_user(user: User_data):
    return create_user_controller(user)


@router.get("/chat/threads")
def get_user_threads(email: str):
    return get_user_threads_controller(email)


@router.get("/chat/history/{thread_id}")
def get_chat_history(thread_id: str, email: str):
    return get_chat_history_controller(thread_id, email)