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

# Install dependencies / Cai dat thu vien
pip install -r requirements.txt

# Configure API Keys / Cau hinh API Keys
cp .env.example .env
# Fill in GOOGLE_API_KEY and SERPER_API_KEY in .env file
# Dien GOOGLE_API_KEY va SERPER_API_KEY vao file .env
```

## Usage / Su dung

```bash
python main.py
```

### Change video topic / Thay doi chu de video:

Edit `video_topic` in `main.py` / Sua `video_topic` trong `main.py`:
```python
# English example:
video_topic = "Basic Derivatives - derivative of x^n, sin(x), e^x - 1 minute video"

# Vietnamese example / Vi du tieng Viet:
video_topic = "Dao ham co ban - 1 phut video tieng Viet"
```

### Output files:

All output files are created in `workspace/`:
Tat ca file output duoc tao trong `workspace/`:

- `video_script.txt` - Script / Kich ban
- `manim_animation.py` - Manim code
- `animation_scene.mp4` - Raw video / Video goc
- `voiceover.mp3` - Audio
- `final_video.mp4` - Final video / Video hoan chinh

## Configuration / Cau hinh

### Change duration / Thay doi thoi luong:
Edit in `src/tasks.py` / Sua trong `src/tasks.py`:
- 130-150 words voiceover = ~1 minute video / phut video
- 400-450 words voiceover = ~3 minute video / phut video

### LLM Models:
Edit in `main.py` / Sua trong `main.py`:
```python
llm_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_pro = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
```

## Project Structure / Cau truc du an

```
manim_ai_studio/
├── main.py              # Entry point / Diem khoi dau
├── src/
│   ├── agents.py        # AI Agents + Manim Handbook
│   ├── tasks.py         # Task definitions / Dinh nghia tasks
│   └── tools/
│       ├── file_tools.py    # File I/O tools
│       ├── manim_tools.py   # Manim + FFmpeg tools
│       └── tts_tools.py     # Text-to-Speech tools
├── workspace/           # Output directory (gitignored)
└── requirements.txt
```

## Manim Handbook / So tay Manim

Manim code follows rules in `MANIM_HANDBOOK` (agents.py):
Code Manim tuan theo cac quy tac trong `MANIM_HANDBOOK` (agents.py):

- **DO NOT use / KHONG dung**: `get_tangent_line()` (not in Manim Community)
- **USE / DUNG**: `axes.plot()`, `MathTex()`, `Transform()`, `VGroup()`
- **Color palette / Bang mau**: TEAL_E (graph), GOLD_E (highlight), BLUE_E (area)

## Language Support / Ho tro ngon ngu

The system automatically detects language:
He thong tu dong phat hien ngon ngu:

- TTS tool auto-detects English/Vietnamese
- Manim tool can render Vietnamese text
- All logs are bilingual (English/Vietnamese)

## License

MIT