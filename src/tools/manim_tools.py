import os
import subprocess
import json
import re
from langchain.tools import BaseTool 

# Đảm bảo thư mục workspace tồn tại
os.makedirs("workspace", exist_ok=True)

class FFmpegTool(BaseTool):
    """Enhanced FFmpeg tool với tính năng điều chỉnh tốc độ và âm thanh."""
    
    name: str = "FFmpeg Video-Audio Merger"
    description: str = (
        "Merges a video file and an audio file into a single output video file using FFmpeg. "
        "Can adjust video speed to match audio duration. "
        "Arguments: video_file (str), audio_file (str), output_file (str, default='final_video.mp4'), "
        "speed_adjust (bool, default=True) - automatically adjust video speed to match audio duration."
    )

    def _get_duration(self, file_path: str) -> float:
        """Lấy thời lượng của file media bằng ffprobe."""
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
            return f"Error: Video file not found at {video_path}"
        if not os.path.exists(audio_path):
            return f"Error: Audio file not found at {audio_path}"

        # Lấy thời lượng của cả hai file
        video_duration = self._get_duration(video_path)
        audio_duration = self._get_duration(audio_path)

        if video_duration <= 0 or audio_duration <= 0:
            # Fallback nếu không lấy được duration
            speed_adjust = False

        # Tính toán hệ số tốc độ
        if speed_adjust and video_duration > 0 and audio_duration > 0:
            # speed_factor > 1: video chạy nhanh hơn, < 1: video chạy chậm hơn
            speed_factor = video_duration / audio_duration
            
            # Giới hạn speed factor trong khoảng hợp lý (0.5x - 2x)
            speed_factor = max(0.5, min(2.0, speed_factor))
            
            # Sử dụng setpts filter để điều chỉnh tốc độ video
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
                f"\n📊 Duration info: Video={video_duration:.2f}s, Audio={audio_duration:.2f}s, "
                f"Speed factor={speed_factor:.2f}x"
            )
        else:
            # Merge đơn giản không điều chỉnh tốc độ
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
            return f"✅ Video and audio merged successfully. Final video at: {output_path}{duration_info}"
        except subprocess.CalledProcessError as e:
            return f"❌ FFmpeg execution failed: {e.stderr}"
        except FileNotFoundError:
            return "❌ Error: 'ffmpeg' command not found. Please ensure FFmpeg is installed and accessible in your system's PATH."


