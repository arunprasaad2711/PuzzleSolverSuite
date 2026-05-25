from pydantic import BaseModel, Field
from typing import List, Optional

class Chess(BaseModel):
    
    Order: int = 8
    NRooks: bool = False
    NBishops: bool = False
    NBishopsRowConstraint: bool = False
    NQueens: bool = True