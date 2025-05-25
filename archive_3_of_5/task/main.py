from fastapi import FastAPI, HTTPException
from app.models import InventoryInput, DietInput, InventoryResponse, DietResponse, AskInput, AskResponse
from app.services.llm_client import LLMClient
from app.agents.inventory_agent import InventoryAgent
from app.agents.diet_agent import DietAgent
from app.agents.manager_agent import ManagerAgent

# Initialize FastAPI app
app = FastAPI(title="Cooking Assistant API")

# Initialize LLM client
llm_client = LLMClient()

# Initialize agents
inventory_agent = InventoryAgent(llm_client)
diet_agent = DietAgent(llm_client)
manager_agent = ManagerAgent(inventory_agent, diet_agent)


@app.post("/inventory", response_model=InventoryResponse)
async def process_inventory(input_data: InventoryInput):
    """
    Process a list of inventory items and return usable items.
    """
    try:
        return await inventory_agent.process_items(input_data.items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing inventory: {str(e)}")


@app.post("/diet", response_model=DietResponse)
async def process_diet(input_data: DietInput):
    """
    Process a list of items with dietary restrictions and suggest recipe ideas.
    """
    # Validate diet input
    valid_diets = ["vegan", "keto", "mediterranean", "gluten-free", "paleo"]
    if input_data.diet.lower() not in [d.lower() for d in valid_diets]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid diet: {input_data.diet}. Must be one of: {', '.join(valid_diets)}"
        )

    try:
        return await diet_agent.process_diet(input_data.items, input_data.diet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing diet: {str(e)}")


@app.post("/ask", response_model=AskResponse)
async def process_ask(input_data: AskInput):
    """
    Unified endpoint that orchestrates the workflow between the Inventory Agent
    and Diet Agent to process items and provide diet-specific suggestions.
    """
    # Validate diet input
    valid_diets = ["vegan", "keto", "mediterranean", "gluten-free", "paleo"]
    if input_data.diet.lower() not in [d.lower() for d in valid_diets]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid diet: {input_data.diet}. Must be one of: {', '.join(valid_diets)}"
        )

    try:
        result = await manager_agent.process_request(input_data.items, input_data.diet)
        return AskResponse(
            usable_items=result["usable_items"],
            diet_filtered=result["diet_filtered"],
            suggestions=result["suggestions"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Cooking Assistant API is running"}