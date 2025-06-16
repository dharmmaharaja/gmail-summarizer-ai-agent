import logging
import os
from flask import Flask, render_template, render_template_string, send_file,jsonify
from gmail_summrizer import get_unread_emails, save_summary_text,summarize_emails_ollama,speak_text,play_audio

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/summarize')
def summarize():
    try: 
      emails = get_unread_emails()
      if not emails:
              return jsonify(success=True, summary="No unread emails found.")
      import json
      logging.info("Emails:\n%s", json.dumps(emails, indent=3))
      summary = summarize_emails_ollama(emails)
      if not summary:
              return jsonify(success=False, error="Failed to generate summary.")
      logging.info(f"Summary:{summary}")
      save_summary_text(summary)
      speak_text(summary)
      return jsonify(success=True, summary=summary)
    except Exception as e:
        return jsonify(success=False, error=str(e))
    #play_audio()
    
    #return send_file("summary.mp3", mimetype="audio/mpeg")

@app.route("/audio")
def get_audio():
    # Serve the saved MP3 file
    return send_file("summary.mp3", mimetype="audio/mpeg")


@app.route('/summary.mp3')
def serve_audio():
    path = '/static/summary.mp3'
    if os.path.exists(path):
        return send_file(path, mimetype='audio/mpeg')
    return '', 404

@app.route('/api/last-summary')
def get_last_summary():
    if os.path.exists("static/last_summary.txt"):
        with open("static/last_summary.txt", "r", encoding="utf-8") as f:
            last_summary = f.read()
        return jsonify(success=True, summary=last_summary)
    else:
        return jsonify(success=False, summary="No summary found.")

if __name__ == "__main__":
    app.run(port=8000)
