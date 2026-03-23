# agent.py - Lightweight ReAct Agent
import requests
import re
from tools import get_current_weather, get_weather_forecast

# LM Studio API endpoint
LM_STUDIO_URL = "http://192.168.31.39:1234/v1/chat/completions"

# Load system prompt
def load_system_prompt():
    try:
        with open('system_prompt.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful weather assistant. Be friendly and use tools to get weather data."

SYSTEM_PROMPT = load_system_prompt()

# Tool definitions
TOOLS = {
    "get_current_weather": {
        "function": get_current_weather,
        "description": "Get current weather for a city. Input: city name"
    },
    "get_weather_forecast": {
        "function": get_weather_forecast,
        "description": "Get weather forecast for a city. Input: city name (optional days)"
    }
}

def call_lm_studio(messages):
    """Call LM Studio API with OpenAI-compatible format"""
    try:
        payload = {
            "model": "google/gemma-3-1b",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500,
            "stream": False
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(LM_STUDIO_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
            return None
        else:
            print(f"LM Studio error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"LM Studio error: {e}")
        return None

def create_agent(user_input: str, max_iterations: int = 3) -> str:
    """
    ReAct agent pattern - Think -> Act -> Observe -> Repeat
    """
    # Build the initial prompt with tools information
    tools_desc = "\n".join([f"- {name}: {info['description']}" for name, info in TOOLS.items()])
    
    system_message = f"""{SYSTEM_PROMPT}

You have access to these tools:
{tools_desc}

When you need to use a tool, output: TOOL_CALL: tool_name|input
Otherwise, just output your response.

Think step by step:
1. Understand what the user is asking
2. Decide if you need to use a tool
3. If yes, output the tool call
4. After getting tool result, provide final answer

Be friendly and conversational!"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    
    iteration = 0
    
    while iteration < max_iterations:
        response = call_lm_studio(messages)
        
        if not response:
            return "Hello! I'm having trouble connecting to my brain. Please check if LM Studio is running. 😊"
        
        # Check for tool call
        if "TOOL_CALL:" in response:
            # Extract tool call
            tool_match = re.search(r'TOOL_CALL:\s*(\w+)\|(.+?)(?:\n|$)', response)
            
            if tool_match:
                tool_name = tool_match.group(1).strip()
                tool_input = tool_match.group(2).strip()
                
                if tool_name in TOOLS:
                    print(f"🔧 Using tool: {tool_name}('{tool_input}')")
                    tool_result = TOOLS[tool_name]["function"](tool_input)
                    
                    # Add tool result to conversation
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": f"Tool result: {tool_result}\n\nNow provide your final answer to the user."})
                else:
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": f"Error: Tool '{tool_name}' not found. Available: {', '.join(TOOLS.keys())}"})
            else:
                # Invalid format
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": "Please use format: TOOL_CALL: tool_name|input"})
        else:
            # No tool call, this is the final answer
            return response
        
        iteration += 1
    
    return "I've reached the maximum number of attempts. Please try asking differently."

# Test function
if __name__ == "__main__":
    print("Testing Lightweight Weather Agent...")
    print("=" * 60)
    
    test_queries = [
        "Is it raining in Pune?",
        "What's the weather in Mumbai?",
        "Hello!"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = create_agent(query)
        print(f"🤖 Agent: {response}")
        print("-" * 60)