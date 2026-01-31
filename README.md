# Manim AI Studio

AI-powered automated video production system for mathematical animations.
He thong AI tu dong san xuat video hoat hinh toan hoc.

Using Google Gemini and Manim Community. Supports English and Vietnamese.
Su dung Google Gemini va Manim Community. Ho tro tieng Anh va tieng Viet.

## Overview / Tong quan

This project transforms a simple prompt into a complete animated video:
Du an nay bien mot cau lenh don gian thanh video hoat hinh hoan chinh:

- **Storyteller Agent**: Writes video script / Viet kich ban video
- **Manim Developer Agent**: Writes Manim code / Viet code Manim
- **QA Agent**: Tests and fixes code errors / Kiem tra va sua loi code
- **Voiceover Agent**: Creates TTS voiceover / Tao loi thoai TTS
- **Production Agent**: Merges video + audio / Ghep video + audio

## Requirements / Yeu cau

- Python 3.10+
- Node.js 18+ (for web UI)
- Manim Community v0.18+
- FFmpeg
- Google Gemini API Key
- Serper API Key (optional / tuy chon)

## Installation / Cai dat

```bash
# Clone repo
git clone https://github.com/TCGxDreams/Manim-Video-test.git
cd Manim-Video-test

# Create virtual environment / Tao moi truong ao
python -m venv manim
source manim/bin/activate  # Windows: manim\Scripts\activate

# Install Python dependencies / Cai dat thu vien Python
pip install -r requirements.txt

# Install Web UI dependencies / Cai dat thu vien Web UI
cd web && npm install && cd ..

# Configure API Keys / Cau hinh API Keys
cp .env.example .env
# Fill in GOOGLE_API_KEY and SERPER_API_KEY in .env file
```

## Usage / Su dung

### Option 1: Web UI (Recommended / De xuat)

Start both backend and frontend:

```bash
# Terminal 1: Start API server
python api/server.py

# Terminal 2: Start Web UI
cd web && npm run dev
```

Open http://localhost:5173 in your browser.

### Option 2: Command Line / Dong lenh

```bash
python main.py
```

Edit `video_topic` in `main.py` to change the topic.

## Web UI Features / Tinh nang Web UI

- Input video topic / Nhap chu de video
- Select language (English/Vietnamese) / Chon ngon ngu
- Select duration (1 min / 3 min) / Chon thoi luong
- Real-time progress tracking / Theo doi tien trinh thoi gian thuc
- Video preview and download / Xem truoc va tai video

## Project Structure / Cau truc du an

```
manim_ai_studio/
├── main.py              # CLI entry point
├── api/
│   └── server.py        # Flask backend API
├── web/                 # React frontend
│   ├── src/
│   │   ├── App.jsx      # Main component
│   │   └── App.css      # Styles
│   └── package.json
├── src/
│   ├── agents.py        # AI Agents + Manim Handbook
│   ├── tasks.py         # Task definitions
│   └── tools/           # Tools (file, manim, tts)
├── workspace/           # Output directory (gitignored)
└── requirements.txt
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Start video generation |
| `/api/status/<id>` | GET | Get generation status |
| `/api/videos` | GET | List generated videos |
| `/api/videos/<name>` | GET | Download video file |
| `/api/health` | GET | Health check |

## Manim Handbook / So tay Manim

Manim code follows rules in `MANIM_HANDBOOK` (agents.py):

- **DO NOT use / KHONG dung**: `get_tangent_line()` (not in Manim Community)
- **USE / DUNG**: `axes.plot()`, `MathTex()`, `Transform()`, `VGroup()`
- **Color palette / Bang mau**: TEAL_E (graph), GOLD_E (highlight), BLUE_E (area)

## License

MIT