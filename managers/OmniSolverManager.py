from solvers.OmniSolver.OmniPuzzleSolver import OmniPuzzleSolver
from models.OmniSolverInputJSONClass import Omni

def OmniSolverManager(puzzle: Omni):
    
    # print(f"Inside OmniSolverManager with data {puzzle}")
    
    Solver = OmniPuzzleSolver(puzzle.Matrix,
            puzzle.OrderRow, puzzle.OrderCol,
            puzzle.ZeroMaskingDigit, 
            puzzle.LowerBound, puzzle.UpperBound,
            puzzle.NoOfSearchers)
    
    if puzzle.Sudoku:
        Solver.ClassicSudokuConstraints()
    
    if puzzle.TLBR_Diagonal:
        Solver.TLBR_DiagonalConstraint()
    
    if puzzle.TRBL_Diagonal:
        Solver.TRBL_DiagonalConstraint()
    
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
    
    if puzzle.ArrowAverageSudoku:
        Solver.ArrowAverage(puzzle.ArrowAverageSudokuCircles,
                        puzzle.ArrowAverageSudokuBodies)
    
    if puzzle.Windoku:
        Solver.WindokuConstraints()
    
    if puzzle.DisjointSudoku:
        Solver.DisjointConstraints()
    
    if puzzle.KillerCage:
        Solver.KillerSudokuConstraints(puzzle.KillerCageSums,
                                       puzzle.KillerCageMap)
    
    if puzzle.RowSumCondition:
        Solver.RowSumConstraints(puzzle.RowSums)
    
    if puzzle.ColSumCondition:
        Solver.ColSumConstraints(puzzle.ColSums)
    
    if puzzle.SubGridSumCondition:
        Solver.SubGridSumConstraints(puzzle.SubGridSums)
    
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
    
    if puzzle.SlowThermometerConstraint:
        Solver.SlowThermometerConstraints(puzzle.SlowThermometers)
    
    if puzzle.QuadsCondition:
        Solver.QuadsConstraints(puzzle.QuadIDs, puzzle.QuadVals)
    
    if puzzle.SameSetRegionsConstraint:
        Solver.SameSetRegions(puzzle.SameSetRegionsSet1, puzzle.SameSetRegionsSet2)
    
    if puzzle.CloneRegionsConstraint:
        Solver.CloneRegions(puzzle.CloneRegionsSet1, puzzle.CloneRegionsSet2)
    
    if puzzle.MultiAntiSumsCondition:
        for AntiSum, PairsExceptions in zip(puzzle.MultiAntiSums, puzzle.MultiAntiSumsPairsList):
            Solver.OrthogonalAntiSumConstraints(AntiSum, PairsExceptions)
    
    if puzzle.MultiAntiDifferenceCondition:
        print("Inside MultiAntiDifference")
        for AntiDifference, PairsExceptions in zip(puzzle.MultiAntiDifference, puzzle.MultiAntiDifferencePairsList):
            print(f"Anti difference = {AntiDifference}, pair = {PairsExceptions}")
            Solver.OrthogonalAntiDifferenceConstraints(AntiDifference, PairsExceptions)
    
    if puzzle.MultiAntiRatiosCondition:
        print("Inside MultiAntiRatios")
        for numerator, denominator, PairsExceptions in zip(puzzle.MultiAntiRatiosNumerators, 
                                                            puzzle.MultiAntiRatiosDenominators, 
                                                            puzzle.MultiAntiRatiosPairsList):
            print(f"Anti ratio = {numerator} : {denominator}, pair = {PairsExceptions}")
            Solver.OrthogonalAntiRatioConstraints(numerator, denominator, PairsExceptions)
    
    if puzzle.AdditionPairsCondition:
        Solver.AdditionPairs(puzzle.AdditionPairsSums, puzzle.AdditionPairs)
    
    if puzzle.SandWichSudoku:
        Solver.SandWichConstraints(puzzle.SandWichRowSums, puzzle.SandWichColSums,
                                   puzzle.SandWichLowNumber, puzzle.SandWichHighNumber)
    
    if puzzle.SkyScraperConstraint:
        Solver.SkyscraperConstraints(puzzle.LeftSkyScrapers, puzzle.RightSkyScrapers,
                                     puzzle.TopSkyScrapers, puzzle.BottomSkyScrapers)
    
    if puzzle.ExtendedSudokuCondition:
        Solver.ExtendedSudokuRowConstraint()
        Solver.ExtendedSudokuColConstraint()
        Solver.ExtendedSudokuSubGridConstraint()
    
    if puzzle.LineDifferenceConstraint:
        Solver.LineDifferences(puzzle.LineDifferenceDifferences,
                               puzzle.LineDifferenceConditions,
                               puzzle.LineDifferenceLines)
    
    if puzzle.GermanWhispersCondition:
        Solver.LineDifferences([5]*len(puzzle.GermanWhispersLines),
                               [1]*len(puzzle.GermanWhispersLines),
                               puzzle.GermanWhispersLines)
    
    if puzzle.DutchWhispersCondition:
        Solver.LineDifferences([4]*len(puzzle.DutchWhispersLines),
                               [1]*len(puzzle.DutchWhispersLines),
                               puzzle.DutchWhispersLines)
    
    if puzzle.RenbanCondition:
        Solver.RenbanLinesConstraints(puzzle.RenbanLines)
    
    if puzzle.NabnerCondition:
        Solver.NabnerLinesConstraints(puzzle.NabnerLines)
    
    if puzzle.PalindromeLineCondition:
        Solver.PalindromeLineConstraints(puzzle.PalindromeLines)
    
    if puzzle.RegionSumLinesCondition:
        Solver.RegionSumLinesConstraints(puzzle.RegionSumLinesGridMap,
                                         puzzle.RegionSumLinesEqualSegmentsIDs,
                                         puzzle.RegionSumLinesNonRepeatValues)
    
    if puzzle.RestrictedCellsCondition:
        Solver.RestrictedCellsConstraints(puzzle.RestrictedCellsMap,
                                          puzzle.RestrictedCellsValsList)
    
    if puzzle.MagicSquareCondition:
        Solver.MagicSquareConstraints(puzzle.MagicSquareSets)
    
    if puzzle.Hidato:
        Solver.HidatoConstraints(puzzle.HidatoRuleMode)
    
    if puzzle.StarBattle:
        Solver.ClassicStarBattleConstraints(puzzle.StarBattleGridMap, puzzle.StarsPerRegion)
    
    if puzzle.NoriNori:
        Solver.ClassicNoriNoriConstraints(puzzle.NoriNoriGridMap, puzzle.NoriNoriPerRegion)
    
    if puzzle.MineSweeper:
        Solver.ClassicMineSweeperConstraints(puzzle.MineSweeperGridMap, puzzle.MineSweeperNeighbourMode)
    
    if puzzle.TentsPuzzle:
        Solver.ClassicTentsConstraints(puzzle.TentsTreeMap, puzzle.TentsAlongRows,
                                       puzzle.TentsAlongCols)
    
    if puzzle.NBishops:
        Solver.NBishopsConstraint(puzzle.NBishopsRowConstraint)
    
    if puzzle.NRooks:
        Solver.NRooksConstraint()
    
    if puzzle.NQueens:
        Solver.NQueensConstraint()
    
    if puzzle.HitoriPuzzle:
        Solver.ClassicHitoriConstraint(puzzle.HitoriGridMap)
    
    if puzzle.CreekPuzzle:
        Solver.ClassicCreekConstraint(puzzle.CreekPuzzleGroups,
                                      puzzle.CreekPuzzleGroupValues)

    if puzzle.PrintConstraints:
        with open("output.txt", "w") as f:
            # print(Solver.Model, file=f)
            for constraint in Solver.Model.Proto().constraints:
                print(constraint, file=f)
    
    if puzzle.SingleSolution:
        Solutions = Solver.Solve()
    else:
        Solutions = Solver.MultiSolutionSolve()
    
    return Solutions