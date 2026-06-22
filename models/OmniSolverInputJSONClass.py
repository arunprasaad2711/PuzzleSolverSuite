from pydantic import BaseModel, Field
from typing import Optional, Literal

class Omni(BaseModel):

    SingleSolution: bool = False
    PrintConstraints: bool = False
    NoOfSearchers: int = 1
    
    # Basic Sudoku Puzzle order
    OrderRow: int = 3
    OrderCol: int = 3
    Matrix: list[list[int]] = Field(default_factory=list)
    LowerBound: int = 1
    UpperBound: int = 9
    ZeroMaskingDigit: int = -1

    # Defaults for Chess Solver
    NRooks: bool = False
    NBishops: bool = False
    NBishopsRowConstraint: bool = False
    NQueens: bool = False

    # Diagonal Condition
    TLBR_Diagonal: bool = False
    TRBL_Diagonal: bool = False

    # Sum of Elements in Rows, Colums, Subgrids
    RowSumCondition: bool = False
    ColSumCondition: bool = False
    SubGridSumCondition: bool = False
    RowSums: Optional[list] = Field(default_factory=list)
    ColSums: Optional[list] = Field(default_factory=list)
    SubGridSums: Optional[list] = Field(default_factory=list)
    
    # Puzzle Booleans
    Sudoku: bool = False
    IrregularSudoku: bool = False
    
    # Chess Constraints
    AntiKnight: bool = False
    AntiKing: bool = False

    # Simple Constraints
    ArgyleSudoku: bool = False
    GirandolaSudoku: bool = False
    CentreDotSudoku: bool = False
    AsteriskSudoku: bool = False
    
    # Non-consecutive Constraints:
    OrthogonalNonConsec: bool = False
    DiagonalNonConsec: bool = False

    # Minimum Difference
    OrthogonalMinDifference: bool = False
    DiagonalMinDifference: bool = False
    OrthogonalMinDifferenceValue: int = 2
    DiagonalMinDifferenceValue: int = 2

    # Irregular Sudoku Region
    IrregularSudokuRegionMap: list[list[int]] = Field(default_factory=list)

    # Arrow Sum Sudoku
    ArrowSumSudoku: bool = False
    ArrowSumSudokuCircles: list[list[int]] = Field(default_factory=list)
    ArrowSumSudokuBodies: list[list[list[int]]] = Field(default_factory=list)

    # Arrow Average Sudoku
    ArrowAverageSudoku: bool = False
    ArrowAverageSudokuCircles: list[list[int]] = Field(default_factory=list)
    ArrowAverageSudokuBodies: list[list[list[int]]] = Field(default_factory=list)

    # Windoku and Disjoint Sudoku
    Windoku: bool = False
    DisjointSudoku: bool = False

    # Magic Square Condition
    MagicSquareCondition: bool = False
    MagicSquareSets: list[list[list[int]]] = Field(default_factory=list)

    # Killer Cage Sudoku
    KillerCage: bool = False
    KillerCageMap: list[list[int]] = Field(default_factory=list)
    KillerCageSums: list[int] = Field(default_factory=list)

    # Little Killer Cage Sudoku
    LittleKillerCage: bool = False
    LittleKillerCageMap: list[list[int]] = Field(default_factory=list)
    LittleKillerCageSums: list[int] = Field(default_factory=list)

    # Odd Even Cell Sudoku
    OddEvenCell: bool = False
    OddEvenCellMap: list[list[int]] = Field(default_factory=list)

    # Difference Pairs
    DifferencePairsCondition: bool = False
    DifferencePairs: list[list[list[int]]] = Field(default_factory=list)
    DifferencePairsDifferences: list[int] = Field(default_factory=list)

    # Ratio Pairs
    RatioPairsCondition: bool = False
    RatioPairs: list[list[list[int]]] = Field(default_factory=list)
    RatioPairsNumerators: list[int] = Field(default_factory=list)
    RatioPairsDenominators: list[int] = Field(default_factory=list)

    # Thermometers
    ThermometerConstraint: bool = False
    Thermometers: list[list[list[int]]] = Field(default_factory=list)

    # Slow Thermometers
    SlowThermometerConstraint: bool = False
    SlowThermometers: list[list[list[int]]] = Field(default_factory=list)

    # Quads Condition
    QuadsCondition: bool = False
    QuadIDs: list[list[int]] = Field(default_factory=list)
    QuadVals: list[list[int]] = Field(default_factory=list)

    # Same Set Regions
    SameSetRegionsConstraint: bool = False
    SameSetRegionsSet1: list[list[list[int]]] = Field(default_factory=list)
    SameSetRegionsSet2: list[list[list[int]]] = Field(default_factory=list)

    # Clone Regions
    CloneRegionsConstraint: bool = False
    CloneRegionsSet1: list[list[list[int]]] = Field(default_factory=list)
    CloneRegionsSet2: list[list[list[int]]] = Field(default_factory=list)

    # Addition Pairs
    AdditionPairsCondition: bool = False
    AdditionPairs: list[list[list[int]]] = Field(default_factory=list)
    AdditionPairsSums: list[int] = Field(default_factory=list)

    # Multi Anti Sum Constraints
    MultiAntiSumsCondition: bool = False
    MultiAntiSums: list[int] = Field(default_factory=list)
    MultiAntiSumsPairsList: Optional[list[list[list[int]]]] = Field(default_factory=list)

    # Multi Anti Difference Constraints
    MultiAntiDifferenceCondition: bool = False
    MultiAntiDifference: list[int] = Field(default_factory=list)
    MultiAntiDifferencePairsList: Optional[list[list[list[int]]]] = Field(default_factory=list)

    # Multi Anti Ratio Constraints
    MultiAntiRatiosCondition: bool = False
    MultiAntiRatiosNumerators: list[int] = Field(default_factory=list)
    MultiAntiRatiosDenominators: list[int] = Field(default_factory=list)
    MultiAntiRatiosPairsList: Optional[list[list[list[int]]]] = Field(default_factory=list)

    # Sandwich Sudoku
    SandWichSudoku: bool = False
    SandWichRowSums: list[Optional[int]] = Field(default_factory=list)
    SandWichColSums: list[Optional[int]] = Field(default_factory=list)
    SandWichLowNumber: int = 1
    SandWichHighNumber: int = 9

    # Skyscraper Sudoku
    SkyScraperConstraint: bool = False
    LeftSkyScrapers: list[Optional[int]] = Field(default_factory=list)
    RightSkyScrapers: list[Optional[int]] = Field(default_factory=list)
    TopSkyScrapers: list[Optional[int]] = Field(default_factory=list)
    BottomSkyScrapers: list[Optional[int]] = Field(default_factory=list)

    # German Whisphers
    GermanWhispersCondition: bool = False
    GermanWhispersLines: list[list[list[int]]] = Field(default_factory=list)

    # Dutch Whisphers
    DutchWhispersCondition: bool = False
    DutchWhispersLines: list[list[list[int]]] = Field(default_factory=list)

    # Line Difference - Differences can be any value including German/Dutch whispers
    LineDifferenceConstraint: bool = False
    LineDifferenceLines: list[list[list[int]]] = Field(default_factory=list)
    LineDifferenceDifferences: list[int] = Field(default_factory=list)
    LineDifferenceConditions: list[int] = Field(default_factory=list)

    # Renban Lines
    RenbanCondition: bool = False
    RenbanLines: list[list[list[int]]] = Field(default_factory=list)

    # Nabner Lines
    NabnerCondition: bool = False
    NabnerLines: list[list[list[int]]] = Field(default_factory=list)

    # Palindrome Lines
    PalindromeLineCondition: bool = False
    PalindromeLines: list[list[list[int]]] = Field(default_factory=list)

    # Region Sum Lines
    RegionSumLinesCondition: bool = False
    RegionSumLinesGridMap: list[list[int]] = Field(default_factory=list)
    RegionSumLinesEqualSegmentsIDs: list[list[int]] = Field(default_factory=list)
    RegionSumLinesNonRepeatValues: list[bool] = Field(default_factory=list)


    # Restricted Cells Condition. Some cells can have only restricted values
    RestrictedCellsCondition: bool = False
    RestrictedCellsMap: list[list[int]] = Field(default_factory=list)
    RestrictedCellsValsList: list[list[int]] = Field(default_factory=list)

    # Unique Entity Condition
    ExtendedSudokuCondition: bool = False

    # Hidato Constraints
    Hidato: bool = False
    HidatoRuleMode: Literal["King", "Knight"] = "King"

    # Star Battle Constraints. Also applicable for Starstruck/Queens/Kings
    # by changing the number of stars
    StarBattle: bool = False
    StarsPerRegion: int = 2
    StarBattleGridMap: list[list[int]] = Field(default_factory=list)

    # Nori-Nori Constraints.
    NoriNori: bool = False
    NoriNoriPerRegion: int = 2
    NoriNoriGridMap: list[list[int]] = Field(default_factory=list)

    # MineSweeper Constraints.
    MineSweeper: bool = False
    MineSweeperNeighbourMode: Literal["King", "Knight", "Orthogonal", "Diagonal"] = "King"
    MineSweeperGridMap: list[list[int]] = Field(default_factory=list)

    # Tents Puzzle Constraints
    TentsPuzzle: bool = False
    TentsAlongRows: list[int] = Field(default_factory=list)
    TentsAlongCols: list[int] = Field(default_factory=list)
    TentsTreeMap: list[list[int]] = Field(default_factory=list)