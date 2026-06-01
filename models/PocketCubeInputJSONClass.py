from pydantic import BaseModel, Field
from typing import Optional

class PocketCube(BaseModel):
    
    Hashes: list[int]