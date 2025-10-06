import os
from gtts import gTTS
from langchain.tools import BaseTool 

class TextToSpeechTool(BaseTool):
    name: str = "Text to Speech Tool"
    description: str = "Converts a given text into an MP3 audio file using Google Text-to-Speech."

    def _run(self, text: str, file_name: str = "voiceover.mp3") -> str:
        workspace_dir = "workspace"
        file_path = os.path.join(workspace_dir, file_name)
        
        try:
            os.makedirs(workspace_dir, exist_ok=True)
            tts = gTTS(text=text, lang='en', slow=False) # 'vi' for Vietnamese
            tts.save(file_path)
            return f"Audio file saved successfully at {file_path}"
        except Exception as e:
            return f"Error generating audio file: {e}"