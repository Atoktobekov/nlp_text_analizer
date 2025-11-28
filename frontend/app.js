// frontend/app.js
// Автоопределение URL бэкенда (работает и локально, и в Docker)
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? "http://localhost:8000/process"
    : `${window.location.protocol}//${window.location.hostname}:8000/process`;

document.getElementById("processBtn").addEventListener("click", async () => {
    const text = document.getElementById("inputText").value;
    const topK = Number(document.getElementById("topK").value) || 20;
    const useVectorizer = false;//document.getElementById("useVectorizer").checked;

    if (!text.trim()) {
        alert("Insert text.");
        return;
    }

    const payload = { text, top_k: topK, use_vectorizer_for_ngrams: useVectorizer };

    try {
        toggleButton(true);
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Server error");
        }
        const data = await res.json();
        showResult(data);
    } catch (e) {
        alert("Ошибка: " + e.message);
        console.error(e);
    } finally {
        toggleButton(false);
    }
});

function toggleButton(disable) {
    const btn = document.getElementById("processBtn");
    btn.disabled = disable;
    btn.textContent = disable ? "Processing..." : "Process";
}

function showResult(data) {
    document.getElementById("cleaned").textContent = "Cleaned: " + data.cleaned_text.slice(0, 1000);
    
    const wordsList = document.getElementById("wordsList");
    wordsList.innerHTML = "";
    data.top_words.forEach(w => {
        const li = document.createElement("li");
        li.textContent = `${w.term} — ${w.count}`;
        wordsList.appendChild(li);
    });

    const bigramsList = document.getElementById("bigramsList");
    bigramsList.innerHTML = "";
    data.top_bigrams.forEach(b => {
        const li = document.createElement("li");
        // Универсальный доступ к данным ngram
        const ngramText = b.ngram || b.term;
        li.textContent = ngramText + " — " + b.count;
        bigramsList.appendChild(li);
    });

    const trigramsList = document.getElementById("trigramsList");
    trigramsList.innerHTML = "";
    data.top_trigrams.forEach(t => {
        const li = document.createElement("li");
        // Универсальный доступ к данным ngram
        const ngramText = t.ngram || t.term;
        li.textContent = ngramText + " — " + t.count;
        trigramsList.appendChild(li);
    });

    document.getElementById("tokens").textContent = data.tokens.slice(0, 200).join(", ");
}