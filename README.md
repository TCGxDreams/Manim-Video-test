# Manim AI Studio - Studio Sản xuất Video Tự động với Google Gemini

Dự án này là một hệ thống AI đa tác nhân tự trị có khả năng biến một câu lệnh (prompt) thành một video hoạt hình hoàn chỉnh, được cung cấp sức mạnh bởi các mô hình Google Gemini. Hệ thống bao gồm hình ảnh từ Manim, lời thoại do AI tạo ra và ghép nối thành phẩm.

## Kiến trúc

Hệ thống sử dụng `crewAI` để điều phối một nhóm các AI Agent chuyên biệt, tất cả đều sử dụng Gemini làm bộ não trung tâm.

## Yêu cầu Hệ thống

Bạn cần cài đặt các công cụ sau trên hệ thống của mình:

1.  **Python 3.10+**
2.  **Manim:** Làm theo [hướng dẫn cài đặt chính thức của Manim Community](https://docs.manim.community/en/stable/installation.html).
3.  **FFmpeg:** Một công cụ dòng lệnh để xử lý video và audio.
    *   Trên macOS: `brew install ffmpeg`
    *   Trên Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
    *   Trên Windows: Tải từ [trang web chính thức](https://ffmpeg.org/download.html) và thêm vào biến môi trường PATH.

## Hướng dẫn Cài đặt

1.  **Clone repository này.**

2.  **Tạo và kích hoạt môi trường ảo:**
    ```bash
    python -m venv manim
    source manim/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Thiết lập Google Gemini API Key:**
    *   Truy cập [Google AI Studio](https://aistudio.google.com/app/apikey) để tạo API Key của bạn.
    *   **Quan trọng:** Bạn cũng cần phải [bật "Generative Language API"](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com) trong Google Cloud project của bạn.
    *   Sao chép tệp `.env.example` thành `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Mở tệp `.env` và điền `GOOGLE_API_KEY` và `SERPER_API_KEY` của bạn.

## Cách Chạy

Sau khi hoàn tất cài đặt, chỉ cần chạy tệp `main.py`:

```bash
python main.py
```

Các tệp tin tạm thời và video cuối cùng sẽ được lưu trong thư mục `workspace/`.