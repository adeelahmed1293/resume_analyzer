# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as resume_router

app = FastAPI(title="Resume Analysis API")

# ✅ Allow all origins, ports, and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all domains & ports
    allow_credentials=True,
    allow_methods=["*"],      # allow all HTTP methods
    allow_headers=["*"],      # allow all headers
)

# Include routes
app.include_router(resume_router)
