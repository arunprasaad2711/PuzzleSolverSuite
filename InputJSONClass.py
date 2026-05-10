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

class Chess(BaseModel):
    
    Order: int = 8
    NRooks: bool = False
    NBishops: bool = False
    NBishopsRowConstraint: bool = False
    NQueens: bool = True

class PocketCube(BaseModel):
    
    Hashes: List[int]