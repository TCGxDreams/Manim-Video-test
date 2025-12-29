# Manim AI Studio

Hệ thống AI tự động sản xuất video toán học hoạt hình, sử dụng Google Gemini và Manim Community.

## Tổng quan

Dự án biến một câu lệnh đơn giản thành video hoạt hình hoàn chỉnh:
- **Storyteller Agent**: Viết kịch bản video
- **Manim Developer Agent**: Viết code Manim 
- **QA Agent**: Kiểm tra và fix lỗi code
- **Voiceover Agent**: Tạo lời thoại TTS
- **Production Agent**: Ghép video + audio

## Yêu cầu

- Python 3.10+
- Manim Community v0.18+
- FFmpeg
- Google Gemini API Key
- Serper API Key (tùy chọn)

## Cài đặt

```bash
# Clone repo
git clone https://github.com/TCGxDreams/Manim-Video-test.git
cd Manim-Video-test

# Tạo virtual environment
python -m venv manim
source manim/bin/activate  # Windows: manim\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Cấu hình API Keys
cp .env.example .env
# Điền GOOGLE_API_KEY và SERPER_API_KEY vào file .env
```

## Sử dụng

```bash
python main.py
```

Video sẽ được tạo trong thư mục `workspace/`:
- `video_script.txt` - Kịch bản
- `manim_animation.py` - Code Manim
- `animation_scene.mp4` - Video gốc
- `voiceover.mp3` - Audio
- `final_video.mp4` - Video hoàn chỉnh

## Tùy chỉnh

### Thay đổi chủ đề video
Sửa `video_topic` trong `main.py`:
```python
video_topic = "Tên chủ đề của bạn"
```

### Thay đổi thời lượng
Sửa trong `src/tasks.py`:
- 130-150 từ voiceover = ~1 phút video
- 400-450 từ voiceover = ~3 phút video

### Model LLM
Sửa trong `main.py`:
```python
llm_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_pro = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
```

## Cấu trúc thư mục

```
manim_ai_studio/
├── main.py              # Entry point
├── src/
│   ├── agents.py        # Định nghĩa AI Agents + Manim Handbook
│   ├── tasks.py         # Định nghĩa Tasks
│   └── tools/
│       ├── file_tools.py    # File I/O tools
│       ├── manim_tools.py   # Manim + FFmpeg tools
│       └── tts_tools.py     # Text-to-Speech tools
├── workspace/           # Output directory (gitignored)
└── requirements.txt
```

## Manim Handbook

Code Manim tuân theo các quy tắc trong `MANIM_HANDBOOK` (agents.py):
- Không dùng `get_tangent_line()` (không có trong Manim Community)
- Dùng `axes.plot()`, `MathTex()`, `Transform()`, `VGroup()`
- Color palette: TEAL_E (graph), GOLD_E (highlight), BLUE_E (area)

## License

MIT