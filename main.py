from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Allow CORS (so React frontend can call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ResearchRequest(BaseModel):
    query: str

@app.post("/research")
async def research(request: ResearchRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(request.query)
        return {"query": request.query, "response": response.text}
    except Exception as e:
        return {"error": str(e)}
