from pydantic import BaseModel, Field
from typing import List, Optional

class Omni(BaseModel):
    
    # Basic Sudoku Puzzle order
    OrderRow: int = 3
    OrderCol: int = 3
    Matrix: List[List[int]] = Field(default_factory=list)
    LowerBound: int = 1
    UpperBound: int = 9
    ZeroMaskingDigit: int = -1

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
    Sudoku: bool = True
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
    IrregularSudokuRegionMap: List[List[int]] = Field(default_factory=list)

    # Arrow Sudoku
    ArrowSumSudoku: bool = False
    ArrowSumSudokuCircles: List[List[int]] = Field(default_factory=list)
    ArrowSumSudokuBodies: List[List[List[int]]] = Field(default_factory=list)

    # Windoku and Disjoint Sudoku
    Windoku: bool = False
    DisjointSudoku: bool = False

    # Magic Square Condition
    MagicSquareCondition: bool = False
    MagicSquareSets: List[List[List[int]]] = Field(default_factory=List)

    # Killer Cage Sudoku
    KillerCage: bool = False
    KillerCageMap: List[List[int]] = Field(default_factory=list)
    KillerCageSums: List[int] = Field(default_factory=list)

    # Little Killer Cage Sudoku
    LittleKillerCage: bool = False
    LittleKillerCageMap: List[List[int]] = Field(default_factory=list)
    LittleKillerCageSums: List[int] = Field(default_factory=list)

    # Odd Even Cell Sudoku
    OddEvenCell: bool = False
    OddEvenCellMap: List[List[int]] = Field(default_factory=list)

    # Difference Pairs
    DifferencePairsCondition: bool = False
    DifferencePairs: List[List[List[int]]] = Field(default_factory=list)
    DifferencePairsDifferences: List[int] = Field(default_factory=list)

    # Ratio Pairs
    RatioPairsCondition: bool = False
    RatioPairs: List[List[List[int]]] = Field(default_factory=list)
    RatioPairsNumerators: List[int] = Field(default_factory=list)
    RatioPairsDenominators: List[int] = Field(default_factory=list)

    # Thermometers
    ThermometerConstraint: bool = False
    Thermometers: List[List[List[int]]] = Field(default_factory=list)

    # Quads Condition
    QuadsCondition: bool = False
    QuadIDs: List[List[int]] = Field(default_factory=list)
    QuadVals: List[List[int]] = Field(default_factory=list)

    # Addition Pairs
    AdditionPairsCondition: bool = False
    AdditionPairs: List[List[List[int]]] = Field(default_factory=list)
    AdditionPairsSums: List[int] = Field(default_factory=list)

    # Multi Anti Sum Constraints
    MultiAntiSumsCondition: bool = False
    MultiAntiSums: List[int] = Field(default_factory=list)
    MultiAntiSumsPairsList: List[List[List[List[int]]]] = Field(default_factory=list)

    # Multi Anti Ratio Constraints
    MultiAntiRatiosCondition: bool = False
    MultiAntiRatiosNumerators: List[int] = Field(default_factory=list)
    MultiAntiRatiosDenominators: List[int] = Field(default_factory=list)
    MultiAntiRatiosPairsList: List[List[List[List[int]]]] = Field(default_factory=list)

    # Sandwich Sudoku
    SandWichSudoku: bool = False
    SandWichRowSums: List[Optional[int]] = Field(default_factory=list)
    SandWichColSums: List[Optional[int]] = Field(default_factory=list)
    SandWichLowNumber: int = 1
    SandWichHighNumber: int = 9

    # German Whisphers
    GermanWhispersCondition: bool = False
    GermanWhispersLines: List[List[List[int]]] = Field(default_factory=list)

    # Dutch Whisphers
    DutchWhispersCondition: bool = False
    DutchWhispersLines: List[List[List[int]]] = Field(default_factory=list)

    # Line Difference - Differences can be any value including German/Dutch whispers
    LineDifferenceConstraint: bool = False
    LineDifferenceLines: List[List[List[int]]] = Field(default_factory=list)
    LineDifferenceDifferences: List[int] = Field(default_factory=list)
    LineDifferenceConditions: List[int] = Field(default_factory=list)

    # Renban Lines
    RenbanCondition: bool = False
    RenbanLines: List[List[List[int]]] = Field(default_factory=list)

    # Nabner Lines
    NabnerCondition: bool = False
    NabnerLines: List[List[List[int]]] = Field(default_factory=list)

    # Palindrome Lines
    PalindromeLineCondition: bool = False
    PalindromeLines: List[List[List[int]]] = Field(default_factory=list)

    # Region Sum Lines
    RegionSumLinesCondition: bool = False
    RegionSumLinesGridMap: List[List[int]] = Field(default_factory=list)
    RegionSumLinesEqualSegmentsIDs: List[List[int]] = Field(default_factory=list)
    RegionSumLinesNonRepeatValues: List[bool] = Field(default_factory=list)


    # Restricted Cells Condition. Some cells can have only restricted values
    RestrictedCellsCondition: bool = False
    RestrictedCellsMap: List[List[int]] = Field(default_factory=list)
    RestrictedCellsValsList: List[List[int]] = Field(default_factory=list)

    # Unique Entity Condition
    ExtendedSudokuCondition: bool = False