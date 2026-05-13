from pydantic import BaseModel, Field
from typing import List

class Omni(BaseModel):
    
    # Basic Sudoku Puzzle order
    OrderRow: int = 3
    OrderCol: int = 3
    Matrix: List[List[int]] = Field(default_factory=list)
    LowerBound: int = 1
    UpperBound: int = 9
    
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

class Chess(BaseModel):
    
    Order: int = 8
    NRooks: bool = False
    NBishops: bool = False
    NBishopsRowConstraint: bool = False
    NQueens: bool = True

class PocketCube(BaseModel):
    
    Hashes: List[int]