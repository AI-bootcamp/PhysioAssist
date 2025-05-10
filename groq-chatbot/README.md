

## Project Structure

Create the following files in your project directory:

```
groq-chatbot/
│
├── .env                  # Environment variables (API keys)
└── app.py                # Main Streamlit application
```


### Contents for .env

```
GROQ_API_KEY=your_groq_api_key_here
```
- you can get the API key form: https://console.groq.com/keys

## Usage
 1. Install required packages:
   ```bash
   pip install streamlit groq python-dotenv
   ```
2. Run the app
```bash
streamlit run app.py
```