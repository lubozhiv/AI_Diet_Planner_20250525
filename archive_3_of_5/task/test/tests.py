import json
import requests
from hstest import StageTest, CheckResult, dynamic_test

class FastAPIStageTest(StageTest):
    BASE_URL = "http://localhost:8000"

    @dynamic_test(time_limit=120_000)
    def test_root(self):
        try:
            response = requests.get(f"{self.BASE_URL}/")
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")
        
        if "Success" not in response_data.get("message", ""):
            return CheckResult.wrong(f"Expected 'Success' in the 'message' value, but got {response_data.get('message', '')}.")

        return CheckResult.correct()

    @dynamic_test(time_limit=120_000)
    def test_ask(self):
        payload = {
            "items": ["tomato", "chicken breast", "spinach", ""],
            "diet": "vegan"
        }

        try:
            response = requests.post(f"{self.BASE_URL}/ask", json=payload)
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            body = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")

        if "usable_items" not in body:
            return CheckResult.wrong("'usable_items' key is missing in response.")
        if "diet_filtered" not in body:
            return CheckResult.wrong("'diet_filtered' key is missing in response.")
        if "suggestions" not in body:
            return CheckResult.wrong("'suggestions' key is missing in response.")
        if not isinstance(body.get("suggestions"), list):
            return CheckResult.wrong("'suggestions' should be a list.")

        return CheckResult.correct()