from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from SolverManager import *
from InputJSONClass import *
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

@app.get(path="/")
async def health_check():
    return {"message": "OmniSolver API is running!"}

@app.post("/solve")
def solve_puzzle(puzzle: Omni):
    
    # print(f"Attempting to use OmniSolver with data {puzzle}")
    
    try:
        Solutions = OmniSolverManager(puzzle)
        
        # Check if solutions were found
        if Solutions and len(Solutions) > 0:
            return {
                "success": True,
                "solutions": Solutions
            }
        else:
            return {
                "success": False,
                "solutions": [],
                "message": "No solutions found"
            }
            
    except Exception as e:
        return {
            "success": False,
            "solutions": [],
            "message": f"Error solving puzzle: {str(e)}"
        }

@app.post("/nqueens")
def solve_chess(puzzle: Chess):
    
    try:
        Solutions = ChessSolverManager(puzzle)
        
        # Check if solutions were found
        if Solutions and len(Solutions) > 0:
            return {
                "success": True,
                "solutions": Solutions
            }
        else:
            return {
                "success": False,
                "solutions": [],
                "message": "No solutions found"
            }
            
    except Exception as e:
        return {
            "success": False,
            "solutions": [],
            "message": f"Error solving puzzle: {str(e)}"
        }
        
# @app.post("/pocketcube")
# def solve_pocket_cube(puzzle: PocketCube):
    
#     try:
#         Depth, Scramble, Solution = PocketCubeSolverManager(puzzle)
        
#         if Depth == -1:
#             return {
#                 "success": False,
#                 "solutions": [],
#                 "message": "No solutions found"
#             }
#         elif Depth >=0 :
#             return {
#                 "success": True,
#                 "depth": Depth,
#                 "scramble": Scramble,
#                 "solution": Solution
#             }
#     except Exception as e:
#         return {
#             "success": False,
#             "solutions": [],
#             "message": f"Error solving puzzle: {str(e)}"
#         }
            

