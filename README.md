
📧 Gmail Summarizer AI Agent 🎙️
A Python-based tool that reads your unread Gmail messages, summarizes them using LLM models (e.g., Ollama Mistral), and then speaks the summary as an audio file (.mp3) using gTTS.

🔥 Features
✅ Authenticates with Gmail using OAuth 2.0

📩 Fetches recent unread emails from your Primary inbox

🧠 Summarizes emails using local LLM (e.g., Mistral via Ollama)

🔊 Converts the summary to speech using Google Text-to-Speech

📁 Outputs an .mp3 file you can play on your mobile/laptop

🧱 Tech Stack
Python 3.8+

Google Gmail API

Ollama – local LLMs like Mistral

gTTS – Text-to-speech

OpenAI (optional / commented)

📦 Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/dharmmaharaja/gmail-summarizer-ai-agent.git
cd gmail-summarizer-ai-agent
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Setup Gmail API

Download credentials.json from Google Developer Console

Save it in the project root.

First run will open a browser to authorize access.

Run Ollama with Mistral

bash
Copy
Edit
ollama run mistral
🚀 Usage
bash
Copy
Edit
python gmail-summrizer.py
This will:

Fetch your unread primary emails from the past 5 days

Summarize them using mistral:latest model via Ollama

Save a speech audio as summary.mp3 in the current folder

🔧 Configuration
Gmail query: You can adjust query = "is:unread newer_than:5d category:primary" for your use case

Summarizer model: Replace "mistral:latest" with any Ollama-supported model

Speech output length: Limited to 5000 characters

🎧 Playing MP3 on Mobile
To listen on your phone:

Use Google Drive, Dropbox, or AirDrop to transfer summary.mp3

Or automate syncing with a cloud folder

🛡️ Security
Tokens are stored in token.pkl locally.

Do not expose your credentials.json or api_key in public repos.

🧠 Prompt Customization
Change the summarization prompt in summarize_emails_ollama() for better results:

python
Copy
Edit
"Please summarize these email messages as clear, concise bullet points..."
🧪 Example Output
pgsql
Copy
Edit
📩 Fetched 10 unread emails
✅ Summary generated
🔊 MP3 saved as summary.mp3
📄 License
MIT License – Free to use and modify.
