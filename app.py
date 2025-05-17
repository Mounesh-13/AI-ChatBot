import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
from werkzeug.exceptions import BadRequest
from datetime import datetime

# Load environment variables
load_dotenv()

# Validate required environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Validate API key format
if not GEMINI_API_KEY.startswith("AIzaSy"):
    raise ValueError("Invalid GEMINI_API_KEY format. It should start with 'AIzaSy'")

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Test API key by listing models
try:
    models = genai.list_models()
    print(f"Successfully connected to Gemini API. Available models: {[m.name for m in models]}")
except Exception as e:
    print(f"Warning: Could not validate Gemini API key: {str(e)}")
    print("Continuing with API configuration...")

# Rate limiting configuration
MAX_REQUESTS_PER_MINUTE = 60
request_count = 0
last_reset_time = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test-api')
def test_api():
    try:
        models = genai.list_models()
        model_names = [m.name for m in models]
        return jsonify({
            'status': 'success',
            'models': model_names,
            'message': 'Successfully connected to Gemini API'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error connecting to Gemini API: {str(e)}'
        }), 500

@app.route('/models', methods=['GET'])
def list_models():
    try:
        models = genai.list_models()
        model_names = [m.name for m in models]
        return jsonify({'models': model_names})
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Could not list models'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global request_count, last_reset_time
    
    try:
        print("Received chat request")
        print(f"Request data: {request.data}")
        
        # Basic rate limiting
        current_time = datetime.now()
        if last_reset_time is None or (current_time - last_reset_time).seconds >= 60:
            request_count = 0
            last_reset_time = current_time
            print("Resetting rate limit counter")
        
        if request_count >= MAX_REQUESTS_PER_MINUTE:
            print("Rate limit exceeded")
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        
        request_count += 1
        print(f"Current request count: {request_count}")
        
        # Validate request
        if not request.is_json:
            raise BadRequest('Request must be JSON')
            
        data = request.get_json()
        user_message = data.get('message', '').strip()
        print(f"User message: {user_message}")
        
        if not user_message:
            raise BadRequest('Message cannot be empty')
            
        # Call Gemini API with correct model name
        print("Initializing Gemini model...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            print("Sending request to Gemini API...")
            response = model.generate_content(user_message)
            print("Received response from Gemini API")
            
            if not response.text:
                raise ValueError('Empty response from Gemini API')
                
            bot_response = response.text.strip()
            print(f"Bot response: {bot_response}")
            
            return jsonify({
                'response': bot_response
            })
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            raise ValueError(f"Error with Gemini API: {str(e)}")
            
    except BadRequest as e:
        print(f"BadRequest error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': 'Sorry, there was an error processing your request. Please try again later.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
