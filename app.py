from flask import Flask, render_template, request, redirect, url_for, session, flash
from Transcribe import getID, getTranscript, punctuateText
from Summarize import summarize
from Entity import entityToHTMLLinks, getFlashcards

app = Flask(__name__)
app.secret_key = "c9l3n5b1"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        URL = request.form["url"]
        ID = getID(URL)
        return redirect(url_for("summary", ID = ID))
    return render_template("home.html")

@app.route("/<ID>")
def summary(ID):
    URL = f"https://www.youtube.com/embed/{ID}"
    transcript = punctuateText(getTranscript(ID))
    summary = summarize(transcript)
    flashcards = getFlashcards(summary)
    transcript = entityToHTMLLinks(transcript)
    summary = entityToHTMLLinks(summary)
    return render_template("transcribe.html", URL = URL, transcript = transcript, summary = summary, flashcards = flashcards)

if __name__ == "__main__":
    app.run(debug = True)