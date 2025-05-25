import os
import json
import httpx
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()


class LLMClient:
    """Client for interacting with Groq's LLM API."""

    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv("LLM_API_KEY")
        if not self.api_key:
            raise ValueError("LLM_API_KEY environment variable not set")

        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"

    async def get_completion(self, prompt: str) -> Dict[Any, Any]:
        """
        Send a prompt to the LLM and get a structured JSON response.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Parsed JSON response from the LLM
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse the JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse LLM response as JSON")