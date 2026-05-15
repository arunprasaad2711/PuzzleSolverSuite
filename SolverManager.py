from OmniSolver.OmniPuzzleSolver import OmniPuzzleSolver
from NQueens.NQueensSolver import NQueens
from PocketCube.PocketCubeSolver import PocketCubeSolver

from InputJSONClass import Omni, Chess, PocketCube

def OmniSolverManager(puzzle: Omni):
    
    # print(f"Inside OmniSolverManager with data {puzzle}")
    
    Solver = OmniPuzzleSolver(puzzle)
    
    if puzzle.Sudoku:
        Solver.ClassicSudokuConstraints()
    
    if puzzle.ArgyleSudoku:
        Solver.ArgyleConstraints()
    
    if puzzle.GirandolaSudoku:
        Solver.GirandolaConstraints()
    
    if puzzle.CentreDotSudoku:
        Solver.CentreDotConstraints()
    
    if puzzle.AsteriskSudoku:
        Solver.AsteriskConstraints()
    
    if puzzle.IrregularSudoku:
        Solver.SudokuRowConstraints()
        Solver.SudokuColConstraints()
        Solver.SudokuCustomGridConstraints(puzzle.IrregularSudokuRegionMap)
        Solver.InitializeGivenEntries()
        
    if puzzle.AntiKing:
        Solver.AntiKingConstraints()
    
    if puzzle.AntiKnight:
        Solver.AntiKnightConstraints()
    
    if puzzle.OrthogonalNonConsec:
        Solver.OrthogonalNonConsecConstraints()
    
    if puzzle.DiagonalNonConsec:
        Solver.DiagonalNonConsecConstraints()
    
    if puzzle.OrthogonalMinDifference:
        Solver.OrthogonalMinDifferenceConstraints(puzzle.OrthogonalMinDifferenceValue)
    
    if puzzle.DiagonalMinDifference:
        Solver.DiagonalMinDifferenceConstraints(puzzle.DiagonalMinDifferenceValue)
    
    if puzzle.ArrowSumSudoku:
        Solver.ArrowSum(puzzle.ArrowSumSudokuCircles,
                        puzzle.ArrowSumSudokuBodies)
    
    if puzzle.Windoku:
        Solver.WindokuConstraints()
    
    if puzzle.DisjointSudoku:
        Solver.DisjointConstraints()
    
    if puzzle.KillerCage:
        Solver.KillerSudokuConstraints(puzzle.KillerCageSums,
                                       puzzle.KillerCageMap)
    
    if puzzle.LittleKillerCage:
        Solver.LittleKillerSudokuConstraints(puzzle.LittleKillerCageSums,
                                       puzzle.LittleKillerCageMap)
    
    if puzzle.OddEvenCell:
        Solver.OddEvenConstraints(puzzle.OddEvenCellMap)
    
    if puzzle.RatioPairsCondition:
        Solver.RatioPairs(numerators=puzzle.RatioPairsNumerators,
                          denominators=puzzle.RatioPairsDenominators,
                          pairs=puzzle.RatioPairs)
    
    if puzzle.DifferencePairsCondition:
        Solver.DifferencePairs(differences=puzzle.DifferencePairsDifferences,
                               pairs=puzzle.DifferencePairs)
    
    if puzzle.ThermometerConstraint:
        Solver.ThermometerConstraints(puzzle.Thermometers)
    
    if puzzle.QuadsCondition:
        Solver.QuadsConstraints(puzzle.QuadIDs, puzzle.QuadVals)
    
    if puzzle.MultiAntiSumsCondition:
        for AntiSum, PairsExceptions in zip(puzzle.MultiAntiSums, puzzle.MultiAntiSumsPairsList):
            Solver.OrthogonalAntiSumConstraints(AntiSum, PairsExceptions)
    
    if puzzle.MultiAntiRatiosCondition:
        for numerator, denominator, PairsExceptions in zip(puzzle.MultiAntiRatiosNumerators, 
                                                            puzzle.MultiAntiRatiosDenominators, 
                                                            puzzle.MultiAntiRatiosPairsList):
            Solver.OrthogonalAntiRatioConstraints(numerator, denominator, PairsExceptions)
    
    if puzzle.AdditionPairsCondition:
        Solver.AdditionPairs(puzzle.AdditionPairsSums, puzzle.AdditionPairs)
            
    # with open("output.txt", "w") as f:
    #     # print(Solver.Model, file=f)
    #     for constraint in Solver.Model.Proto().constraints:
    #         print(constraint, file=f)
        
    Solutions = Solver.MultiSolutionSolve()
    # Solutions = Solver.Solve()
    
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