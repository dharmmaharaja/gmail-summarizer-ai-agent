Here's your **organized, detailed, and copy-ready `README.md`**, perfect for GitHub or sharing:

---

````markdown
# 📬 Gmail Summarizer AI Agent

This project fetches unread Gmail messages, summarizes them using a local AI model via Ollama, and optionally converts the summary to an MP3 audio file using Google Text-to-Speech (gTTS).

---

## 🚀 Features

- ✅ **Authenticate Gmail** using OAuth2
- 📩 **Fetch unread emails** from the Primary inbox (last 5 days)
- 🧹 **Clean and trim email content** (removes URLs, excess newlines)
- 🧠 **Summarize emails locally** using [Ollama](https://ollama.com) + `mistral:latest`
- 🔊 **Convert summary to MP3** using `gTTS`
- 🪵 **Detailed logging** for every step with timestamps

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dharmmaharaja/gmail-summarizer-ai-agent.git
cd gmail-summarizer-ai-agent
````

### 2️⃣ Create Virtual Environment & Install Requirements

```bash
python -m venv venv
# For Linux/macOS:
source venv/bin/activate
# For Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 3️⃣ Add Google Gmail API Credentials

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Create a project → Enable Gmail API → Create OAuth credentials
* Download `credentials.json` and place it in the **project root folder**

---

## 🛠️ Ollama Installation & Model Setup

### ✅ Step 1: Install Ollama

#### 🔵 macOS (via Homebrew)

```bash
brew install ollama
```

#### 🔵 Linux (Debian/Ubuntu)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 🔵 Windows

1. Download from [https://ollama.com/download](https://ollama.com/download)
2. Run the `.exe` installer
3. Restart your computer if needed

---

### ✅ Step 2: Verify Ollama Installation

```bash
ollama --version
```

---

### ✅ Step 3: Pull the Model (e.g., `mistral`)

```bash
ollama pull mistral
```

To pull the latest version:

```bash
ollama pull mistral:latest
```

Check installed models:

```bash
ollama list
```

---

### ✅ Step 4: Start Ollama Server (Terminal 1)

```bash
ollama serve
```

Keep this running — your Python app talks to it at `http://localhost:11434`.

---

### ✅ Step 5: (Optional) Run the Model in CLI

```bash
ollama run mistral
```

---

## ▶️ How to Run

Make sure your Ollama server is running in a separate terminal, then run:

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

This project is based on **open-source libraries**, each governed by their respective licenses. See individual library documentation for details.
