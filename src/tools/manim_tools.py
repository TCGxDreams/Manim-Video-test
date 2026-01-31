import os
import subprocess
import json
import re
from langchain.tools import BaseTool 

# Ensure workspace directory exists / Dam bao thu muc workspace ton tai
os.makedirs("workspace", exist_ok=True)

class FFmpegTool(BaseTool):
    """Enhanced FFmpeg tool with speed adjustment. / Cong cu FFmpeg voi dieu chinh toc do."""
    
    name: str = "FFmpeg Video-Audio Merger"
    description: str = (
        "Merges a video file and an audio file into a single output video file using FFmpeg. "
        "Ghep video va audio thanh mot file output. "
        "Can adjust video speed to match audio duration. "
        "Arguments: video_file (str), audio_file (str), output_file (str, default='final_video.mp4'), "
        "speed_adjust (bool, default=True) - automatically adjust video speed to match audio duration."
    )

    def _get_duration(self, file_path: str) -> float:
        """Get media file duration using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "json", file_path
                ],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except Exception:
            return 0.0

    def _run(
        self, 
        video_file: str, 
        audio_file: str, 
        output_file: str = "final_video.mp4",
        speed_adjust: bool = True,
        normalize_audio: bool = True
    ) -> str:
        video_path = os.path.join("workspace", video_file)
        audio_path = os.path.join("workspace", audio_file)
        output_path = os.path.join("workspace", output_file)

        if not os.path.exists(video_path):
            return f"Error: Video file not found at {video_path} / Khong tim thay file video"
        if not os.path.exists(audio_path):
            return f"Error: Audio file not found at {audio_path} / Khong tim thay file audio"

        # Get duration of both files
        video_duration = self._get_duration(video_path)
        audio_duration = self._get_duration(audio_path)

        if video_duration <= 0 or audio_duration <= 0:
            speed_adjust = False

        # Calculate speed factor
        if speed_adjust and video_duration > 0 and audio_duration > 0:
            speed_factor = video_duration / audio_duration
            speed_factor = max(0.5, min(2.0, speed_factor))
            video_filter = f"setpts={1/speed_factor}*PTS"
            
            command = [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-i", audio_path,
                "-filter_complex", f"[0:v]{video_filter}[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_path,
            ]
            
            duration_info = (
                f"\nInfo: Video={video_duration:.2f}s, Audio={audio_duration:.2f}s, "
                f"Speed factor={speed_factor:.2f}x"
            )
        else:
            command = [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_path,
            ]
            duration_info = ""

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return f"[OK] Video and audio merged successfully! / Ghep video va audio thanh cong!\nFinal video at: {output_path}{duration_info}"
        except subprocess.CalledProcessError as e:
            return f"[ERROR] FFmpeg execution failed / FFmpeg that bai: {e.stderr}"
        except FileNotFoundError:
            return "[ERROR] 'ffmpeg' command not found. Please install FFmpeg. / Khong tim thay lenh 'ffmpeg'. Vui long cai dat FFmpeg."


class ManimExecutionTool(BaseTool):
    """Enhanced Manim execution tool. Supports Vietnamese text."""
    
    name: str = "Manim Code Execution Tool"
    description: str = (
        "Executes Manim code with configurable quality settings. "
        "Supports Vietnamese text in animations. "
        "Arguments: manim_code (str) - Python code, class_name (str) - Manim class name, "
        "quality (str, default='h') - 'l'=480p, 'm'=720p, 'h'=1080p, 'p'=1440p, 'k'=4K, "
        "fps (int, default=30) - frame rate (15, 30, or 60). "
        "Returns the path to the rendered video file, duration, and resolution info."
    )

    QUALITY_MAP = {
        "l": {"flag": "-ql", "resolution": "480p", "default_fps": 15},
        "m": {"flag": "-qm", "resolution": "720p", "default_fps": 30},
        "h": {"flag": "-qh", "resolution": "1080p", "default_fps": 60},
        "p": {"flag": "-qp", "resolution": "1440p", "default_fps": 60},
        "k": {"flag": "-qk", "resolution": "4K", "default_fps": 60},
    }

    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "json", video_path
                ],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except Exception:
            return 0.0

    def _detect_vietnamese(self, code: str) -> bool:
        """Check if code contains Vietnamese characters."""
        vietnamese_chars = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
        for char in code:
            if char in vietnamese_chars:
                return True
        return False

    def _inject_vietnamese_support(self, code: str) -> str:
        """Add Vietnamese support if needed. / Them ho tro tieng Viet neu can."""
        if not self._detect_vietnamese(code):
            return code
        
        # Add TexTemplate import if not exists
        if "TexTemplate" not in code:
            import_section = """
# Vietnamese language support / Ho tro tieng Viet
from manim import TexTemplate

