# Product Price Fetcher (Amazon Scraper + Gemini Filter) 🛍️

This app scrapes product listings from Amazon India/US and uses **Gemini LLM** to filter for exact matches using natural language prompts.

## 🚀 Features

- Scrape real-time prices from Amazon
- Match relevant results using Gemini LLM
- FastAPI-powered API
- AI filtering via Google Gemini (`gemini-1.5-pro-latest`)
- Docker-ready and productionizable

## 📂 Folder Structure

```plaintext
├── app/
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   ├── matcher.py
│   ├── schemas.py
│   ├── scraper.py
│   └── logger.py
│
├── .gitignore
│
├── README.md
│
└── requirements.txt
```

## ⚙️ Requirements

- Python 3.7 or higher
- FastAPI
- httpx
- beautifulsoup4
- Google Gemini API access (`gemini-1.5-pro-latest`)

## 🛠️ Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/APMAPM1/Product-Price-Fetcher.git
   cd Product-Price-Fetcher
   ```
2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your API Key:**

   ```bash
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

5. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 📡 Example API Usage

### Endpoint:

```bash
POST /search
```

### Example cURL Request:

```bash
curl -X POST http://127.0.0.1:8000/search \
-H "Content-Type: application/json" \
-d '{"country": "IN", "query": "boAt Airdopes 311 Pro"}'
```

### Example Response:

```bash
[
   {
     "productName": "boAt Airdopes 311 Pro, 50HRS Battery, Fast Charge, ...",
     "price": 999.0,
     "currency": "INR",
     "link": "https://www.amazon.in/dp/B0C8ZTPM29"
   }
]
```

## 🧠 Notes

- Uses beautifulsoup4 to scrape Amazon results.
- Uses Gemini (gemini-1.5-pro-latest) to rank matching results.
- Handles rate limit errors, but you may need to upgrade Gemini quota for production.
