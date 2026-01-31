# src/tasks.py - Bilingual version (English/Vietnamese)

from crewai import Task

class VideoTasks:
    def __init__(self):
        self.script_file = "video_script.txt"
        self.manim_code_file = "manim_animation.py"
        self.voiceover_file = "voiceover.mp3"
        self.silent_video_file = "animation_scene.mp4"
        self.final_video_file = "final_video.mp4"

    def storytelling_task(self, agent, topic):
        return Task(
            description=(
                f"Research the topic '{topic}', then write a short video script.\n"
                f"Nghien cuu chu de '{topic}', sau do viet mot kich ban video ngan gon.\n\n"
                "IMPORTANT REQUIREMENTS / YEU CAU QUAN TRONG:\n"
                "1. [VOICEOVER SCRIPT] should be 130-150 words (for 1-minute video).\n"
                "   Phan [VOICEOVER SCRIPT] phai co do dai 130-150 tu (cho video 1 phut).\n"
                "2. [VISUAL SCRIPT] should have 3-4 SCENEs with timing.\n"
                "   Phan [VISUAL SCRIPT] nen chia thanh 3-4 SCENE voi timing.\n"
                "3. Add [TIMING] section at the end with estimated total duration.\n"
                "   Them phan [TIMING] o cuoi voi tong thoi luong uoc tinh.\n\n"
                "FORMAT:\n"
                "```\n"
                "[VISUAL SCRIPT]\n"
                "SCENE 1 (10s): Description / Mo ta scene 1\n"
                "SCENE 2 (15s): Description / Mo ta scene 2\n"
                "...\n\n"
                "[VOICEOVER SCRIPT]\n"
                "Voiceover content / Noi dung loi thoai...\n\n"
                "[TIMING]\n"
                "- Total video duration / Tong thoi luong video: ~60s (1 minute / phut)\n"
                "- Estimated audio duration / Thoi luong audio uoc tinh: ~55s\n"
                "```\n\n"
                f"Finally, use the 'File Write Tool' to save the script to '{self.script_file}'.\n"
                f"Cuoi cung, su dung 'File Write Tool' de luu kich ban vao tep '{self.script_file}'."
            ),
            expected_output=(
                f"Confirmation string from 'File Write Tool' indicating '{self.script_file}' was written successfully.\n"
                f"Chuoi xac nhan tu 'File Write Tool' cho biet tep '{self.script_file}' da duoc ghi thanh cong."
            ),
            agent=agent
        )

    def manim_development_task(self, agent):
        return Task(
            description=(
                f"Read content from file '{self.script_file}'. Based on [VISUAL SCRIPT], write complete Manim code.\n"
                f"Doc noi dung tu tep '{self.script_file}'. Dua vao phan [VISUAL SCRIPT], viet ma Manim hoan chinh.\n\n"
                "IMPORTANT REQUIREMENTS / YEU CAU QUAN TRONG:\n"
                "1. Strictly follow the MANIM PROGRAMMING HANDBOOK in your backstory.\n"
                "   Tuan thu nghiem ngat SO TAY LAP TRINH MANIM trong backstory cua ban.\n"
                "2. Use timing from script to set appropriate run_time for each animation.\n"
                "   Su dung timing tu script de dat run_time phu hop cho moi animation.\n"
                "3. Add self.wait() between scenes for viewers to understand.\n"
                "   Them self.wait() giua cac scene de nguoi xem co thoi gian hieu.\n"
                "4. Render with quality 'h' (1080p) when done.\n"
                "   Render voi chat luong 'h' (1080p) khi hoan tat.\n\n"
                f"Then, use 'File Write Tool' to save code to '{self.manim_code_file}'.\n"
                f"Sau do, su dung 'File Write Tool' de luu ma vao tep '{self.manim_code_file}'."
            ),
            expected_output=(
                f"Confirmation string from 'File Write Tool' indicating '{self.manim_code_file}' was written successfully.\n"
                f"Chuoi xac nhan tu 'File Write Tool' cho biet tep '{self.manim_code_file}' da duoc ghi thanh cong."
            ),
            agent=agent
        )

    def qa_task(self, agent):
        return Task(
            description=(
                f"Read Python code content from file '{self.manim_code_file}'.\n"
                f"Doc noi dung ma Python tu tep '{self.manim_code_file}'.\n"
                "Find the Manim class name in the code.\n"
                "Tim ten lop Manim trong ma.\n\n"
                "Use 'Manim Code Execution Tool' with parameters:\n"
                "Su dung 'Manim Code Execution Tool' voi cac tham so:\n"
                "- manim_code: Python code content / noi dung ma Python\n"
                "- class_name: Manim class name / ten lop Manim\n"
                "- quality: 'h' (1080p - default, high quality)\n"
                "- fps: 30 (default frame rate)\n\n"
                "IF FAILED / NEU THAT BAI: Create error report with specific details.\n"
                "IF SUCCESS / NEU THANH CONG: Note video duration and confirm success."
            ),
            expected_output=(
                "A confirmation string of successful Manim execution (including video path and duration) "
                "or a detailed error report if failed.\n"
                "Chuoi xac nhan thuc thi Manim thanh cong (bao gom duong dan video va thoi luong) "
                "hoac bao cao loi chi tiet neu that bai."
            ),
            agent=agent
        )

    def voiceover_task(self, agent):
        return Task(
            description=(
                f"Read content from file '{self.script_file}'.\n"
                f"Doc noi dung tu tep '{self.script_file}'.\n\n"
                "Use [VOICEOVER SCRIPT] section to create audio file using 'Text to Speech Tool'.\n"
                "Su dung phan [VOICEOVER SCRIPT] de tao tep am thanh bang 'Text to Speech Tool'.\n\n"
                "NOTE / LUU Y:\n"
                "1. Tool will auto-detect language (English/Vietnamese).\n"
                "   Cong cu se tu dong phat hien ngon ngu (Tieng Anh/Tieng Viet).\n"
                "2. Note the audio duration returned.\n"
                "   Ghi nhan thoi luong audio duoc tra ve.\n"
                "3. For complex content, use slow=True for slower speech.\n"
                "   Voi noi dung phuc tap, dung slow=True de doc cham hon.\n\n"
                f"Save audio to '{self.voiceover_file}'.\n"
                f"Luu audio vao '{self.voiceover_file}'."
            ),
            expected_output=(
                f"Confirmation from 'Text to Speech Tool' indicating '{self.voiceover_file}' was saved successfully, "
                "including audio duration info.\n"
                f"Xac nhan tu 'Text to Speech Tool' cho biet '{self.voiceover_file}' da duoc luu thanh cong, "
                "bao gom thong tin ve thoi luong audio."
            ),
            agent=agent
        )

    def production_task(self, agent):
        return Task(
            description=(
                f"Merge video file '{self.silent_video_file}' with audio file '{self.voiceover_file}'.\n"
                f"Ghep tep video '{self.silent_video_file}' voi tep am thanh '{self.voiceover_file}'.\n\n"
                "Use 'FFmpeg Video-Audio Merger' with parameters:\n"
                "Su dung 'FFmpeg Video-Audio Merger' voi cac tham so:\n"
                f"- video_file: '{self.silent_video_file}'\n"
                f"- audio_file: '{self.voiceover_file}'\n"
                f"- output_file: '{self.final_video_file}'\n"
                "- speed_adjust: True (auto-adjust video speed to match audio)\n"
                "  (tu dong dieu chinh toc do video de khop audio)\n\n"
                "BEFORE MERGE / TRUOC KHI MERGE: Can use 'Media Duration Tool' to check duration of both files.\n"
                "Co the dung 'Media Duration Tool' de kiem tra thoi luong cua ca hai file."
            ),
            expected_output=(
                f"Confirmation message that final video was created at 'workspace/{self.final_video_file}', "
                "including duration and speed adjustment info if any.\n"
                f"Thong bao xac nhan video cuoi cung da duoc tao tai 'workspace/{self.final_video_file}', "
                "bao gom thong tin ve duration va speed adjustment neu co."
            ),
            agent=agent
        )