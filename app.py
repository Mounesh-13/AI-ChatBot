import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
from werkzeug.exceptions import BadRequest
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate required environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is not set in environment variables")
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Validate API key format
if not GEMINI_API_KEY.startswith("AIzaSy"):
    logger.error("Invalid GEMINI_API_KEY format")
    raise ValueError("Invalid GEMINI_API_KEY format. It should start with 'AIzaSy'")

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Test API key by listing models
try:
    models = genai.list_models()
    logger.info(f"Successfully connected to Gemini API. Available models: {[m.name for m in models]}")
except Exception as e:
    logger.error(f"Could not validate Gemini API key: {str(e)}")
    logger.info("Continuing with API configuration...")

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
        logger.error(f"Error testing API: {str(e)}")
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
        logger.error(f"Error listing models: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Could not list models'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global request_count, last_reset_time
    
    try:
        logger.info("Received chat request")
        logger.debug(f"Request data: {request.data}")
        
        # Basic rate limiting
        current_time = datetime.now()
        if last_reset_time is None or (current_time - last_reset_time).seconds >= 60:
            request_count = 0
            last_reset_time = current_time
            logger.info("Resetting rate limit counter")
        
        if request_count >= MAX_REQUESTS_PER_MINUTE:
            logger.warning("Rate limit exceeded")
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        
        request_count += 1
        logger.info(f"Current request count: {request_count}")
        
        # Validate request
        if not request.is_json:
            logger.error('Request must be JSON')
            raise BadRequest('Request must be JSON')
            
        data = request.get_json()
        user_message = data.get('message', '').strip()
        logger.info(f"User message: {user_message}")
        
        if not user_message:
            logger.error('Message cannot be empty')
            raise BadRequest('Message cannot be empty')
            
        # Call Gemini API with correct model name
        logger.info("Initializing Gemini model...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Sending request to Gemini API...")
            response = model.generate_content(user_message)
            logger.info("Received response from Gemini API")
            
            if not response.text:
                logger.error('Empty response from Gemini API')
                raise ValueError('Empty response from Gemini API')
                
            bot_response = response.text.strip()
            logger.info(f"Bot response: {bot_response}")
            
            return jsonify({
                'response': bot_response
            })
            
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            raise ValueError(f"Error with Gemini API: {str(e)}")
            
    except BadRequest as e:
        logger.error(f"BadRequest error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': 'Sorry, there was an error processing your request. Please try again later.'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
