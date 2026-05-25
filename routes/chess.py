from fastapi import APIRouter
from managers.ChessSolverManager import ChessSolverManager
from models.ChessSolverInputJSONClass import Chess

router = APIRouter(prefix="/nqueens", tags=["Chess Solver"])

@router.post("")
def solve_chess(puzzle: Chess):
    
    try:
        Solutions = ChessSolverManager(puzzle)
        
        # Check if solutions were found
        if Solutions and len(Solutions) > 0:
            return { "success": True, "solutions": Solutions}
        return {"success": False, "solutions": [], "message": "No solutions found" }
            
    except Exception as e:
        return { "success": False, "solutions": [], "message": f"Error solving puzzle: {str(e)}" }