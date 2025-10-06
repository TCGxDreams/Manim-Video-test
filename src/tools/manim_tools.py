import os
import subprocess
from langchain.tools import BaseTool 

# Đảm bảo thư mục workspace tồn tại
os.makedirs("workspace", exist_ok=True)

class FFmpegTool(BaseTool):
    name: str = "FFmpeg Video-Audio Merger"
    description: str = "Merges a video file and an audio file into a single output video file using FFmpeg."

    def _run(self, video_file: str, audio_file: str, output_file: str = "final_video.mp4") -> str:
        video_path = os.path.join("workspace", video_file)
        audio_path = os.path.join("workspace", audio_file)
        output_path = os.path.join("workspace", output_file)

        if not os.path.exists(video_path):
            return f"Error: Video file not found at {video_path}"
        if not os.path.exists(audio_path):
            return f"Error: Audio file not found at {audio_path}"

        command = [
            "ffmpeg",
            "-y",  # Ghi đè file output nếu đã tồn tại
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",  # Sao chép luồng video mà không mã hóa lại
            "-c:a", "aac",   # Mã hóa audio thành AAC
            "-shortest",     # Kết thúc video khi luồng ngắn nhất kết thúc
            output_path,
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return f"Video and audio merged successfully. Final video at: {output_path}"
        except subprocess.CalledProcessError as e:
            return f"FFmpeg execution failed: {e.stderr}"
        except FileNotFoundError:
            return "Error: 'ffmpeg' command not found. Please ensure FFmpeg is installed and accessible in your system's PATH."

class ManimExecutionTool(BaseTool):
    name: str = "Manim Code Execution Tool"
    description: str = "Executes Manim code. Takes Python code string and the Manim class name as input. Returns the path to the rendered video file or an error message."

    def _run(self, manim_code: str, class_name: str) -> str:
        # Chúng ta sẽ luôn làm việc với một tên file cố định để tránh nhầm lẫn
        file_name = "animation_scene"
        
        # Đường dẫn để script Python này ghi file vào (từ thư mục gốc của dự án)
        py_file_path_to_write = os.path.join("workspace", f"{file_name}.py")
        
        # Đường dẫn mà lệnh manim sẽ sử dụng (từ bên trong thư mục 'workspace')
        py_file_path_for_command = f"{file_name}.py"

        # Ghi mã Manim vào một file .py
        try:
            with open(py_file_path_to_write, "w", encoding="utf-8") as f:
                f.write(manim_code)
        except Exception as e:
            return f"Error writing Manim code to file: {e}"

        # === BẢN SỬA LỖI NẰM Ở ĐÂY ===
        # Xây dựng lệnh Manim sử dụng các flag hiện đại
        command = [
            "manim",
            "-ql", # Render chất lượng thấp
            py_file_path_for_command, # Đường dẫn tương đối với cwd
            class_name,
            "--media_dir", ".", # Yêu cầu Manim xuất MỌI THỨ ra thư mục hiện tại (tức là 'workspace')
            "-o", file_name, # Đặt tên file video output là 'animation_scene.mp4'
        ]

        try:
            # Chạy lệnh với thư mục làm việc hiện tại (cwd) là 'workspace'
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd="workspace", 
                check=True
            )
            
            video_file_path = os.path.join("workspace", f"{file_name}.mp4")
            return f"Manim scene rendered successfully. Video available at: {video_file_path}"
        except subprocess.CalledProcessError as e:
            error_message = f"Manim execution failed with error code {e.returncode}.\n"
            error_message += f"STDERR:\n{e.stderr}\n" # stderr thường chứa thông báo lỗi của Manim
            error_message += f"STDOUT:\n{e.stdout}"
            return error_message
        except FileNotFoundError:
            return "Error: 'manim' command not found. Please ensure Manim is installed and accessible in your system's PATH."