# NLP Text Processor

Веб-приложение для обработки текста с использованием NLP: токенизация, лемматизация, стемминг, анализ n-грамм.

## 📁 Структура проекта

```
project/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── processing.py
│   │   ├── model_setup.py
│   │   └── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── docker-compose.yml
├── nginx.conf
├── .gitignore
└── README.md
```

## 🚀 Запуск проекта

### Вариант 1: Docker (рекомендуется)

**Требования:**
- Docker
- Docker Compose

**Запуск:**

```bash
# Сборка и запуск
docker-compose up --build

# В фоновом режиме
docker-compose up -d --build
```

**Доступ:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Остановка:**
```bash
docker-compose down
```

---

### Вариант 2: Локальный запуск

#### Backend

**Требования:**
- Python 3.11+
- pip

**Установка:**

```bash
cd backend/app

# Создать виртуальное окружение (опционально)
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Скачать модель spaCy
python -m spacy download en_core_web_sm

# Запустить сервер
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на http://localhost:8000

#### Frontend

**Простой способ (Python):**
```bash
cd frontend
python -m http.server 3000
```

**Или с Node.js:**
```bash
cd frontend
npx serve -p 3000
```

Frontend будет доступен на http://localhost:3000

---

## 🔧 Настройки

### Backend (main.py)

Измените CORS origins для продакшена:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # укажи свой домен
    ...
)
```

### Frontend (app.js)

URL бэкенда определяется автоматически, но можно задать вручную:
```javascript
const API_URL = "https://your-api-domain.com/process";
```

---

## 📝 API Эндпоинты

### POST /process

Обработка текста

**Request:**
```json
{
  "text": "Your text here",
  "top_k": 20,
  "use_vectorizer_for_ngrams": false
}
```

**Response:**
```json
{
  "cleaned_text": "cleaned text",
  "tokens": ["token1", "token2"],
  "lemmas": ["lemma1", "lemma2"],
  "stems": ["stem1", "stem2"],
  "top_words": [{"term": "word", "count": 5}],
  "top_bigrams": [{"ngram": "word1 word2", "count": 3}],
  "top_trigrams": [{"ngram": "word1 word2 word3", "count": 2}]
}
```

---

## 🐛 Troubleshooting

### spaCy модель не найдена
```bash
python -m spacy download en_core_web_sm
```

### NLTK данные не найдены
```python
import nltk
nltk.download('punkt')
```

### CORS ошибки
Проверь настройки CORS в `main.py` - должен быть разрешен origin фронтенда

### Docker проблемы
```bash
# Пересборка без кэша
docker-compose build --no-cache

# Проверка логов
docker-compose logs backend
docker-compose logs frontend
```

---

## 📦 Зависимости

**Backend:**
- FastAPI - веб-фреймворк
- spaCy - NLP обработка
- scikit-learn - векторизация
- NLTK - n-граммы и стемминг
- uvicorn - ASGI сервер

**Frontend:**
- Vanilla JavaScript
- HTML/CSS

---

## 🎯 Возможности

- ✅ Очистка текста от пунктуации и чисел
- ✅ Токенизация
- ✅ Лемматизация (spaCy)
- ✅ Стемминг (Porter Stemmer)
- ✅ Удаление стоп-слов
- ✅ Частотный анализ слов
- ✅ Анализ биграмм и триграмм
- ✅ Два метода для n-грамм (NLTK и CountVectorizer)

---

## 📄 Лицензия

MIT