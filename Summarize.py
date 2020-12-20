from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

def getWordFreqTable(words):
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    table = dict()

    for word in words:
        word = stemmer.stem(word)
        if word in stop_words:
            continue

        if word in table:
            table[word] += 1
        else:
            table[word] = 1

    return table

def getSentenceScoreTable(sentences, wordFreqTable, character_depth = 10):
    table = dict()

    for sentence in sentences:
        num_words = len(word_tokenize(sentence))
        for wordValue in wordFreqTable:
            if wordValue in sentence.lower():
                if sentence[:character_depth] in table:
                    table[sentence[:character_depth]] += wordFreqTable[wordValue]
                else:
                    table[sentence[:character_depth]] = wordFreqTable[wordValue]

        table[sentence[:character_depth]] = table[sentence[:character_depth]] // num_words

    return table

def getAverageScore(sentenceScoreTable):
    sumValues = 0
    for key in sentenceScoreTable:
        sumValues += sentenceScoreTable[key]
    avg = int(sumValues / len(sentenceScoreTable))

    return avg

def getSummary(sentences, sentenceScoreTable, threshold, character_depth = 10):
    num_sentences = 0
    summary = ""

    for sentence in sentences:
        if sentence[:character_depth] in sentenceScoreTable and sentenceScoreTable[sentence[:character_depth]] > threshold:
            summary += sentence + " "
            num_sentences += 1

    return summary

def summarize(text, thresholdScale = 1.1):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    wordFreqTable = getWordFreqTable(words)
    sentenceScores = getSentenceScoreTable(sentences, wordFreqTable)
    threshold = getAverageScore(sentenceScores) * thresholdScale
    summary = getSummary(sentences, sentenceScores, threshold)

    return summary