class ManimExecutionTool(BaseTool):
    """Enhanced Manim execution tool với nhiều tùy chọn chất lượng."""
    
    name: str = "Manim Code Execution Tool"
    description: str = (
        "Executes Manim code with configurable quality settings. "
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

    # Template cho tiếng Việt với XeLaTeX
    VIETNAMESE_TEX_TEMPLATE = '''
\\documentclass[preview]{standalone}
\\usepackage{fontspec}
\\usepackage{unicode-math}
\\setmainfont{Arial}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\begin{document}
YourTextHere
\\end{document}
'''

    def _get_video_duration(self, video_path: str) -> float:
        """Lấy thời lượng video bằng ffprobe."""
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
        """Kiểm tra xem code có chứa ký tự tiếng Việt không."""
        vietnamese_pattern = r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]'
        return bool(re.search(vietnamese_pattern, code))

    def _inject_vietnamese_support(self, code: str) -> str:
        """Thêm hỗ trợ tiếng Việt nếu cần."""
        if not self._detect_vietnamese(code):
            return code
        
        # Thêm import TexTemplate nếu chưa có
        if "TexTemplate" not in code:
            # Tìm vị trí import cuối cùng
            import_section = """
# Vietnamese language support
from manim import TexTemplate

vietnamese_template = TexTemplate()
vietnamese_template.preamble = r'''
\\usepackage{fontspec}
\\setmainfont{Arial}
\\usepackage{amsmath}
\\usepackage{amssymb}
'''
"""
            # Chèn sau dòng import manim
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
            quality = "h"  # Default to 1080p
        
        quality_info = self.QUALITY_MAP[quality]
        
        # Validate FPS
        if fps not in [15, 30, 60]:
            fps = quality_info["default_fps"]
        
        file_name = "animation_scene"
        py_file_path_to_write = os.path.join("workspace", f"{file_name}.py")
        py_file_path_for_command = f"{file_name}.py"
        
        # Inject Vietnamese support nếu cần
        manim_code = self._inject_vietnamese_support(manim_code)

        # Ghi mã Manim vào file .py
        try:
            with open(py_file_path_to_write, "w", encoding="utf-8") as f:
                f.write(manim_code)
        except Exception as e:
            return f"❌ Error writing Manim code to file: {e}"

        # Xây dựng lệnh Manim
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
            
            # Manim outputs to: workspace/videos/animation_scene/{quality}/animation_scene.mp4
            # We need to copy to workspace/animation_scene.mp4 for production step
            quality_folder = f"{quality_info['resolution'].replace('p', '')}p{fps}"
            actual_video_path = os.path.join("workspace", "videos", file_name, quality_folder, f"{file_name}.mp4")
            expected_video_path = os.path.join("workspace", f"{file_name}.mp4")
            
            # Try to find and copy the video
            import shutil
            import glob
            
            # Search for the video file in various quality folders
            search_pattern = os.path.join("workspace", "videos", file_name, "*", f"{file_name}.mp4")
            found_videos = glob.glob(search_pattern)
            
            if found_videos:
                # Copy the most recent video to workspace root
                shutil.copy2(found_videos[0], expected_video_path)
                video_file_path = expected_video_path
            else:
                video_file_path = expected_video_path
            
            # Lấy thời lượng video
            duration = self._get_video_duration(video_file_path)
            duration_str = f"{duration:.2f}s" if duration > 0 else "unknown"
            
            return (
                f"✅ Manim scene rendered successfully!\n"
                f"📁 Video path: {video_file_path}\n"
                f"🎬 Resolution: {quality_info['resolution']} @ {fps}fps\n"
                f"⏱️ Duration: {duration_str}"
            )
            
        except subprocess.CalledProcessError as e:
            # Phân loại lỗi chi tiết
            stderr = e.stderr
            stdout = e.stdout
            
            error_type = "Unknown Error"
            suggestion = ""
            
            if "SyntaxError" in stderr or "SyntaxError" in stdout:
                error_type = "🔴 SYNTAX ERROR"
                suggestion = "Kiểm tra cú pháp Python: dấu ngoặc, dấu hai chấm, indent."
            elif "ImportError" in stderr or "ModuleNotFoundError" in stderr:
                error_type = "🟠 IMPORT ERROR"
                suggestion = "Module không tồn tại. Chỉ sử dụng các class từ 'from manim import *'."
            elif "AttributeError" in stderr:
                error_type = "🟡 ATTRIBUTE ERROR"
                suggestion = "Method hoặc property không tồn tại. Kiểm tra tên method đúng chính tả."
            elif "TypeError" in stderr:
                error_type = "🟣 TYPE ERROR"
                suggestion = "Sai kiểu dữ liệu. Kiểm tra các tham số truyền vào."
            elif "ValueError" in stderr:
                error_type = "🔵 VALUE ERROR"
                suggestion = "Giá trị không hợp lệ."
            elif "RuntimeError" in stderr or "Exception" in stderr:
                error_type = "⚫ RUNTIME ERROR"
                suggestion = "Lỗi khi thực thi. Kiểm tra logic trong construct()."
            
            error_message = (
                f"❌ {error_type} - Manim execution failed (code {e.returncode})\n\n"
                f"💡 Gợi ý: {suggestion}\n\n"
                f"--- STDERR ---\n{stderr}\n\n"
                f"--- STDOUT ---\n{stdout}"
            )
            return error_message
            
        except FileNotFoundError:
            return "❌ Error: 'manim' command not found. Please ensure Manim is installed and accessible in your system's PATH."


class VideoDurationTool(BaseTool):
    """Tool để lấy thông tin thời lượng của video hoặc audio."""
    
    name: str = "Media Duration Tool"
    description: str = (
        "Gets the duration of a video or audio file in seconds. "
        "Argument: file_name (str) - name of the file in workspace directory."
    )

    def _run(self, file_name: str) -> str:
        file_path = os.path.join("workspace", file_name)
        
        if not os.path.exists(file_path):
            return f"❌ Error: File not found at {file_path}"
        
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
            return f"✅ Duration of {file_name}: {duration:.2f} seconds"
        except subprocess.CalledProcessError as e:
            return f"❌ Error getting duration: {e.stderr}"
        except Exception as e:
            return f"❌ Error: {e}"