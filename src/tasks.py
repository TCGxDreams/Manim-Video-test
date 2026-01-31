# src/tasks.py - Enhanced version with timing support

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
                f"Research the topic '{topic}', then write a short video script.\n\n"
                "IMPORTANT REQUIREMENTS:\n"
                "1. [VOICEOVER SCRIPT] should be 130-150 words (for 1-minute video).\n"
                "2. [VISUAL SCRIPT] should have 3-4 SCENEs with timing.\n"
                "3. Add [TIMING] section at the end with estimated total duration.\n\n"
                "FORMAT:\n"
                "```\n"
                "[VISUAL SCRIPT]\n"
                "SCENE 1 (10s): Description of scene 1\n"
                "SCENE 2 (15s): Description of scene 2\n"
                "...\n\n"
                "[VOICEOVER SCRIPT]\n"
                "Voiceover content...\n\n"
                "[TIMING]\n"
                "- Total video duration: ~60s (1 minute)\n"
                "- Estimated audio duration: ~55s\n"
                "```\n\n"
                f"Finally, use the 'File Write Tool' to save the script to '{self.script_file}'."
            ),
            expected_output=(
                f"Confirmation string from 'File Write Tool' indicating '{self.script_file}' was written successfully."
            ),
            agent=agent
        )

    def manim_development_task(self, agent):
        return Task(
            description=(
                f"Read content from file '{self.script_file}'. Based on [VISUAL SCRIPT], write complete Manim code.\n\n"
                "IMPORTANT REQUIREMENTS:\n"
                "1. Strictly follow the MANIM PROGRAMMING HANDBOOK in your backstory.\n"
                "2. Use timing from script to set appropriate run_time for each animation.\n"
                "3. Add self.wait() between scenes for viewers to understand.\n"
                "4. Render with quality 'h' (1080p) when done.\n\n"
                f"Then, use 'File Write Tool' to save code to '{self.manim_code_file}'."
            ),
            expected_output=(
                f"Confirmation string from 'File Write Tool' indicating '{self.manim_code_file}' was written successfully."
            ),
            agent=agent
        )

    def qa_task(self, agent):
        return Task(
            description=(
                f"Read Python code content from file '{self.manim_code_file}'.\n"
                "Find the Manim class name in the code.\n\n"
                "Use 'Manim Code Execution Tool' with parameters:\n"
                "- manim_code: Python code content\n"
                "- class_name: Manim class name\n"
                "- quality: 'h' (1080p - default, high quality)\n"
                "- fps: 30 (default frame rate)\n\n"
                "IF FAILED: Create error report with specific details.\n"
                "IF SUCCESS: Note video duration and confirm success."
            ),
            expected_output=(
                "A confirmation string of successful Manim execution (including video path and duration) "
                "or a detailed error report if failed."
            ),
            agent=agent
        )

    def voiceover_task(self, agent):
        return Task(
            description=(
                f"Read content from file '{self.script_file}'.\n\n"
                "Use [VOICEOVER SCRIPT] section to create audio file using 'Text to Speech Tool'.\n\n"
                "NOTE:\n"
                "1. Tool will auto-detect language (English/Vietnamese).\n"
                "2. Note the audio duration returned.\n"
                "3. For complex content, use slow=True for slower speech.\n\n"
                f"Save audio to '{self.voiceover_file}'."
            ),
            expected_output=(
                f"Confirmation from 'Text to Speech Tool' indicating '{self.voiceover_file}' was saved successfully, "
                "including audio duration info."
            ),
            agent=agent
        )

    def production_task(self, agent):
        return Task(
            description=(
                f"Merge video file '{self.silent_video_file}' with audio file '{self.voiceover_file}'.\n\n"
                "Use 'FFmpeg Video-Audio Merger' with parameters:\n"
                f"- video_file: '{self.silent_video_file}'\n"
                f"- audio_file: '{self.voiceover_file}'\n"
                f"- output_file: '{self.final_video_file}'\n"
                "- speed_adjust: True (auto-adjust video speed to match audio)\n\n"
                "BEFORE MERGE: Can use 'Media Duration Tool' to check duration of both files."
            ),
            expected_output=(
                f"Confirmation message that final video was created at 'workspace/{self.final_video_file}', "
                "including duration and speed adjustment info if any."
            ),
            agent=agent
        )