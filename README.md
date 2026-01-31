# 🎬 Manim AI Studio

> AI-powered automated video production system for mathematical animations using Google Gemini and Manim Community.

![Manim AI Studio](https://img.shields.io/badge/Manim-Community%20v0.18-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🤖 **AI-Powered Script Writing** - Gemini creates educational video scripts
- 🎨 **3Blue1Brown Style Animations** - Professional math animations with Manim
- 🔄 **Auto Error Recovery** - QA agent automatically fixes code errors
- 🎙️ **Text-to-Speech** - Automatic voiceover generation (English/Vietnamese)
- 🎬 **Video Production** - FFmpeg merges video and audio
- 🌐 **Web UI** - Modern React interface for easy usage
- ☁️ **Cloud Ready** - Docker + Railway/Vercel deployment

---

## 📋 Requirements

- Python 3.10+
- Node.js 18+ (for web UI)
- Manim Community v0.18+
- FFmpeg
- LaTeX (for mathematical symbols)

### API Keys

- **Google Gemini API Key** - [Get it here](https://makersuite.google.com/app/apikey)
- **Serper API Key** (optional) - [Get it here](https://serper.dev/)

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/TCGxDreams/Manim-Video-test.git
cd Manim-Video-test

# Create virtual environment
python -m venv manim
source manim/bin/activate  # Windows: manim\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Web UI dependencies
cd web && npm install && cd ..
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 3. Run

**Option A: Web UI (Recommended)**
```bash
# Terminal 1: Start API server
python api/server.py

# Terminal 2: Start Web UI
cd web && npm run dev
```

Open http://localhost:5173

**Option B: Command Line**
```bash
python main.py
```

---

## 🖥️ Web UI

Modern dark theme interface with:

- **Topic Input** - Enter video topic (English or Vietnamese)
- **Language Selector** - Choose output language
- **Duration Selector** - 1 minute or 3 minutes video
- **Progress Tracker** - Real-time progress updates
- **Video List** - View and download generated videos

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web UI (React)                       │
│                     http://localhost:5173                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask API Server                         │
│                     http://localhost:5001                   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────────┐   ┌─────────────┐
│  Storyteller  │   │  Manim Developer  │   │     QA      │
│     Agent     │   │      Agent        │   │   Engineer  │
│   (Script)    │   │     (Code)        │   │   (Test)    │
└───────────────┘   └───────────────────┘   └─────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────────┐   ┌─────────────┐
│   Voiceover   │   │    Production     │   │   Output    │
│    Artist     │   │     Engineer      │   │   Video     │
│    (TTS)      │   │  (FFmpeg Merge)   │   │   (.mp4)    │
└───────────────┘   └───────────────────┘   └─────────────┘
```

---

## 📁 Project Structure

```
manim_ai_studio/
├── main.py              # CLI entry point
├── api/
│   └── server.py        # Flask backend API
├── web/                 # React frontend
│   ├── src/
│   │   ├── App.jsx      # Main component
│   │   └── App.css      # Styles
│   ├── vercel.json      # Vercel config
│   └── package.json
├── src/
│   ├── agents.py        # AI Agents + MANIM_HANDBOOK
│   ├── tasks.py         # Task definitions
│   └── tools/
│       ├── file_tools.py    # File R/W tools
│       ├── manim_tools.py   # Manim + FFmpeg tools
│       └── tts_tools.py     # Text-to-Speech tools
├── workspace/           # Output directory (gitignored)
├── Dockerfile           # Docker config for deployment
├── railway.toml         # Railway config
└── requirements.txt
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Start video generation |
| `/api/status/<id>` | GET | Get generation status |
| `/api/videos` | GET | List generated videos |
| `/api/videos/<name>` | GET | Download video file |
| `/api/health` | GET | Health check |

### Example Request

```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Basic Derivatives", "language": "en", "duration": 1}'
```

---

## ☁️ Cloud Deployment

### Option 1: Railway (Backend) + Vercel (Frontend)

**Deploy Backend to Railway:**

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select repo: `TCGxDreams/Manim-Video-test`
4. Add environment variables:
   - `GOOGLE_API_KEY`
   - `SERPER_API_KEY`
5. Deploy → Get URL (e.g., `https://manim-xxx.railway.app`)

**Deploy Frontend to Vercel:**

1. Go to https://vercel.com
2. "Import" → Select GitHub repo
3. Root Directory: `web`
4. Add environment variable:
   - `VITE_API_URL` = `https://manim-xxx.railway.app/api`
5. Deploy

### Option 2: Docker (Self-hosted)

```bash
# Build
docker build -t manim-studio .

# Run
docker run -p 5001:5001 \
  -e GOOGLE_API_KEY=your_key \
  -e SERPER_API_KEY=your_key \
  manim-studio
```

---

## 🎨 MANIM_HANDBOOK

The AI agents follow strict rules defined in `MANIM_HANDBOOK`:

### Color Palette (3Blue1Brown Style)
```python
TEAL_E = "#49A88F"   # Graphs
GOLD_E = "#C78D46"   # Highlights
BLUE_E = "#1C758A"   # Areas
GREY_A = "#DDDDDD"   # Axes
```

### Allowed Methods
- ✅ `axes.plot()` - Draw graphs
- ✅ `MathTex()`, `Text()` - Mathematical formulas
- ✅ `Create()`, `Write()`, `FadeOut()` - Animations
- ✅ `Transform()`, `ReplacementTransform()`
- ✅ `VGroup().arrange()` - Group objects

### Forbidden Methods
- ❌ `get_tangent_line()` - Not in Manim Community
- ❌ `always_redraw()` with complex logic
- ❌ Complex `ValueTracker` animations

---

## 📊 Output Files

All files are saved to `workspace/`:

| File | Description |
|------|-------------|
| `video_script.txt` | Generated script |
| `manim_animation.py` | Manim source code |
| `animation_scene.mp4` | Silent video |
| `voiceover.mp3` | TTS audio |
| `final_video.mp4` | Final merged video |

---

## 🔧 Configuration

### Change Video Duration

Edit `src/tasks.py`:
- 130-150 words → ~1 minute video
- 400-450 words → ~3 minute video

### Change LLM Models

Edit `main.py` or `api/server.py`:
```python
llm_flash = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
llm_pro = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 in use | macOS AirPlay uses 5000. We use 5001 instead. |
| LaTeX errors | Install full texlive: `brew install texlive` |
| FFmpeg not found | Install FFmpeg: `brew install ffmpeg` |
| API timeout | Increase retry count or use faster models |

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

---

## 🙏 Credits

- **Manim Community** - Animation engine
- **Google Gemini** - AI language models
- **3Blue1Brown** - Animation style inspiration
- **gTTS** - Text-to-Speech
- **FFmpeg** - Video processing

---

Made with ❤️ for math education