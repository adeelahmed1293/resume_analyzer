# Resume Analysis API Backend

A FastAPI-based backend service for resume analysis and conversational AI chat functionality. This API allows users to upload resumes for detailed analysis and engage in threaded conversations with an AI assistant.

## Features

- **Resume Analysis**: Upload PDF resumes and receive comprehensive analysis including:
  - Overall and category-wise scores (0-100)
  - Key strengths and areas for improvement
  - Actionable suggestions for enhancement
  - ATS-friendly evaluation

- **Conversational AI**: Thread-based chat system powered by LangGraph and Groq LLM
  - Persistent conversation history
  - User-specific thread management
  - Context-aware responses

- **User Management**: Basic user creation and thread tracking
- **CORS Enabled**: Supports cross-origin requests for frontend integration

## Tech Stack

- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph, Groq LLM
- **Database**: MongoDB (for user data and conversation persistence)
- **PDF Processing**: PyPDFLoader
- **Validation**: Pydantic
- **Deployment**: Vercel

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd app-backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   MONGODB_URI=your_mongodb_connection_string
   ```

## Running the Application

### Development
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Resume Analysis
- **POST** `/analyze_resume`
  - Upload a PDF resume for analysis
  - Returns: Structured analysis with scores, strengths, and suggestions

### Chat System
- **POST** `/chat`
  - Send a message in a conversation thread
  - Requires: `message`, `email`, `thread_id`
  - Returns: AI response with thread ID

- **GET** `/chat/threads`
  - Get all thread IDs for a user
  - Query param: `email`
  - Returns: List of thread IDs

- **GET** `/chat/history/{thread_id}`
  - Get conversation history for a specific thread
  - Query params: `thread_id`, `email`
  - Returns: Paired human-AI messages

### User Management
- **POST** `/user/create`
  - Create a new user
  - Body: `{"email": "user@example.com"}`
  - Returns: Success message

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Deployment

This application is configured for deployment on Vercel:

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

## Project Structure

```
app-backend/
├── main.py              # FastAPI application entry point
├── routes.py            # API route definitions
├── controllers.py       # Business logic for endpoints
├── schemas.py           # Pydantic models for requests/responses
├── agent.py             # LangGraph agent for chat functionality
├── config.py            # Configuration (LLM, database connections)
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment configuration
└── Notebooks/           # Jupyter notebooks for development/testing
```

## Environment Variables

- `GROQ_API_KEY`: API key for Groq LLM service
- `MONGODB_URI`: MongoDB connection string for data persistence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


