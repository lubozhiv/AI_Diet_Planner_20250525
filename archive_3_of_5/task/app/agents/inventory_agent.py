from app.services.llm_client import LLMClient
from app.models import InventoryResponse
import json
from typing import List


class InventoryAgent:
    """
    Agent responsible for processing inventory items and filtering out unusable ones.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def process_items(self, items: List[str]) -> InventoryResponse:
        """
        Process a list of items and filter out any that are unusable for cooking.

        Args:
            items: List of items to process

        Returns:
            InventoryResponse with usable items and a confirmation message
        """
        prompt = (
            f"You are a kitchen assistant. Given the JSON array of ingredients:\n"
            f"{json.dumps(items)}\n"
            "Return a JSON object with:\n"
            "  usable_items: an array of ingredients that are non-empty and suitable for cooking (remove blank or invalid entries),\n"
            "  message: a short confirmation string.\n"
            "Respond ONLY with valid JSON."
        )

        try:
            # Get response from LLM
            response = await self.llm_client.get_completion(prompt)

            # Create InventoryResponse from LLM response
            return InventoryResponse(
                usable_items=response.get("usable_items", []),
                message=response.get("message", "Items processed successfully.")
            )
        except Exception as e:
            # Handle any errors
            return InventoryResponse(
                usable_items=[item for item in items if item.strip()],
                message=f"Error processing items: {str(e)}. Using basic filtering instead."
            )