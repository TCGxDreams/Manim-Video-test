# api/server.py - Flask Backend API for Manim AI Studio

import os
import sys
import uuid
import threading
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# Store generation jobs
jobs = {}

# Workspace directory
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)


def run_video_generation(job_id, topic, language, duration):
    """Run video generation in background thread."""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["phase"] = "Initializing / Khoi tao..."
        
        # Import here to avoid circular imports
        from dotenv import load_dotenv
        load_dotenv()
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
        
        from src.agents import VideoAgents
        from src.tasks import VideoTasks
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        jobs[job_id]["phase"] = "Loading LLM models / Dang tai mo hinh LLM..."
        
        llm_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1)
        llm_pro = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.4)
        
        agents = VideoAgents()
        tasks = VideoTasks()
        
        storyteller = agents.storyteller_agent(llm_flash)
        manim_dev = agents.manim_developer_agent(llm_pro)
        qa_engineer = agents.qa_engineer_agent(llm_flash)
        voice_artist = agents.voiceover_artist_agent(llm_flash)
        producer = agents.production_engineer_agent(llm_flash)
        
        # Phase 1: Script
        jobs[job_id]["phase"] = "Phase 1: Creating script / Dang tao kich ban..."
        jobs[job_id]["progress"] = 10
        
        story_task = tasks.storytelling_task(storyteller, topic)
        story_task.execute(agent=storyteller)
        
        # Phase 2: Development
        jobs[job_id]["phase"] = "Phase 2: Writing Manim code / Dang viet code Manim..."
        jobs[job_id]["progress"] = 30
        
        code_task = tasks.manim_development_task(manim_dev)
        max_retries = 5
        is_approved = False
        
        for i in range(max_retries):
            jobs[job_id]["phase"] = f"Phase 2: Attempt {i+1}/{max_retries} / Lan thu {i+1}/{max_retries}"
            
            code_task.execute(agent=manim_dev)
            
            jobs[job_id]["phase"] = "Phase 2: QA checking / Dang kiem tra..."
            qa_task = tasks.qa_task(qa_engineer)
            qa_result = qa_task.execute(agent=qa_engineer)
            
            if "SUCCESS" in qa_result.upper() or "THANH CONG" in qa_result.upper():
                is_approved = True
                break
        
        if not is_approved:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = "Code could not be fixed after retries / Khong the sua code sau nhieu lan thu"
            return
        
        jobs[job_id]["progress"] = 60
        
        # Phase 3: Production
        jobs[job_id]["phase"] = "Phase 3: Creating voiceover / Dang tao loi thoai..."
        jobs[job_id]["progress"] = 70
        
        voice_task = tasks.voiceover_task(voice_artist)
        voice_task.execute(agent=voice_artist)
        
        jobs[job_id]["phase"] = "Phase 3: Merging video & audio / Dang ghep video & audio..."
        jobs[job_id]["progress"] = 85
        
        production_task = tasks.production_task(producer)
        production_task.execute(agent=producer)
        
        # Complete
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["phase"] = "Completed! / Hoan thanh!"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["video_path"] = "final_video.mp4"
        
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


@app.route("/api/generate", methods=["POST"])
def generate_video():
    """Start video generation."""
    data = request.json
    topic = data.get("topic", "Basic Derivatives")
    language = data.get("language", "en")
    duration = data.get("duration", 1)  # minutes
    
    job_id = str(uuid.uuid4())[:8]
    
    jobs[job_id] = {
        "id": job_id,
        "topic": topic,
        "language": language,
        "duration": duration,
        "status": "queued",
        "phase": "Queued / Dang cho...",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "video_path": None,
        "error": None
    }
    
    # Start generation in background thread
    thread = threading.Thread(
        target=run_video_generation,
        args=(job_id, topic, language, duration)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({"job_id": job_id, "message": "Generation started / Da bat dau tao video"})


@app.route("/api/status/<job_id>", methods=["GET"])
def get_status(job_id):
    """Get job status."""
    if job_id not in jobs:
        return jsonify({"error": "Job not found / Khong tim thay job"}), 404
    
    return jsonify(jobs[job_id])


@app.route("/api/videos", methods=["GET"])
def list_videos():
    """List generated videos."""
    videos = []
    
    for filename in os.listdir(WORKSPACE_DIR):
        if filename.endswith(".mp4"):
            filepath = os.path.join(WORKSPACE_DIR, filename)
            videos.append({
                "name": filename,
                "size": os.path.getsize(filepath),
                "created_at": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
            })
    
    return jsonify(videos)


@app.route("/api/videos/<filename>", methods=["GET"])
def get_video(filename):
    """Serve video file."""
    return send_from_directory(WORKSPACE_DIR, filename)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Server is running / Server dang chay"})


if __name__ == "__main__":
    print("[INFO] Starting Manim AI Studio API Server...")
    print("[INFO] Dang khoi dong Manim AI Studio API Server...")
    print("[INFO] API running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
