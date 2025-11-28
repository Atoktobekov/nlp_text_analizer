# backend/app/processing.py
import re
from collections import Counter
from typing import List, Tuple

import spacy
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk import ngrams
import nltk

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# load spaCy model (should be loaded once by app)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
ps = PorterStemmer()

# cleaning function
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    # keep letters and spaces (english). If you need other languages, tweak regex.
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_and_lemmas(text: str) -> Tuple[List[str], List[str]]:
    doc = nlp(text)
    tokens = []
    lemmas = []
    for token in doc:
        if token.is_space:
            continue
        if token.is_punct:
            continue
        if token.like_num:
            continue
        if token.is_stop:
            continue
        txt = token.text.strip()
        if txt == "":
            continue
        tokens.append(txt)
        lemmas.append(token.lemma_.strip())
    return tokens, lemmas

def stems_from_tokens(tokens: List[str]) -> List[str]:
    return [ps.stem(t) for t in tokens]

def freq_words(tokens: List[str], top_k: int = 50):
    return Counter(tokens).most_common(top_k)

def freq_ngrams(tokens: List[str], n: int = 2, top_k: int = 50):
    if len(tokens) < n:
        return []
    # build ngrams from token list
    ng = ngrams(tokens, n)
    return Counter(ng).most_common(top_k)

def text_get_ngrams_by_vectorizer(text: str, n: int = 2, top_k: int = 50):
    # alternative: CountVectorizer on cleaned string (useful for multi-word ngrams)
    vect = CountVectorizer(ngram_range=(n, n))
    X = vect.fit_transform([text])
    names = vect.get_feature_names_out()
    counts = X.toarray()[0]
    pairs = list(zip(names, counts))
    pairs.sort(key=lambda x: x[1], reverse=True)
    return pairs[:top_k]