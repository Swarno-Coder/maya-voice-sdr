<div align="center">

# 🎙️ Maya Voice SDR

### AI-Powered Sales Development Representative with RAG Knowledge Base

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![LiveKit](https://img.shields.io/badge/LiveKit-Powered-purple.svg)](https://livekit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-orange.svg)](https://www.trychroma.com/)

<p align="center">
  <strong>Experience the future of B2B sales with Maya — your AI-powered voice assistant that engages prospects naturally, qualifies leads intelligently, and answers product questions from a real-time knowledge base.</strong>
</p>

[Live Demo](https://maya-voice-sdr.vercel.app) · [Report Bug](https://github.com/Swarno-Coder/maya-voice-sdr/issues) · [Request Feature](https://github.com/Swarno-Coder/maya-voice-sdr/issues)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🗣️ Natural Conversations

- Human-like voice interactions
- Adaptive conversational pace
- Natural speech patterns & fillers
- Real-time voice processing

</td>
<td width="50%">

### 🎯 Intelligent Qualification

- Smart lead qualification
- Pain point identification
- Tailored value propositions
- Meeting scheduling automation

</td>
</tr>
<tr>
<td width="50%">

### 🧠 RAG Knowledge Base

- Sub-50ms vector retrieval
- Dynamic context injection
- Product docs, pricing & case studies
- Extensible document ingestion

</td>
<td width="50%">

### ⚡ Enterprise Ready

- 24/7 availability
- Scalable architecture
- Privacy-focused
- Professional guardrails

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
maya-voice-sdr/
├── 📁 backend/                  # Python LiveKit Agent
│   ├── agent.py                 # Maya AI Agent with RAG integration
│   ├── rag_engine.py            # Low-latency RAG engine (ChromaDB + sentence-transformers)
│   ├── ingest.py                # Document ingestion pipeline CLI
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── 📁 knowledge_base/      # Source documents for RAG
│   │   ├── product_overview.md
│   │   ├── pricing_tiers.md
│   │   ├── case_studies.md
│   │   ├── faq.md
│   │   └── competitor_comparison.md
│   └── 📁 chroma_db/           # Vector store (auto-generated, git-ignored)
│
├── 📁 frontend/                 # Next.js 15 Application
│   ├── app/                     # App router pages
│   ├── components/              # React components
│   ├── styles/                  # Global styles
│   └── package.json             # Node dependencies
│
├── render.yaml                  # Render deployment config
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🧠 RAG Pipeline Architecture

Maya uses a **low-latency Retrieval-Augmented Generation** pipeline to ground conversations in real product knowledge:

```
┌─────────────┐    ┌─────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────┐
│  User Voice  │───▶│   STT   │───▶│  RAG Query   │───▶│ LLM + Context│───▶│   TTS   │
│  (LiveKit)   │    │ Assembly│    │  (<50ms)     │    │  (Gemini)   │    │ Cartesia│
└─────────────┘    └─────────┘    └──────┬───────┘    └─────────────┘    └─────────┘
                                         │
                                    ┌────▼────┐
                                    │ChromaDB │
                                    │ Vector  │
                                    │  Store  │
                                    └────┬────┘
                                         │
                                  ┌──────▼──────┐
                                  │ Sentence     │
                                  │ Transformers │
                                  │ Embeddings   │
                                  └──────────────┘
```

### How It Works

1. **Document Ingestion** — `.md`, `.txt`, `.pdf` files are chunked (512 tokens, 64 overlap) and embedded using `all-MiniLM-L6-v2`
2. **Vector Storage** — Embeddings are stored in ChromaDB with metadata (source, category) for filtered retrieval
3. **Real-Time Retrieval** — On each user turn, the agent queries the vector store (~15ms) and retrieves top-3 relevant chunks
4. **Context Injection** — Retrieved context is injected as a system message before the LLM generates a response
5. **Natural Response** — Maya weaves knowledge-base facts into conversation naturally, never revealing the RAG system

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **ChromaDB (in-process)** | Zero network latency — runs inside the agent process |
| **sentence-transformers** | Local CPU embedding in ~15ms, no API calls |
| **Cosine similarity + threshold** | Filters irrelevant results (distance > 0.75) to prevent hallucination |
| **Singleton pattern** | RAG engine initialized once in prewarm, shared across sessions |
| **Before-LLM callback** | Non-invasive integration — RAG enriches context without modifying agent logic |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **pnpm** (recommended) or npm
- **LiveKit Cloud** account ([Sign up free](https://cloud.livekit.io))

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Swarno-Coder/maya-voice-sdr.git
cd maya-voice-sdr
```

### 2️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your LiveKit credentials
```

### 3️⃣ Ingest Knowledge Base

```bash
# Ingest sample documents into the vector store
python ingest.py

# Or reset and re-ingest from scratch
python ingest.py --reset

# Or ingest from a custom directory
python ingest.py --dir /path/to/your/docs
```

### 4️⃣ Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Configure environment
cp .env.example .env
# Edit .env with your LiveKit credentials
```

### 5️⃣ Run the Application

**Terminal 1 - Backend:**

```bash
cd backend
python agent.py dev
```

**Terminal 2 - Frontend:**

```bash
cd frontend
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser 🎉

---

## 📚 Managing the Knowledge Base

### Adding Documents

Drop `.txt`, `.md`, or `.pdf` files into `backend/knowledge_base/` and run:

```bash
python ingest.py
```

The ingestion pipeline automatically:

- Detects file type and extracts text
- Chunks documents with overlap for context continuity
- Infers category tags from filenames (pricing, faq, case_study, competitor, product)
- Generates deterministic IDs for idempotent upserts (safe to re-run)

### Category Auto-Detection

| Filename contains | Category assigned |
|-------------------|-------------------|
| `pricing`, `plan` | `pricing` |
| `case`, `success`, `story` | `case_study` |
| `faq`, `question` | `faq` |
| `competitor`, `comparison`, `vs` | `competitor` |
| `product`, `feature`, `overview` | `product` |
| anything else | `general` |

### Resetting the Knowledge Base

```bash
python ingest.py --reset  # Wipes and re-ingests everything
```

---

## ⚙️ Configuration

### LiveKit Credentials

Get your credentials from [LiveKit Cloud](https://cloud.livekit.io):

| Variable | Description |
|----------|-------------|
| `LIVEKIT_API_KEY` | Your LiveKit API Key |
| `LIVEKIT_API_SECRET` | Your LiveKit API Secret |
| `LIVEKIT_URL` | WebSocket URL (e.g., `wss://your-app.livekit.cloud`) |

### AI Models (Backend)

Maya uses the following AI services (configurable in `agent.py`):

| Service | Model | Purpose |
|---------|-------|---------|
| **STT** | AssemblyAI Universal | Speech-to-Text |
| **LLM** | Google Gemini 2.5 Flash | Language Model |
| **TTS** | Cartesia Sonic 3 | Text-to-Speech |
| **Embeddings** | all-MiniLM-L6-v2 | RAG Vector Embeddings |
| **Vector DB** | ChromaDB | Knowledge Store |

### RAG Configuration (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `RAG_COLLECTION_NAME` | `maya_knowledge` | ChromaDB collection name |
| `RAG_TOP_K` | `3` | Number of chunks to retrieve per query |
| `RAG_CHUNK_SIZE` | `512` | Words per chunk during ingestion |
| `RAG_CHUNK_OVERLAP` | `64` | Overlap between chunks |
| `RAG_EMBED_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |

---

## 🌐 Deployment

### Frontend → Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Swarno-Coder/maya-voice-sdr&env=LIVEKIT_API_KEY,LIVEKIT_API_SECRET,LIVEKIT_URL)

1. Import repository to Vercel
2. Set environment variables
3. Deploy!

### Backend → Render

1. Create new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt && python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" && python ingest.py && python agent.py download-files`
   - **Start Command:** `python agent.py start`
4. Add environment variables
5. Deploy!

---

## 🎭 Maya's Personality

Maya is designed to be:

- **Warm & Confident** — Builds rapport naturally
- **Genuinely Curious** — Asks thoughtful questions
- **Knowledge-Grounded** — Answers with real product data from RAG
- **Professional** — Maintains appropriate boundaries
- **Adaptive** — Adjusts pace to the prospect
- **Honest** — Never overpromises

### Conversation Strategy

```
1. 👋 Friendly greeting & introduction
2. 👂 Active listening for pain points
3. ❓ One thoughtful question at a time
4. 🧠 RAG-powered product knowledge retrieval
5. 💡 Value proposition alignment with real data
6. 📅 Meeting scheduling (if qualified)
```

---

## 🛡️ Guardrails

Maya is programmed with safety measures:

- ✅ Professional and respectful interactions
- ✅ Graceful handling of disinterested prospects
- ✅ Honest about product capabilities
- ✅ Privacy-conscious data handling
- ✅ Never reveals AI nature
- ✅ RAG context used naturally, never referenced explicitly

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

<div align="center">

**Made with ❤️ by Swarnodip Nag**

[![GitHub](https://img.shields.io/badge/GitHub-Swarno--Coder-181717?style=for-the-badge&logo=github)](https://github.com/Swarno-Coder)

</div>

---

<div align="center">
<sub>If you found this project helpful, please consider giving it a ⭐</sub>
</div>
