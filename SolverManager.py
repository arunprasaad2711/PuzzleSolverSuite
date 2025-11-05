from OmniSolver.OmniPuzzleSolver import OmniPuzzleSolver
from NQueens.NQueensSolver import NQueens
from PocketCube.PocketCubeSolver import PocketCubeSolver

from InputJSONClass import Omni, Chess, PocketCube

def OmniSolverManager(puzzle: Omni):
    
    print(f"Inside OmniSolverManager with data {puzzle}")
    
    Solver = OmniPuzzleSolver(puzzle)
    
    if puzzle.Sudoku:
        Solver.ClassicSudokuConstraints()
        
    if puzzle.AntiKing:
        Solver.AntiKingConstraints()
    
    if puzzle.AntiKnight:
        Solver.AntiKnightConstraints()
    
    if puzzle.OrthogonalNonConsec:
        Solver.OrthogonalNonConsecConstraints()
        
    # Solutions = Solver.MultiSolutionSolve()
    Solutions = Solver.Solve()
    
    return Solutions

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

# def PocketCubeSolverManager(puzzle: PocketCube):
    
#     Solver = PocketCubeSolver()
    
#     Depth, Scramble, Solution = Solver.Solve(puzzle.Hashes)
    
#     return Depth, Scramble, Solution