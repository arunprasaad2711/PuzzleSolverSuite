from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from SolverManager import *
from InputJSONClass import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Enable this for production
        "https://arunprasaad2711.github.io",
        # Enable this for local testing
        # "http://127.0.0.1:5500", 
        # "http://localhost:5500",
        # "http://127.0.0.1:8000",  # Add this if needed
        # "http://localhost:8000"   # Add this if needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/")
async def health_check():
    return {"message": "OmniSolver API is running!"}

@app.post("/solve")
def solve_puzzle(puzzle: Omni):
    
    print(f"Attempting to use OmniSolver with data {puzzle}")
    
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
            

