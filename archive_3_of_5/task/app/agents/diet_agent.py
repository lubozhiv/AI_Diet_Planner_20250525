from app.services.llm_client import LLMClient
from app.models import DietResponse
import json
from typing import List


class DietAgent:
    """
    Agent responsible for applying dietary restrictions and suggesting recipe ideas.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def process_diet(self, items: List[str], diet: str) -> DietResponse:
        """
        Process a list of items and apply dietary restrictions to suggest compatible recipes.

        Args:
            items: List of items to process
            diet: Type of diet (e.g., "vegan", "keto", "mediterranean", "gluten-free", "paleo")

        Returns:
            DietResponse with compatible items and suggested recipe ideas
        """
        prompt = (
            f"You are a nutritionist and cooking expert. Given the JSON array of ingredients:\n"
            f"{json.dumps(items)}\n"
            f"And the dietary preference: {diet}\n\n"
            f"Return a JSON object with:\n"
            f"  compatible_items: an array of ingredients that are compatible with the {diet} diet,\n"
            f"  suggested_recipe_ideas: an array with EXACTLY 5 recipe ideas that can be made using the compatible ingredients and follow the {diet} diet.\n"
            f"Recipes should be short titles, not detailed descriptions.\n"
            f"Respond ONLY with valid JSON."
        )

        try:
            # Get response from LLM
            response = await self.llm_client.get_completion(prompt)

            # Create DietResponse from LLM response
            compatible_items = response.get("compatible_items", [])
            recipe_ideas = response.get("suggested_recipe_ideas", [])

            # Ensure exactly 5 recipe ideas
            if len(recipe_ideas) > 5:
                recipe_ideas = recipe_ideas[:5]
            while len(recipe_ideas) < 5:
                recipe_ideas.append(f"Simple {diet.capitalize()} Dish with {', '.join(compatible_items[:2])}")

            return DietResponse(
                compatible_items=compatible_items,
                suggested_recipe_ideas=recipe_ideas
            )
        except Exception as e:
            # Handle any errors with fallback logic
            # For fallback, we'll do a simple filtering based on common dietary restrictions
            compatible = items.copy()
            if diet.lower() == "vegan":
                # Simple fallback logic for vegan diet
                non_vegan = ["meat", "chicken", "beef", "pork", "fish", "egg", "milk", "cheese", "butter", "cream"]
                compatible = [item for item in items if not any(nv in item.lower() for nv in non_vegan)]

            return DietResponse(
                compatible_items=compatible,
                suggested_recipe_ideas=[
                    f"{diet.capitalize()} Recipe 1 with {compatible[0] if compatible else 'ingredients'}",
                    f"{diet.capitalize()} Recipe 2 with {compatible[0] if compatible else 'ingredients'}",
                    f"{diet.capitalize()} Recipe 3 with {compatible[0] if compatible else 'ingredients'}",
                    f"{diet.capitalize()} Recipe 4 with {compatible[0] if compatible else 'ingredients'}",
                    f"{diet.capitalize()} Recipe 5 with {compatible[0] if compatible else 'ingredients'}"
                ]
            )