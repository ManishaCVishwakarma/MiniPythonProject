# 🌤️ Agentic Weather Assistant

## Overview
This project is an **Agentic AI-based Weather Assistant** built using Python, Flask, and LM Studio (local LLM).

Agentic AI systems combine:
- **LLM (the brain)** – Google's Gemma-3-1b running locally via LM Studio
- **System prompt (behavior)** – Defines how the agent thinks and acts
- **Tools (capabilities)** – Functions to fetch real-time weather data

The agent uses the **ReAct pattern**:
1. **Think** – Understands the user's query
2. **Act** – Calls appropriate tools when needed
3. **Observe** – Processes tool results
4. **Repeat** – Continues until providing final answer

The system can **autonomously understand user queries, decide actions, and use tools** to fetch real-time weather information.

---

## Features
- Agentic AI (autonomous decision-making)
- Local LLM using LM Studio (no API cost)
- Tool-based architecture (weather API integration)
- Flask web interface for easy interaction
- Real-time weather data using **Open-Meteo API**
- Natural language – Extracts city names automatically

---

## How It Works

1. User sends a query to the Flask web interface
2. The **Agent** receives the query and processes it through LM Studio
3. The **LLM (brain)** analyzes the input using the system prompt
4. If weather data is needed, the agent decides to use a **tool** (`get_current_weather` or `get_weather_forecast`)
5. The tool fetches live weather data from Open-Meteo API
6. The agent interprets the data and formats a natural response
7. Final response is returned to the user with emojis and friendly language

---

## Technologies Used

- **Python** – Core programming language
- **Flask** – Web framework for the interface
- **Requests** – HTTP client for API calls
- **LM Studio** – Local LLM hosting (Gemma-3-1b)
- **Open-Meteo API** – Free weather data source

---

## Installation & Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Configuration
1. Update the LM Studio URL in `agent.py` or set environment variable:
   ```bash
   export LM_STUDIO_URL="http://your-ip:1234/v1/chat/completions"
text
