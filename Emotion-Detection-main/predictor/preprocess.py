from collections import Counter
import pandas as pd
import nltk
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def clean(message):
    df = pd.DataFrame(message)

    string = [str(item) for item in df[0]]

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    text_stem = []
    for i in string:
        text = stemmer.stem(i)
        text_stem.append(text)

    dataframe_stem = pd.DataFrame(text_stem)

    def remove_stopwords(lemma):
        #lemmatises and then removes stopwords
        lemma = [lemmatiser.lemmatize(word) for word in lemma if word not in (stop_english) and (word.isalpha())]
        lemma = " ".join(lemma) #joins the words back into a single string
        return lemma

    #slits each string into a list of words using tokenizer
    df_stem = dataframe_stem[0].apply(word_tokenize)

    lemmatiser = WordNetLemmatizer()
    stop_english = Counter(stopwords.words())
    dataframe = str(df_stem.apply(remove_stopwords))

    return dataframe