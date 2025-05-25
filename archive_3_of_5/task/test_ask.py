import requests
import json

BASE_URL = "http://localhost:8000"


def test_ask_endpoint():
    """Test the ask endpoint with a sample request."""

    # Test data
    data = {
        "items": ["tomato", "chicken", "spinach", " ", ""],
        "diet": "keto"
    }

    # Send POST request
    response = requests.post(
        f"{BASE_URL}/ask",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )

    # Print response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Check if successful
    if response.status_code == 200:
        print("✅ Ask endpoint test successful")

        # Verify the structure of the response
        result = response.json()
        if all(key in result for key in ["usable_items", "diet_filtered", "suggestions"]):
            print("✅ Response structure is correct")

            # Verify that usable_items doesn't contain empty strings
            if not any(item == "" or item == " " for item in result["usable_items"]):
                print("✅ Empty items filtered correctly")
            else:
                print("❌ Empty items not filtered correctly")

            # Verify that we have exactly 5 suggestions
            if len(result["suggestions"]) == 5:
                print("✅ Exactly 5 suggestions provided")
            else:
                print(f"❌ Expected 5 suggestions, got {len(result['suggestions'])}")
        else:
            print("❌ Response structure is incorrect")
    else:
        print("❌ Ask endpoint test failed")


def test_different_diets():
    """Test the ask endpoint with different diets."""

    diets = ["vegan", "keto", "mediterranean", "gluten-free", "paleo"]
    items = ["chicken", "broccoli", "rice", "cheese", "eggs", "tomato", "avocado", "bread"]

    for diet in diets:
        print(f"\n=== Testing {diet.upper()} diet ===")

        # Test data
        data = {
            "items": items,
            "diet": diet
        }

        # Send POST request
        response = requests.post(
            f"{BASE_URL}/ask",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )

        # Print response
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()

            print(f"Original items: {len(items)}")
            print(f"Usable items: {len(result['usable_items'])}")
            print(f"Diet-compatible items: {len(result['diet_filtered'])}")
            print(f"Number of suggestions: {len(result['suggestions'])}")

            print("\nDiet-compatible items:")
            for item in result["diet_filtered"]:
                print(f"  - {item}")

            print("\nRecipe suggestions:")
            for suggestion in result["suggestions"]:
                print(f"  - {suggestion}")
        else:
            print(f"Response: {response.text}")


if __name__ == "__main__":
    print("Testing Ask Endpoint...")
    test_ask_endpoint()

    print("\nTesting Different Diets...")
    test_different_diets()