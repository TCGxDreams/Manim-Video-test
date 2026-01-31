import os
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# STEP 1: ENVIRONMENT CONFIGURATION AND AUTHENTICATION
# Must be done BEFORE importing project libraries
# --------------------------------------------------------------------------
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
load_dotenv()

from src.agents import VideoAgents
from src.tasks import VideoTasks
from langchain_google_genai import ChatGoogleGenerativeAI


# --------------------------------------------------------------------------
# STEP 2: INITIALIZE LLM MODELS AND AGENTS
# --------------------------------------------------------------------------

serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    print("[ERROR] Please set SERPER_API_KEY in .env file")
    exit()

print("[INFO] Initializing LLM Flash for creative tasks...")
llm_flash = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1
)

print("[INFO] Initializing LLM Pro for coding tasks...")
llm_pro = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.4
)

agents = VideoAgents()
tasks = VideoTasks()

print("[INFO] Assigning LLMs to specialized Agents...")
storyteller = agents.storyteller_agent(llm_flash)
manim_dev = agents.manim_developer_agent(llm_pro) 
qa_engineer = agents.qa_engineer_agent(llm_flash)
voice_artist = agents.voiceover_artist_agent(llm_flash)
producer = agents.production_engineer_agent(llm_flash)


# --------------------------------------------------------------------------
# STEP 3: MAIN WORKFLOW
# --------------------------------------------------------------------------

def main():
    """Main function controlling the entire video production process."""
    video_topic = "Basic Derivatives - derivative of x^n, sin(x), e^x"
    max_retries = 5

    print(f"\n[START] Beginning video production for topic: '{video_topic}'")

    # --- PHASE 1: SCRIPT CREATION ---
    print("\n[PHASE 1] CREATING SCRIPT...")
    story_task = tasks.storytelling_task(storyteller, video_topic)
    script_result = story_task.execute(agent=storyteller)
    print(f"[OK] Script created: {script_result}")

    # --- PHASE 2: DEVELOPMENT & ERROR FIX LOOP ---
    print("\n[PHASE 2] STARTING DEVELOPMENT & ERROR FIX LOOP...")
    
    code_task = tasks.manim_development_task(manim_dev)
    current_error_report = ""
    is_code_approved = False

    for i in range(max_retries):
        print(f"\n--- Attempt #{i + 1}/{max_retries} ---")
        
        if current_error_report:
            code_task.description = (
                "Your previous code had execution errors. "
                "Read the error report below, analyze the cause and rewrite the code correctly. "
                "Make sure to follow the 'Manim Programming Handbook' strictly.\n"
                f"--- ERROR REPORT FROM QA ---\n{current_error_report}\n--- END OF ERROR REPORT ---\n\n"
                "Original task: "
                f"Read [VISUAL SCRIPT] from file '{tasks.script_file}' and write complete Manim code. "
                f"Save code to file '{tasks.manim_code_file}'."
            )
        
        print("[DEV] Developer is writing/fixing code...")
        code_result = code_task.execute(agent=manim_dev)
        print(f"[OK] Code written/fixed: {code_result}")

        print("[QA] Checking code...")
        qa_task = tasks.qa_task(qa_engineer)
        qa_result = qa_task.execute(agent=qa_engineer)

        print(f"[REPORT] QA Result:\n{qa_result}")

        if "SUCCESS" in qa_result.upper() or "THANH CONG" in qa_result.upper():
            print("\n[SUCCESS] QA approved code! Moving to production phase.")
            is_code_approved = True
            break
        else:
            print("[BUG] QA found errors. Preparing for next fix attempt.")
            current_error_report = qa_result
    
    if not is_code_approved:
        print(f"\n[ERROR] CRITICAL: Developer could not fix errors after {max_retries} attempts. Stopping.")
        return

    # --- PHASE 3: PRODUCTION ---
    print("\n[PHASE 3] PRODUCTION...")
    
    print("[TTS] Creating voiceover...")
    voice_task = tasks.voiceover_task(voice_artist)
    voice_result = voice_task.execute(agent=voice_artist)
    print(f"[OK] Voiceover created: {voice_result}")

    print("[RENDER] Building final video...")
    production_task = tasks.production_task(producer)
    final_result = production_task.execute(agent=producer)
    print(f"[OK] Final video created: {final_result}")
    
    print("\n=== VIDEO PRODUCTION COMPLETE! ===")


# --------------------------------------------------------------------------
# STEP 5: PROGRAM ENTRY POINT
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()