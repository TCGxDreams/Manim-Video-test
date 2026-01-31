# Manim AI Studio

AI-powered automated video production system for mathematical animations, using Google Gemini and Manim Community.

## Overview

This project transforms a simple prompt into a complete animated video:
- **Storyteller Agent**: Writes video script
- **Manim Developer Agent**: Writes Manim code 
- **QA Agent**: Tests and fixes code errors
- **Voiceover Agent**: Creates TTS voiceover
- **Production Agent**: Merges video + audio

## Requirements

- Python 3.10+
- Manim Community v0.18+
- FFmpeg
- Google Gemini API Key
- Serper API Key (optional)

## Installation

```bash
# Clone repo
git clone https://github.com/TCGxDreams/Manim-Video-test.git
cd Manim-Video-test

# Create virtual environment
python -m venv manim
source manim/bin/activate  # Windows: manim\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API Keys
cp .env.example .env
# Fill in GOOGLE_API_KEY and SERPER_API_KEY in .env file
```

## Usage

```bash
python main.py
```

Output files are created in `workspace/`:
- `video_script.txt` - Script
- `manim_animation.py` - Manim code
- `animation_scene.mp4` - Raw video
- `voiceover.mp3` - Audio
- `final_video.mp4` - Final video

## Configuration

### Change video topic
Edit `video_topic` in `main.py`:
```python
video_topic = "Your topic here"
```

### Change duration
Edit in `src/tasks.py`:
- 130-150 words voiceover = ~1 minute video
- 400-450 words voiceover = ~3 minute video

### LLM Models
Edit in `main.py`:
```python
llm_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_pro = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
```

## Project Structure

```
manim_ai_studio/
├── main.py              # Entry point
├── src/
│   ├── agents.py        # AI Agents + Manim Handbook
│   ├── tasks.py         # Task definitions
│   └── tools/
│       ├── file_tools.py    # File I/O tools
│       ├── manim_tools.py   # Manim + FFmpeg tools
│       └── tts_tools.py     # Text-to-Speech tools
├── workspace/           # Output directory (gitignored)
└── requirements.txt
```

## Manim Handbook

Manim code follows rules in `MANIM_HANDBOOK` (agents.py):
- DO NOT use `get_tangent_line()` (not in Manim Community)
- USE `axes.plot()`, `MathTex()`, `Transform()`, `VGroup()`
- Color palette: TEAL_E (graph), GOLD_E (highlight), BLUE_E (area)

## License

MIT