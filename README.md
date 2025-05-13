# PhysioAssist

## Project Structure

Create the following files in your project directory:

```
PhysioAssist/
│
├── .env                  # Environment variables (API keys)
├── requirements.txt      
└── ...                # The other files
```


### Contents for .env

```
GROQ_API_KEY=your_groq_api_key_here
```
- you can get the API key form: https://console.groq.com/keys

## Usage
 1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app
```bash
streamlit run home.py
```
