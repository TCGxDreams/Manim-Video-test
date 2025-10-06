# src/tools/file_tools.py

import os
from langchain.tools import BaseTool # Đảm bảo import từ langchain.tools

# --- Công cụ Ghi tệp (giữ nguyên) ---
class FileWriteTool(BaseTool):
    name: str = "File Write Tool"
    description: str = "Writes content to a specified file in the 'workspace' directory. Creates the directory if it doesn't exist."

    def _run(self, file_path: str, content: str) -> str:
        workspace_dir = "workspace"
        full_path = os.path.join(workspace_dir, file_path)
        
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Content successfully written to {full_path}"
        except Exception as e:
            return f"Error writing to file: {e}"

# --- THÊM CÔNG CỤ ĐỌC TỆP MỚI VÀO ĐÂY ---
class CustomFileReadTool(BaseTool):
    name: str = "File Read Tool"
    description: str = "Reads the content of a specified file from the 'workspace' directory."
    
    def _run(self, file_path: str) -> str:
        workspace_dir = "workspace"
        full_path = os.path.join(workspace_dir, file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found at path {full_path}"
        except Exception as e:
            return f"Error reading file: {e}"