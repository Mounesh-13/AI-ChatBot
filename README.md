# Modern AI Chatbot with Flask and Google Gemini

A sleek, modern AI chatbot web application built with Flask and Google's Gemini API, featuring a dark, cozy theme and smooth interactions.

## Features

- Modern dark theme with frosted glass effects
- Real-time chat interface with smooth animations
- Rate limiting for API calls
- Error handling with user-friendly messages
- Responsive design for all screen sizes
- Loading states and API validation
- Model listing and testing

## Prerequisites

- Python 3.7+
- Google Gemini API key (starts with 'AIzaSy')
- pip (Python package installer)

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd ai-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
ai-chatbot/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Modern dark theme styles
│   └── js/
│       └── chat.js    # Chat functionality
├── templates/
│   └── index.html    # Main template
└── .env              # Environment variables
```

## Technologies Used

- Backend: Flask
- Frontend: HTML, CSS, JavaScript
- AI: Google Gemini API
- Styling: Modern dark theme with frosted glass effects
- Error Handling: Comprehensive error management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to Google for the Gemini API
- Special thanks to the Flask community for their excellent documentation

## Support

For support, please open an issue in the repository or contact the maintainer.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Rename `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Visit `http://localhost:5000` in your web browser.

## Project Structure

```
ai-chatbot/
├── app.py                # Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── Procfile              # For deployment
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Styles
│   └── js/
│       └── chat.js     # Frontend JavaScript
└── templates/
    └── index.html      # Main HTML template
```

## Customization

- **Styling**: Edit `static/css/style.css` to change the look and feel.
- **Behavior**: Modify `static/js/chat.js` for frontend behavior changes.
- **Backend**: Edit `app.py` to change the AI model or add new features.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [OpenAI GPT-3.5-turbo](https://openai.com/)
- Modern UI with custom CSS
