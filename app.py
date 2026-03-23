# app.py - Flask web interface
from flask import Flask, request, jsonify, render_template_string
from agent import create_agent

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Assistant</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 10px;
            outline: none;
        }
        input:focus {
            border-color: #667eea;
        }
        button {
            padding: 12px 30px;
            font-size: 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        button:hover {
            background: #5a67d8;
        }
        .response {
            margin-top: 20px;
            padding: 20px;
            background: #f7f9fc;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .query {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        .examples {
            margin-top: 30px;
            padding: 15px;
            background: #eef2f7;
            border-radius: 10px;
        }
        .examples h3 {
            margin-top: 0;
        }
        .examples ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .examples li {
            margin: 5px 0;
        }
        .status {
            margin-top: 20px;
            text-align: center;
            font-size: 0.8em;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Assistant</h1>
        <div class="subtitle">Autonomous AI Agent | ReAct Pattern | LM Studio Brain</div>
        
        <form method="GET" action="/weather">
            <div class="input-group">
                <input type="text" name="q" placeholder="Is it raining in Pune?" required>
                <button type="submit">Ask</button>
            </div>
        </form>
        
        {% if query %}
        <div class="response">
            <div class="query">You: {{ query }}</div>
            <div>🤖 {{ response }}</div>
        </div>
        {% endif %}
        
        <div class="examples">
            <h3>💡 Try asking:</h3>
            <ul>
                <li>Is it raining in Mumbai?</li>
                <li>What's the weather in Delhi?</li>
                <li>Will it rain in Bangalore?</li>
                <li>Weather forecast for London</li>
                <li>Hello! Good morning</li>
            </ul>
        </div>
        
        <div class="status">
            🧠 LLM Brain: LM Studio (google/gemma-3-1b) | 🔄 Pattern: ReAct Agent
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, query=None, response=None)

@app.route("/weather")
def weather():
    query = request.args.get("q", "")
    if not query:
        return render_template_string(HTML_TEMPLATE, query=None, 
                                     response="Please enter a question")
    
    response = create_agent(query)
    return render_template_string(HTML_TEMPLATE, query=query, response=response)

@app.route("/api/weather")
def weather_api():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = create_agent(query)
    return jsonify({"query": query, "response": response})

if __name__ == "__main__":
    print("=" * 60)
    print("🌤️ Lightweight Agentic Weather Assistant")
    print("=" * 60)
    print("🧠 LLM: LM Studio (google/gemma-3-1b)")
    print("🔄 Pattern: ReAct (Thought → Action → Observation)")
    print("🌐 Web: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)