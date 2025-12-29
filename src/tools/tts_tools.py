import os
from mutagen.mp3 import MP3
from gtts import gTTS
from langchain.tools import BaseTool 

class TextToSpeechTool(BaseTool):
    """Enhanced TTS tool với nhiều tính năng hơn."""
    
    name: str = "Text to Speech Tool"
    description: str = (
        "Converts text into an MP3 audio file using Google Text-to-Speech. "
        "Arguments: text (str) - text to convert, file_name (str, default='voiceover.mp3'), "
        "language (str, default='auto') - 'en', 'vi', or 'auto' for auto-detection, "
        "slow (bool, default=False) - slower speech speed. "
        "Returns the file path and audio duration in seconds."
    )

    # Các pattern để detect ngôn ngữ
    VIETNAMESE_CHARS = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')

    def _detect_language(self, text: str) -> str:
        """Tự động phát hiện ngôn ngữ dựa trên ký tự."""
        text_chars = set(text)
        if text_chars & self.VIETNAMESE_CHARS:
            return 'vi'
        return 'en'

    def _get_audio_duration(self, file_path: str) -> float:
        """Lấy thời lượng file MP3 bằng mutagen."""
        try:
            audio = MP3(file_path)
            return audio.info.length
        except Exception:
            return 0.0

    def _run(
        self, 
        text: str, 
        file_name: str = "voiceover.mp3",
        language: str = "auto",
        slow: bool = False
    ) -> str:
        workspace_dir = "workspace"
        file_path = os.path.join(workspace_dir, file_name)
        
        try:
            os.makedirs(workspace_dir, exist_ok=True)
            
            # Auto-detect language nếu cần
            if language == "auto":
                language = self._detect_language(text)
            
            # Validate language
            supported_langs = ['en', 'vi', 'fr', 'de', 'es', 'it', 'ja', 'ko', 'zh-CN', 'zh-TW']
            if language not in supported_langs:
                language = 'en'
            
            # Tạo audio với gTTS
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(file_path)
            
            # Lấy thời lượng
            duration = self._get_audio_duration(file_path)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"✅ Audio file saved successfully!\n"
                f"📁 Path: {file_path}\n"
                f"🌐 Language: {language}\n"
                f"⏱️ Duration: {duration_str}"
            )
            
        except Exception as e:
            return f"❌ Error generating audio file: {e}"


class EnhancedTTSTool(BaseTool):
    """TTS tool với tùy chọn tốc độ và ngữ điệu."""
    
    name: str = "Enhanced Text to Speech Tool"
    description: str = (
        "Advanced text-to-speech with speed control. "
        "Arguments: text (str), file_name (str), language (str, default='auto'), "
        "speed (float, default=1.0) - speech speed multiplier (0.5 to 2.0). "
        "Note: Speed adjustment requires ffmpeg."
    )

    VIETNAMESE_CHARS = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')

    def _detect_language(self, text: str) -> str:
        text_chars = set(text)
        if text_chars & self.VIETNAMESE_CHARS:
            return 'vi'
        return 'en'

    def _get_audio_duration(self, file_path: str) -> float:
        try:
            audio = MP3(file_path)
            return audio.info.length
        except Exception:
            return 0.0

    def _run(
        self, 
        text: str, 
        file_name: str = "voiceover.mp3",
        language: str = "auto",
        speed: float = 1.0
    ) -> str:
        import subprocess
        
        workspace_dir = "workspace"
        temp_file = os.path.join(workspace_dir, "temp_audio.mp3")
        final_file = os.path.join(workspace_dir, file_name)
        
        try:
            os.makedirs(workspace_dir, exist_ok=True)
            
            # Auto-detect language
            if language == "auto":
                language = self._detect_language(text)
            
            # Tạo audio ban đầu
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Nếu không cần điều chỉnh tốc độ
            if abs(speed - 1.0) < 0.01:
                tts.save(final_file)
            else:
                # Lưu file tạm và điều chỉnh tốc độ bằng ffmpeg
                tts.save(temp_file)
                
                # Giới hạn speed trong khoảng hợp lý
                speed = max(0.5, min(2.0, speed))
                
                # Sử dụng atempo filter (chỉ hỗ trợ 0.5-2.0)
                command = [
                    "ffmpeg", "-y",
                    "-i", temp_file,
                    "-filter:a", f"atempo={speed}",
                    final_file
                ]
                
                subprocess.run(command, capture_output=True, check=True)
                
                # Xóa file tạm
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            duration = self._get_audio_duration(final_file)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"✅ Audio file generated!\n"
                f"📁 Path: {final_file}\n"
                f"🌐 Language: {language}\n"
                f"⚡ Speed: {speed}x\n"
                f"⏱️ Duration: {duration_str}"
            )
            
        except Exception as e:
            # Cleanup temp file on error
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return f"❌ Error generating audio file: {e}"