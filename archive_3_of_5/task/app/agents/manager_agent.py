from app.agents.inventory_agent import InventoryAgent
from app.agents.diet_agent import DietAgent
from typing import List, Dict, Any


class ManagerAgent:
    """
    Agent responsible for orchestrating the workflow between the Inventory Agent
    and Diet Agent to provide a unified experience.
    """

    def __init__(self, inventory_agent: InventoryAgent, diet_agent: DietAgent):
        self.inventory_agent = inventory_agent
        self.diet_agent = diet_agent

    async def process_request(self, items: List[str], diet: str) -> Dict[str, Any]:
        """
        Process a request by orchestrating the workflow between the Inventory Agent
        and Diet Agent.

        Args:
            items: List of items to process
            diet: Type of diet to apply

        Returns:
            A dictionary containing:
            - usable_items: Items filtered by the Inventory Agent
            - diet_filtered: Items compatible with the diet
            - suggestions: Recipe suggestions based on the diet
        """
        # Step 1: Call the Inventory Agent to filter out unusable items
        inventory_response = await self.inventory_agent.process_items(items)
        usable_items = inventory_response.usable_items

        # Step 2: Call the Diet Agent to apply dietary restrictions and get suggestions
        diet_response = await self.diet_agent.process_diet(usable_items, diet)

        # Step 3: Create the final response
        manager_response = {
            "usable_items": usable_items,
            "diet_filtered": diet_response.compatible_items,
            "suggestions": diet_response.suggested_recipe_ideas
        }

        return manager_response