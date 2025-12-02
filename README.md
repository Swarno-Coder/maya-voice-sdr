<div align="center">

# 🎙️ Maya Voice SDR

### AI-Powered Sales Development Representative

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![LiveKit](https://img.shields.io/badge/LiveKit-Powered-purple.svg)](https://livekit.io/)

<p align="center">
  <strong>Experience the future of B2B sales with Maya — your AI-powered voice assistant that engages prospects naturally, qualifies leads intelligently, and never sleeps.</strong>
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

### 🎨 Modern UI/UX
- Fluid gradient animations
- Glass morphism design
- Dark/Light mode support
- Responsive layout

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
├── 📁 backend/              # Python LiveKit Agent
│   ├── agent.py             # Maya AI Agent logic
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
│
├── 📁 frontend/             # Next.js 15 Application
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── styles/              # Global styles
│   └── package.json         # Node dependencies
│
├── .gitignore
├── LICENSE
└── README.md
```

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

### 3️⃣ Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Configure environment
cp .env.example .env
# Edit .env with your LiveKit credentials
```

### 4️⃣ Run the Application

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
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python agent.py start`
4. Add environment variables
5. Deploy!

---

## 🎭 Maya's Personality

Maya is designed to be:

- **Warm & Confident** — Builds rapport naturally
- **Genuinely Curious** — Asks thoughtful questions
- **Professional** — Maintains appropriate boundaries
- **Adaptive** — Adjusts pace to the prospect
- **Honest** — Never overpromises

### Conversation Strategy

```
1. 👋 Friendly greeting & introduction
2. 👂 Active listening for pain points
3. ❓ One thoughtful question at a time
4. 💡 Value proposition alignment
5. 📅 Meeting scheduling (if qualified)
```

---

## 🛡️ Guardrails

Maya is programmed with safety measures:

- ✅ Professional and respectful interactions
- ✅ Graceful handling of disinterested prospects
- ✅ Honest about product capabilities
- ✅ Privacy-conscious data handling
- ✅ Never reveals AI nature

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
