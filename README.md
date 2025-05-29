# Gmail Summarizer AI Agent

This project fetches unread Gmail messages, summarizes them using an AI model, and optionally converts the summary to speech.

## Features

- ✅ Authenticates with Gmail via OAuth2
- 📩 Fetches recent unread emails from the Primary category
- 🧹 Cleans and trims email bodies (removes URLs, formats text)
- 🧠 Summarizes emails using a local Ollama model (`mistral:latest`)
- 🔊 Converts summary to MP3 audio using Google Text-to-Speech (gTTS)
- 🪵 Logs key steps with timestamps

## Setup

1. **Clone this repo**  
   ```bash
   git clone https://github.com/dharmmaharaja/gmail-summarizer-ai-agent.git
   cd gmail-summarizer-ai-agent
   ```

2. **Create virtual environment and install dependencies**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Place credentials**  
   - Download `credentials.json` from Google Cloud Console.
   - Place it in the project root.

4. **Install Ollama and pull model**  
   ```bash
   ollama pull mistral
   ```

## Usage

```bash
python gmail-summrizer.py
```

This will:
- Fetch emails
- Summarize them using `mistral` via Ollama API on `localhost:11434`
- Save the summary to `summary.mp3`

## Dependencies

- `google-api-python-client`
- `google-auth-oauthlib`
- `requests`
- `gtts`
- `openai`

Install with:

```bash
pip install -r requirements.txt
```

## Notes

- The summarization model must be running locally via Ollama.
- The `.gitignore` should exclude `venv/` and `token.pkl`.

## License

This project uses open-source dependencies, each under their respective licenses.