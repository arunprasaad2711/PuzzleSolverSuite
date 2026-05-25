from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import omni, chess
import os

'''
To install, use uvicorn
To run this,
uvicorn main:app --host 127.0.0.1 --port 5500
'''

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    origins = ["https://arunprasaad2711.github.io"]
else:
    origins = ["http://127.0.0.1:5500", "http://localhost:5500"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/", tags=["Health"])
async def health_check():
    return {"message": "Puzzle Solver Suite API is running!"}

app.include_router(omni.router)
app.include_router(chess.router)

