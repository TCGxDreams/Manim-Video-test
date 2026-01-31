import os
from mutagen.mp3 import MP3
from gtts import gTTS
from langchain.tools import BaseTool 

class TextToSpeechTool(BaseTool):
    """Enhanced TTS tool with multiple features."""
    
    name: str = "Text to Speech Tool"
    description: str = (
        "Converts text into an MP3 audio file using Google Text-to-Speech. "
        "Arguments: text (str) - text to convert, file_name (str, default='voiceover.mp3'), "
        "language (str, default='auto') - 'en', 'vi', or 'auto' for auto-detection, "
        "slow (bool, default=False) - slower speech speed. "
        "Returns the file path and audio duration in seconds."
    )

    VIETNAMESE_CHARS = set('aeiouydAEIOUYD')

    def _detect_language(self, text: str) -> str:
        """Auto-detect language based on characters."""
        vietnamese_pattern = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
        for char in text:
            if char in vietnamese_pattern:
                return 'vi'
        return 'en'

    def _get_audio_duration(self, file_path: str) -> float:
        """Get MP3 file duration using mutagen."""
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
            
            # Auto-detect language if needed
            if language == "auto":
                language = self._detect_language(text)
            
            # Validate language
            supported_langs = ['en', 'vi', 'fr', 'de', 'es', 'it', 'ja', 'ko', 'zh-CN', 'zh-TW']
            if language not in supported_langs:
                language = 'en'
            
            # Create audio with gTTS
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(file_path)
            
            # Get duration
            duration = self._get_audio_duration(file_path)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"[OK] Audio file saved successfully!\n"
                f"Path: {file_path}\n"
                f"Language: {language}\n"
                f"Duration: {duration_str}"
            )
            
        except Exception as e:
            return f"[ERROR] Error generating audio file: {e}"


class EnhancedTTSTool(BaseTool):
    """TTS tool with speed and pitch control."""
    
    name: str = "Enhanced Text to Speech Tool"
    description: str = (
        "Advanced text-to-speech with speed control. "
        "Arguments: text (str), file_name (str), language (str, default='auto'), "
        "speed (float, default=1.0) - speech speed multiplier (0.5 to 2.0). "
        "Note: Speed adjustment requires ffmpeg."
    )

    def _detect_language(self, text: str) -> str:
        vietnamese_pattern = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
        for char in text:
            if char in vietnamese_pattern:
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
            
            # Create initial audio
            tts = gTTS(text=text, lang=language, slow=False)
            
            # If no speed adjustment needed
            if abs(speed - 1.0) < 0.01:
                tts.save(final_file)
            else:
                # Save temp file and adjust speed with ffmpeg
                tts.save(temp_file)
                
                # Limit speed to reasonable range
                speed = max(0.5, min(2.0, speed))
                
                # Use atempo filter (only supports 0.5-2.0)
                command = [
                    "ffmpeg", "-y",
                    "-i", temp_file,
                    "-filter:a", f"atempo={speed}",
                    final_file
                ]
                
                subprocess.run(command, capture_output=True, check=True)
                
                # Delete temp file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            duration = self._get_audio_duration(final_file)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"[OK] Audio file generated!\n"
                f"Path: {final_file}\n"
                f"Language: {language}\n"
                f"Speed: {speed}x\n"
                f"Duration: {duration_str}"
            )
            
        except Exception as e:
            # Cleanup temp file on error
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return f"[ERROR] Error generating audio file: {e}"