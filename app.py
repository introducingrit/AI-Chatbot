from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

api_key = 'your_api_key'

@app.route('/', methods=['GET'])
def home():
    # Only render the HTML on the first visit
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Receive the full conversation history from JavaScript
    data = request.json
    client_messages = data.get('messages', [])
    
    # Your detailed system prompt
    system_prompt = {
        "role": "system",
        "content": """You are a helpful assistant.

Always format your answers clearly and professionally.

Rules:
- Use bullet points whenever explaining information.
- Use numbered lists for step-by-step instructions.
- Keep paragraphs short.
- Use headings when the answer has multiple sections.
- Highlight important words using bold formatting.
- Avoid long blocks of plain text.
- Make answers easy to read and scan.
- If there are multiple points, separate them into bullet points.
- Give concise but useful answers."""
    }
    
    # Ensure the advanced system prompt overrides any basic one from the frontend
    if client_messages and client_messages[0].get("role") == "system":
        client_messages[0] = system_prompt
    else:
        client_messages.insert(0, system_prompt)

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "openai/gpt-oss-20b",
            "messages": client_messages
        }
    )

    data_response = response.json()

    if response.ok:
        reply = data_response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    else:
        error_msg = data_response.get('error', {}).get('message', 'Something went wrong.')
        return jsonify({"reply": f"Error: {error_msg}"})

if __name__ == '__main__':
    app.run(debug=True)