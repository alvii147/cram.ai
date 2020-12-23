import re
import string
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess

# get YouTube video ID from URL
def getID(URL):
    id_capture_regex = "^.*(youtu.be\/|v\/|e\/|u\/\w+\/|embed\/|v=)([^#\&\?]*).*"
    ID = re.match(id_capture_regex, URL).group(2)
    return ID

# get transcript from YouTube video ID
def getTranscript(ID):
    transcript_dict = YouTubeTranscriptApi.get_transcript(ID)
    transcript_array = [chunk["text"] for chunk in transcript_dict]
    transcript_text_raw = " ".join(transcript_array)
    printable = set(string.printable)
    transcript_text = "".join(filter(lambda x: x in printable, transcript_text_raw))
    return transcript_text

# add punctuation to text
def punctuateText(text):
    if '.' in text or ',' in text:
        return text
    processedText = text.replace("&", "%26")
    cmd = subprocess.run(f"curl -d \"text={processedText}\" http://bark.phon.ioc.ee/punctuator", capture_output = True, encoding="utf8")
    return cmd.stdout

# get transcription from YouTube URL
def smartTranscribe(URL):
    ID = getID(URL)
    transcript = getTranscript(ID)
    punctuatedTranscript = punctuateText(transcript)
    return punctuatedTranscript

if __name__ == "__main__":
    URL = "https://www.youtube.com/watch?v=CqgmozFr_GM"
    print(smartTranscribe(URL))
