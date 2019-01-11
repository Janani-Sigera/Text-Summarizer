from nltk.corpus import wordnet
import re

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize


def corpus_generator(*features):
        synonyms = []
        for feature in features[0]:
            synonyms.append(feature)
            feature = str(feature)
            synsets = wordnet.synsets(feature)

            for synset in synsets:
                for hypo in synset.hyponyms():
                    for lem in hypo.lemmas():
                        synonyms.append(lem.name())
        synonyms = (set(synonyms))
        return synonyms

def sentence_extracter(features, text):
    sent = []
    for hyp in features:
        ext = re.findall(r"([^.]*?" + hyp + "[^.]*\.)", str(text))
        if (ext != []):
            sent.extend(ext)
    return sent

def summary_ratio(averageTime,text):
    tokenizer = RegexpTokenizer("[\w']+")
    word = tokenizer.tokenize(text)
    count = len(word)
    rat = (float)((200*averageTime/60)/count)
    return rat

# def summary_ratio(averageTime,text):
#     tokenizer = RegexpTokenizer("[\w']+")
#     word = tokenizer.tokenize(text)
#     count = len(word)
#     rat = (float)((200*averageTime)/count)
#     return rat

def summary_generator(text,averageTime):
    # title, text = get_only_text(url)

    # rat= (float)(summary_ratio(averageTime,text))
    rat = (float)(summary_ratio(averageTime, text))

    sum= summarize(str(text), ratio=rat)
    summary = sum.rstrip().replace("\n", " ")
    # return title,summary
    return summary

def summary_merge(generalSummary,sentences,text):
    generalSummarySentences = sent_tokenize(generalSummary)
    generalSummarySentsWithoutQuotos = [item.replace('"', '') for item in generalSummarySentences]
    generalSummarySentsWithoutQuotos = [item.replace('/', '') for item in generalSummarySentences]
    #remove quotes ans slashes from text
    textSentences = sent_tokenize(text)
    textSentsWithoutQuotes= textSentences


    for sent in sentences:
        sentWithoutQuotes = sent
        sentWithoutQuotes = sentWithoutQuotes.lstrip()
        sentWithoutQuotes = sentWithoutQuotes.rstrip()

        if not sentWithoutQuotes in generalSummarySentsWithoutQuotos:
            index = textSentsWithoutQuotes.index(sentWithoutQuotes)
            if index == 0:
                generalSummarySentences.insert(0, sent)
            else:
                for index in range(0):
                    previousSent = textSentences[index-1]
                    if previousSent in generalSummarySentsWithoutQuotos:
                        previousIndex = generalSummarySentsWithoutQuotos.index(previousSent)
                        generalSummarySentences.insert(previousIndex+1, sent)
                        break
                    else:
                        index = index - 1

    return generalSummarySentences


averageTime = int(input("\n Enter average time of user in seconds: "))
word = input("Enter personal interests separated by comma ")
word = word.split(",")

# word =input("enter word:")
# title,summary = summary_generator(url,averageTime)
text = input("Enter text: ")
summary = summary_generator(text, averageTime)
# print("title:"+title)

features = corpus_generator(word)
print(corpus_generator(word))
sentences = sentence_extracter(features, text)
generalSummarySentences = sent_tokenize(summary)
print(generalSummarySentences)
print(summary_merge(summary, sentences, text))
