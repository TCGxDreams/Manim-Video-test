import os
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# STEP 1: ENVIRONMENT CONFIGURATION AND AUTHENTICATION
# BUOC 1: CAU HINH MOI TRUONG VA XAC THUC
# --------------------------------------------------------------------------
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
load_dotenv()

from src.agents import VideoAgents
from src.tasks import VideoTasks
from langchain_google_genai import ChatGoogleGenerativeAI


# --------------------------------------------------------------------------
# STEP 2: INITIALIZE LLM MODELS AND AGENTS
# BUOC 2: KHOI TAO LLM VA AGENTS
# --------------------------------------------------------------------------

serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    print("[ERROR] Please set SERPER_API_KEY in .env file")
    print("[LOI] Vui long thiet lap SERPER_API_KEY trong file .env")
    exit()

print("[INFO] Initializing LLM Flash for creative tasks...")
print("[INFO] Khoi tao LLM Flash cho cac tac vu sang tao...")
llm_flash = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1
)

print("[INFO] Initializing LLM Pro for coding tasks...")
print("[INFO] Khoi tao LLM Pro cho tac vu viet code...")
llm_pro = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0.4
)

agents = VideoAgents()
tasks = VideoTasks()

print("[INFO] Assigning LLMs to specialized Agents...")
print("[INFO] Phan cong LLM cho cac Agent chuyen biet...")
storyteller = agents.storyteller_agent(llm_flash)
manim_dev = agents.manim_developer_agent(llm_pro) 
qa_engineer = agents.qa_engineer_agent(llm_flash)
voice_artist = agents.voiceover_artist_agent(llm_flash)
producer = agents.production_engineer_agent(llm_flash)


# --------------------------------------------------------------------------
# STEP 3: MAIN WORKFLOW / QUY TRINH CHINH
# --------------------------------------------------------------------------

def main():
    """
    Main function controlling the entire video production process.
    Ham chinh dieu khien toan bo quy trinh san xuat video.
    """
    # Change topic here / Thay doi chu de o day
    video_topic = "Basic Derivatives - derivative of x^n, sin(x), e^x - 1 minute video"
    # Vietnamese example / Vi du tieng Viet:
    # video_topic = "Dao ham co ban - derivative of x^n, sin(x), e^x - video 1 phut tieng Viet"
    
    max_retries = 5

    print(f"\n[START] Beginning video production for topic: '{video_topic}'")
    print(f"[BAT DAU] Bat dau quy trinh san xuat video cho chu de: '{video_topic}'")

    # --- PHASE 1: SCRIPT CREATION / GIAI DOAN 1: TAO KICH BAN ---
    print("\n[PHASE 1] CREATING SCRIPT...")
    print("[GIAI DOAN 1] TAO KICH BAN...")
    story_task = tasks.storytelling_task(storyteller, video_topic)
    script_result = story_task.execute(agent=storyteller)
    print(f"[OK] Script created / Kich ban da duoc tao: {script_result}")

    # --- PHASE 2: DEVELOPMENT & ERROR FIX LOOP / GIAI DOAN 2: PHAT TRIEN & SUA LOI ---
    print("\n[PHASE 2] STARTING DEVELOPMENT & ERROR FIX LOOP...")
    print("[GIAI DOAN 2] BAT DAU VONG LAP PHAT TRIEN & SUA LOI...")
    
    code_task = tasks.manim_development_task(manim_dev)
    current_error_report = ""
    is_code_approved = False

    for i in range(max_retries):
        print(f"\n--- Attempt #{i + 1}/{max_retries} / Lan thu #{i + 1}/{max_retries} ---")
        
        if current_error_report:
            code_task.description = (
                "Your previous code had execution errors. "
                "Read the error report below, analyze the cause and rewrite the code correctly. "
                "Make sure to follow the 'Manim Programming Handbook' strictly.\n"
                "---\n"
                "Ma truoc do cua ban da gap loi. "
                "Doc bao cao loi ben duoi, phan tich nguyen nhan va viet lai ma cho chinh xac.\n"
                f"--- ERROR REPORT / BAO CAO LOI ---\n{current_error_report}\n--- END / KET THUC ---\n\n"
                f"Read [VISUAL SCRIPT] from file '{tasks.script_file}' and write complete Manim code. "
                f"Save code to file '{tasks.manim_code_file}'."
            )
        
        print("[DEV] Developer is writing/fixing code...")
        print("[DEV] Lap trinh vien dang viet/sua ma...")
        code_result = code_task.execute(agent=manim_dev)
        print(f"[OK] Code written/fixed / Ma da duoc viet/sua: {code_result}")

        print("[QA] Checking code / Dang kiem tra ma...")
        qa_task = tasks.qa_task(qa_engineer)
        qa_result = qa_task.execute(agent=qa_engineer)

        print(f"[REPORT] QA Result / Ket qua QA:\n{qa_result}")

        if "SUCCESS" in qa_result.upper() or "THANH CONG" in qa_result.upper():
            print("\n[SUCCESS] QA approved code! Moving to production phase.")
            print("[THANH CONG] QA da phe duyet ma! Chuyen sang giai doan san xuat.")
            is_code_approved = True
            break
        else:
            print("[BUG] QA found errors. Preparing for next fix attempt.")
            print("[LOI] QA tim thay loi. Chuan bi cho lan sua tiep theo.")
            current_error_report = qa_result
    
    if not is_code_approved:
        print(f"\n[ERROR] CRITICAL: Developer could not fix errors after {max_retries} attempts. Stopping.")
        print(f"[LOI] NGHIEM TRONG: Lap trinh vien khong the sua loi sau {max_retries} lan thu. Dung lai.")
        return

    # --- PHASE 3: PRODUCTION / GIAI DOAN 3: SAN XUAT ---
    print("\n[PHASE 3] PRODUCTION...")
    print("[GIAI DOAN 3] SAN XUAT...")
    
    print("[TTS] Creating voiceover / Dang tao loi thoai...")
    voice_task = tasks.voiceover_task(voice_artist)
    voice_result = voice_task.execute(agent=voice_artist)
    print(f"[OK] Voiceover created / Loi thoai da duoc tao: {voice_result}")

    print("[RENDER] Building final video / Dang dung video cuoi cung...")
    production_task = tasks.production_task(producer)
    final_result = production_task.execute(agent=producer)
    print(f"[OK] Final video created / Video cuoi cung da duoc tao: {final_result}")
    
    print("\n=== VIDEO PRODUCTION COMPLETE! / QUY TRINH SAN XUAT VIDEO DA HOAN TAT! ===")


# --------------------------------------------------------------------------
# STEP 5: PROGRAM ENTRY POINT / DIEM KHOI DAU CHUONG TRINH
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()