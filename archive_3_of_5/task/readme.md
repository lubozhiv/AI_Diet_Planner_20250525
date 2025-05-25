# Cooking Assistant API

This FastAPI application provides a multi-agent system for cooking assistance:

1. **Inventory Agent**: Filters and cleans up a list of groceries
2. **Diet Agent**: Applies dietary restrictions to ingredients and suggests recipe ideas
3. **Manager Agent**: Orchestrates the workflow between the Inventory and Diet agents

## Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- A Groq API key (get it from https://console.groq.com)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install fastapi uvicorn httpx python-dotenv
```

3. Set up environment variables:
```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file and add your Groq API key
# LLM_API_KEY=your-groq-api-key-here
```

### Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### 1. Unified Workflow (Recommended)

**POST /ask**

This endpoint orchestrates the workflow by calling both the Inventory and Diet agents in sequence.

Request:
```bash
curl -X POST http://localhost:8000/ask \
     -H 'Content-Type: application/json' \
     -d '{"items":["tomato","chicken","spinach"],"diet":"keto"}'
```

Response:
```json
{
  "usable_items": ["tomato", "chicken", "spinach"],
  "diet_filtered": ["tomato", "chicken", "spinach"],
  "suggestions": [
    "Keto Chicken Spinach Salad",
    "Keto Tomato Chicken Stir-Fry",
    "Spinach & Chicken Keto Bowl",
    "Chicken Spinach Wraps",
    "Tomato Chicken Skillet"
  ]
}
```

### 2. Individual Agent Endpoints

#### Inventory Agent

**POST /inventory**

Filter out unusable ingredients from a list.

Request:
```bash
curl -X POST http://localhost:8000/inventory \
     -H 'Content-Type: application/json' \
     -d '{"items":["tomato"," ","chicken","spinach",""]}'
```

Response:
```json
{
  "usable_items": ["tomato", "chicken", "spinach"],
  "message": "Filtered usable items successfully."
}
```

#### Diet Agent

**POST /diet**

Apply dietary restrictions and get recipe suggestions.

Request:
```bash
curl -X POST http://localhost:8000/diet \
     -H 'Content-Type: application/json' \
     -d '{"items":["tomato","chicken","spinach"],"diet":"vegan"}'
```

Response:
```json
{
  "compatible_items": ["tomato", "spinach"],
  "suggested_recipe_ideas": [
    "Vegan Tomato Spinach Salad",
    "Tomato Spinach Pasta",
    "Spinach & Tomato Wraps",
    "Tomato-Spinach Soup",
    "Grilled Tomato & Spinach Bruschetta"
  ]
}
```

## Supported Diets

- Vegan
- Keto
- Mediterranean
- Gluten-Free
- Paleo

## Testing

You can test the API using the provided test scripts:

```bash
# Test the /ask endpoint
python test_ask.py

# Test the individual endpoints
python test_api.py
```