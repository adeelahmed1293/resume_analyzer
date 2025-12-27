# config.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    streaming=True,
    temperature=0.3,
    max_tokens=500,
)

# Get MONGO_URI from environment
mongo_uri = os.getenv("MONGO_URL")

client = MongoClient(mongo_uri)
checkpointer = MongoDBSaver(client)

db = client["app_project"]
user_collection = db["users"]
