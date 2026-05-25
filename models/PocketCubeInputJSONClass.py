from pydantic import BaseModel, Field
from typing import List, Optional

class PocketCube(BaseModel):
    
    Hashes: List[int]