from fastapi import APIRouter
from managers.OmniSolverManager import OmniSolverManager
from models.OmniSolverInputJSONClass import Omni

router = APIRouter(prefix="/solve", tags=["Omni Solver"])

@router.post("")
def solve_puzzle(puzzle: Omni):
    try:
        Solutions = OmniSolverManager(puzzle)

        # Check if solutions were found
        if Solutions and len(Solutions) > 0:
            return {"success": True, "solutions": Solutions}
        
        return {"success": False, "solutions": [], "message": "No solutions found"}
    
    except Exception as e:
        return {"success": False, "solutions": [], "message": f"Error solving puzzle: {str(e)}"}