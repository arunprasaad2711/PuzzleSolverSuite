from solvers.NQueens.NQueensSolver import NQueens
from models.ChessSolverInputJSONClass import Chess

def ChessSolverManager(puzzle: Chess):
    
    Solver = NQueens(puzzle)
    
    if puzzle.NBishops:
        Solver.NBishopsConstraint(puzzle.NBishopsRowConstraint)
    
    if puzzle.NRooks:
        Solver.NRooksConstraint()
    
    if puzzle.NQueens:
        Solver.NQueensConstraint()
    
    Solutions = Solver.Solve()
    
    return Solutions