vietnamese_template = TexTemplate()
vietnamese_template.preamble = r'''
\\usepackage{fontspec}
\\setmainfont{Arial}
\\usepackage{amsmath}
\\usepackage{amssymb}
'''
"""
            if "from manim import" in code:
                code = code.replace("from manim import *", "from manim import *" + import_section)
            elif "import manim" in code:
                code = code.replace("import manim", "import manim" + import_section)
        
        return code

    def _run(
        self, 
        manim_code: str, 
        class_name: str, 
        quality: str = "h",
        fps: int = 30
    ) -> str:
        # Validate quality
        quality = quality.lower()
        if quality not in self.QUALITY_MAP:
            quality = "h"
        
        quality_info = self.QUALITY_MAP[quality]
        
        # Validate FPS
        if fps not in [15, 30, 60]:
            fps = quality_info["default_fps"]
        
        file_name = "animation_scene"
        py_file_path_to_write = os.path.join("workspace", f"{file_name}.py")
        py_file_path_for_command = f"{file_name}.py"
        
        # Inject Vietnamese support if needed
        manim_code = self._inject_vietnamese_support(manim_code)

        # Write Manim code to .py file
        try:
            with open(py_file_path_to_write, "w", encoding="utf-8") as f:
                f.write(manim_code)
        except Exception as e:
            return f"[ERROR] Error writing Manim code to file / Loi ghi ma Manim vao file: {e}"

        # Build Manim command
        command = [
            "manim",
            quality_info["flag"],
            "--fps", str(fps),
            py_file_path_for_command,
            class_name,
            "--media_dir", ".",
            "-o", file_name,
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd="workspace", 
                check=True
            )
            
            # Find and copy video to workspace root
            import shutil
            import glob
            
            search_pattern = os.path.join("workspace", "videos", file_name, "*", f"{file_name}.mp4")
            found_videos = glob.glob(search_pattern)
            expected_video_path = os.path.join("workspace", f"{file_name}.mp4")
            
            if found_videos:
                shutil.copy2(found_videos[0], expected_video_path)
                video_file_path = expected_video_path
            else:
                video_file_path = expected_video_path
            
            # Get video duration
            duration = self._get_video_duration(video_file_path)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"[OK] Manim scene rendered successfully! / Manim scene render thanh cong!\n"
                f"Video path: {video_file_path}\n"
                f"Resolution / Do phan giai: {quality_info['resolution']} @ {fps}fps\n"
                f"Duration / Thoi luong: {duration_str}"
            )
            
        except subprocess.CalledProcessError as e:
            stderr = e.stderr
            stdout = e.stdout
            
            error_type = "Unknown Error / Loi khong xac dinh"
            suggestion = ""
            
            if "SyntaxError" in stderr or "SyntaxError" in stdout:
                error_type = "SYNTAX ERROR / LOI CU PHAP"
                suggestion = "Check Python syntax: parentheses, colons, indentation. / Kiem tra cu phap Python: dau ngoac, dau hai cham, indent."
            elif "ImportError" in stderr or "ModuleNotFoundError" in stderr:
                error_type = "IMPORT ERROR / LOI IMPORT"
                suggestion = "Module does not exist. Only use classes from 'from manim import *'. / Module khong ton tai."
            elif "AttributeError" in stderr:
                error_type = "ATTRIBUTE ERROR / LOI ATTRIBUTE"
                suggestion = "Method or property does not exist. Check method name spelling. / Method hoac property khong ton tai."
            elif "TypeError" in stderr:
                error_type = "TYPE ERROR / LOI KIEU DU LIEU"
                suggestion = "Wrong data type. Check parameters passed. / Sai kieu du lieu."
            elif "ValueError" in stderr:
                error_type = "VALUE ERROR / LOI GIA TRI"
                suggestion = "Invalid value. / Gia tri khong hop le."
            elif "RuntimeError" in stderr or "Exception" in stderr:
                error_type = "RUNTIME ERROR / LOI RUNTIME"
                suggestion = "Error during execution. Check logic in construct(). / Loi khi thuc thi."
            
            error_message = (
                f"[ERROR] {error_type} - Manim execution failed (code {e.returncode})\n\n"
                f"Suggestion / Goi y: {suggestion}\n\n"
                f"--- STDERR ---\n{stderr}\n\n"
                f"--- STDOUT ---\n{stdout}"
            )
            return error_message
            
        except FileNotFoundError:
            return "[ERROR] 'manim' command not found. Please install Manim. / Khong tim thay lenh 'manim'. Vui long cai dat Manim."


class VideoDurationTool(BaseTool):
    """Tool to get video or audio duration information."""
    
    name: str = "Media Duration Tool"
    description: str = (
        "Gets the duration of a video or audio file in seconds. "
        "Lay thoi luong cua file video hoac audio tinh bang giay. "
        "Argument: file_name (str) - name of the file in workspace directory."
    )

    def _run(self, file_name: str) -> str:
        file_path = os.path.join("workspace", file_name)
        
        if not os.path.exists(file_path):
            return f"[ERROR] File not found at {file_path} / Khong tim thay file"
        
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "json", file_path
                ],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            duration = float(data["format"]["duration"])
            return f"[OK] Duration of {file_name} / Thoi luong cua {file_name}: {duration:.2f} seconds / giay"
        except subprocess.CalledProcessError as e:
            return f"[ERROR] Error getting duration / Loi lay thoi luong: {e.stderr}"
        except Exception as e:
            return f"[ERROR] Error / Loi: {e}"