# 🎬 CineFace — Actor Recognition System

CineFace lets you find out which English speaking actor looks most like you. It builds a database of above a thousand of popular actors using TMDB API, generates facial embeddings with InsightFace, and finds the closest match using cosine similarity search in PostgreSQL.

---

## 🧠 How It Works

1. **Data ingestion** — Popular English-speaking actors are fetched from the TMDB API (up to 300 pages ≈ 1,000 actors). Their profile photos are downloaded and facial embeddings are generated using the `buffalo_l` InsightFace model.
2. **Storage** — Embeddings are stored in a PostgreSQL database with an **HNSW index** (`pgvector`) for fast cosine similarity search.
3. **Recognition** — Given a photo and a name, the system generates an embedding for the provided face and queries the database for the closest match, returning the actor's name and a similarity score.

```
Your Photo → InsightFace (buffalo_l) → Embedding → pgvector cosine search → Closest Actor Match
```

---

## 📁 Project Structure

```
.
├── API_connector.py    # TMDB scraper — populates the database with actor embeddings
├── db_connector.py     # PostgreSQL interface (add, fetch, search embeddings)
├── embeddings.py       # Person class — photo fetching & embedding generation
├── face_detecting.py   # Entry point — run recognition on a photo
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
└── README.md
```

---

## ⚙️ Requirements

- Python 3.12
- PostgreSQL with [`pgvector`](https://github.com/pgvector/pgvector) extension
- CUDA-capable GPU *(recommended for embedding generation speed)*

### Python dependencies

```bash
pip install -r requirements.txt
```

> For CPU-only usage, replace `onnxruntime-gpu` with `onnxruntime`.

---

## 🗄️ Database Setup

```sql
-- Enable pgvector extension
CREATE EXTENSION vector;

-- Create actors table
CREATE TABLE actors (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    last_name   VARCHAR(100),
    embedding   vector(512),
    popularity  FLOAT
);

-- Create HNSW index for fast cosine similarity search
CREATE INDEX ON actors USING hnsw (embedding vector_cosine_ops);
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your_tmdb_api_key

DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

Get your TMDB API key at [themoviedb.org](https://www.themoviedb.org/settings/api).

---

## 🚀 Usage

### 1. Populate the database

```bash
python API_connector.py
```

This fetches up to 300 pages of popular actors from TMDB (~1,000 entries) and stores their facial embeddings in the database (it may take a while)

### 2. Identify a person from a photo

```bash
python face_detecting.py "FirstName LastName" path/to/photo.jpg
```

**With a popularity threshold:**

```bash
python face_detecting.py "FirstName LastName" path/to/photo.jpg 5.0
```

**Example output:**

```
Found closest match: Tom Hanks with similarity 91.34%
```

> **Popularity threshold** — values range from ~3.4 to ~50. Higher values narrow the search to more famous actors. The top 5 popularity scores in the dataset are: 50.42, 35.21, 24.82, 23.56, 21.67.

---

## 📌 Notes

- Only **English-language** actors with a profile photo are included in the database.
- Only actors with a **popularity score above 3.4** are considered during ingestion.
- The system currently assumes **one face per photo**. If multiple faces are detected, only the first one is used.
- Names are split on spaces and apostrophes (e.g. *O'Brien* → name: `O`, last name: `Brien`). Consider extending `divide_into_parts()` for edge cases.

---

## 📄 License

MIT
