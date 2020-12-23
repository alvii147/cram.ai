import os
import re
from google.cloud import language
from nltk import sent_tokenize

# get entities from text
def getEntities(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"general-use-c85025f0b131.json"
    client = language.LanguageServiceClient()
    document = language.Document(content = text.title(), type_ = language.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document = document)
    return response.entities

# get entities with wikipedia links
def getWikipediaLinks(entities):
    wiki = {}
    for entity in entities:
        wiki_url = entity.metadata.get("wikipedia_url", "")
        if wiki_url:
            wiki[str(entity.name)] = str(wiki_url)
    return wiki

# add wikipedia hyperlinks to entities
def addHTMLWikipediaLinks(wiki_links, text):
    return_text = text
    for link in wiki_links:
        pattern = re.compile(link, re.IGNORECASE)
        return_text = pattern.sub(f"<a href=\"{wiki_links[link]}\">{link}</a>", return_text, count = 1)
    return return_text

# add wikipedia hyperlinks to text
def entityToHTMLLinks(text):
    entities = getEntities(text)
    wikilinks = getWikipediaLinks(entities)
    html = addHTMLWikipediaLinks(wikilinks, text)
    return html

# generate flashcards from entities
def getFlashcards(summary):
    summary_processed = summary
    punc = [',', '.', ' ']
    remove_list = []
    for char in summary_processed:
        if (not char.isalnum()) and (char not in punc):
            if char not in remove_list:
                remove_list.append(char)
    for char in remove_list:
        summary_processed = summary_processed.replace(char, '')

    flashcards = []
    summary_sentences = sent_tokenize(summary_processed)
    for sent in summary_sentences:
        entities = getEntities(sent)
        if len(entities) != 0:
            for entity in entities:
                wiki_url = entity.metadata.get("wikipedia_url", "")
                if wiki_url:
                    flashcards.append([sent.replace(str(entity.name).lower(), "_____"), entity.name])
    return flashcards

if __name__ == "__main__":
    text = "And boy, do I know that feeling. My team lost, the national coach walked away. Not as much."
    print(getFlashcards(text))
