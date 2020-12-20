import os
import re
from google.cloud import language
from nltk import sent_tokenize

def getEntities(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"general-use-c85025f0b131.json"
    client = language.LanguageServiceClient()
    document = language.Document(content = text.title(), type_ = language.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document = document)
    return response.entities

def getWikipediaLinks(entities):
    wiki = {}
    for entity in entities:
        wiki_url = entity.metadata.get("wikipedia_url", "")
        if wiki_url:
            wiki[str(entity.name)] = str(wiki_url)
    return wiki

def addHTMLWikipediaLinks(wiki_links, text):
    return_text = text
    for link in wiki_links:
        pattern = re.compile(link, re.IGNORECASE)
        return_text = pattern.sub(f"<a href=\"{wiki_links[link]}\">{link}</a>", return_text, count = 1)
    return return_text

def entityToHTMLLinks(text):
    entities = getEntities(text)
    wikilinks = getWikipediaLinks(entities)
    html = addHTMLWikipediaLinks(wikilinks, text)
    return html

def getFlashcards(summary):
    flashcards = []
    summary_sentences = sent_tokenize(summary)
    for sent in summary_sentences:
        entities = getEntities(sent)
        for entity in entities:
            wiki_url = entity.metadata.get("wikipedia_url", "")
            if wiki_url:
                flashcards.append([sent.replace(str(entity.name).lower(), "_____"), entity.name])
    return flashcards

if __name__ == "__main__":
    text = "So, let's begin by describing the wave theory of Light. Now, just like a mechanical wave carries energy as it propagates through space. Electromagnetic waves also carry energy and Light waves, carry energy and the energy is stored within the oscillating electric and magnetic fields. Now, the only way that this diffraction pattern was explained is by assuming that Light does in fact act as a wave. That depends on the frequency of that Light, so this is our Light wave that consists of individual, discrete photons. Now each photon is in fact a Massless Particle. So, within The Photoelectric Experiment, Light was essentially directed at a metal surface to eject the electrons found on those surface. So once again, within the photoelectric effect, experiment, Light was directed at metal, surface and electrons were only ejected if the frequency of Light and the energy of Light was high enough. So that means no matter how intense our Light wave is. If the frequency is not high enough because of the one-to-one collision between the photon electron, no ejection takes place. So this experiment basically validated the particle theory of Light. The fact that Light consists of photons now the second experiment that basically validated the photon theory of Light, was the confidence act in this experiment. Photons, basically collided and interacted with stationary electrons and scattering of those photons took place. So once again, Light can act as a wave or it can act as a particle as described in these two theories and this phenomenon. This concept became known as the wave particle duality of Light."
    print(getFlashcards(text))