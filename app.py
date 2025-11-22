"""
Flask Web Application for Tourism AI Agent System
"""
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from agents.parent_agent import TourismAIAgent
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the Tourism AI Agent
try:
    agent = TourismAIAgent()
    agent_ready = True
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent_ready = False
    agent = None

@app.route('/')
def index():
    """Render the main HTML page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user query and return response"""
    if not agent_ready or not agent:
        return jsonify({
            'success': False,
            'error': 'Agent not initialized. Please check your GOOGLE_API_KEY in .env file.'
        }), 500
    
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                'success': False,
                'error': 'Please provide a query.'
            }), 400
        
        # Process the query
        response = agent.process_query(user_query)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

