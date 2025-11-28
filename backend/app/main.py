# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from processing import clean_text, tokenize_and_lemmas, stems_from_tokens, freq_words, freq_ngrams, text_get_ngrams_by_vectorizer
import model_setup

# ensure model present at startup
model_setup.ensure_spacy_model()

app = FastAPI(title="Text Processing API")

# Allow CORS from frontend (adjust origin for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    text: str
    top_k: Optional[int] = 30
    use_vectorizer_for_ngrams: Optional[bool] = False

@app.post("/process")
def process(req: ProcessRequest):
    if not req.text or req.text.strip() == "":
        raise HTTPException(status_code=422, detail="Empty text")
    cleaned = clean_text(req.text)
    tokens, lemmas = tokenize_and_lemmas(cleaned)
    stems = stems_from_tokens(tokens)
    top_k = req.top_k or 30

    words_freq = freq_words(tokens, top_k)
    bigrams = freq_ngrams(tokens, 2, top_k)
    trigrams = freq_ngrams(tokens, 3, top_k)

    # vectorizer option (sometimes better for multiword tokens)
    if req.use_vectorizer_for_ngrams:
        bigrams = text_get_ngrams_by_vectorizer(cleaned, 2, top_k)
        trigrams = text_get_ngrams_by_vectorizer(cleaned, 3, top_k)

    # prepare JSON serializable output
    def pair_to_json(pair):
        if isinstance(pair[0], tuple):
            # For ngrams from freq_ngrams (tuples)
            return {"ngram": " ".join(pair[0]), "count": pair[1]}
        elif isinstance(pair[0], str):
            # For ngrams from vectorizer (strings)
            return {"ngram": pair[0], "count": pair[1]}
        else:
            return {"term": pair[0], "count": pair[1]}

    return {
        "cleaned_text": cleaned,
        "tokens": tokens,
        "lemmas": lemmas,
        "stems": stems,
        "top_words": [{"term": w, "count": c} for w, c in words_freq],
        "top_bigrams": [pair_to_json(p) for p in bigrams],
        "top_trigrams": [pair_to_json(p) for p in trigrams],
    }