from pydantic import BaseModel
from typing import List

# Input models
class InventoryInput(BaseModel):
    items: List[str]

class DietInput(BaseModel):
    items: List[str]
    diet: str

class AskInput(BaseModel):
    items: List[str]
    diet: str

# Response models
class InventoryResponse(BaseModel):
    usable_items: List[str]
    message: str

class DietResponse(BaseModel):
    compatible_items: List[str]
    suggested_recipe_ideas: List[str]

class AskResponse(BaseModel):
    usable_items: List[str]
    diet_filtered: List[str]
    suggestions: List[str]