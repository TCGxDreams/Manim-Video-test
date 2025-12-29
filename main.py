import os
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# BƯỚC 1: CẤU HÌNH MÔI TRƯỜNG VÀ XÁC THỰC
# Phải thực hiện TRƯỚC khi import các thư viện của dự án
# --------------------------------------------------------------------------
# Thiết lập biến môi trường để sử dụng tệp Service Account.
# Đây là phương pháp xác thực đáng tin cậy nhất.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# Tải các biến môi trường từ file .env (chỉ cần cho SERPER_API_KEY)
load_dotenv()

# Import các thành phần của dự án
from src.agents import VideoAgents
from src.tasks import VideoTasks
from langchain_google_genai import ChatGoogleGenerativeAI


# --------------------------------------------------------------------------
# BƯỚC 2: KHỞI TẠO CÁC MÔ HÌNH NGÔN NGỮ (LLM) VÀ AGENT
# --------------------------------------------------------------------------

# Kiểm tra xem SERPER_API_KEY đã được thiết lập chưa
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    print("Vui lòng thiết lập SERPER_API_KEY trong file .env")
    exit()

# Khởi tạo hai "bộ não" AI riêng biệt cho các nhiệm vụ khác nhau
print("🧠 Khởi tạo LLM Flash cho các tác vụ sáng tạo...")
llm_flash = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1 # Tăng nhiệt độ để kịch bản sáng tạo hơn
)

print("💻 Khởi tạo LLM Pro cho tác vụ viết code...")
llm_pro = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.4 # Giảm nhiệt độ để code logic và chính xác hơn
)

# Khởi tạo các lớp chứa định nghĩa Agent và Task
agents = VideoAgents()
tasks = VideoTasks()

# Phân công đúng LLM cho đúng Agent
print("👥 Phân công LLM cho các Agent chuyên biệt...")
storyteller = agents.storyteller_agent(llm_flash)
manim_dev = agents.manim_developer_agent(llm_pro) 
qa_engineer = agents.qa_engineer_agent(llm_flash)
voice_artist = agents.voiceover_artist_agent(llm_flash)
producer = agents.production_engineer_agent(llm_flash)


# --------------------------------------------------------------------------
# BƯỚC 3: ĐỊNH NGHĨA QUY TRÌNH LÀM VIỆC CHÍNH
# --------------------------------------------------------------------------

def main():
    """
    Hàm chính điều khiển toàn bộ quy trình sản xuất video,
    bao gồm cả vòng lặp tự sửa lỗi.
    """
    video_topic = "Đạo hàm cơ bản - derivative of x^n, sin(x), e^x - video 1 phút tiếng Việt"
    max_retries = 5 # Số lần tối đa cho phép Lập trình viên sửa lỗi

    print(f"\n🎬 Bắt đầu quy trình sản xuất nâng cao cho chủ đề: '{video_topic}'")

    # --- GIAI ĐOẠN 1: SÁNG TẠO KỊCH BẢN ---
    print("\n📝 GIAI ĐOẠN 1: SÁNG TẠO KỊCH BẢN...")
    story_task = tasks.storytelling_task(storyteller, video_topic)
    script_result = story_task.execute(agent=storyteller)
    print(f"✅ Kịch bản đã được tạo: {script_result}")

    # --- GIAI ĐOẠN 2: VÒNG LẶP PHÁT TRIỂN & SỬA LỖI ---
    print("\n💻 GIAI ĐOẠN 2: BẮT ĐẦU VÒNG LẶP PHÁT TRIỂN & SỬA LỖI...")
    
    # Lấy đối tượng task code ban đầu
    code_task = tasks.manim_development_task(manim_dev)
    
    current_error_report = "" # Báo cáo lỗi ban đầu là rỗng
    is_code_approved = False  # Cờ để kiểm tra xem mã đã được duyệt chưa

    for i in range(max_retries):
        print(f"\n--- Lần thử #{i + 1}/{max_retries} ---")
        
        # Nếu có báo cáo lỗi từ lần trước, hãy cập nhật mô tả nhiệm vụ cho Lập trình viên
        if current_error_report:
            code_task.description = (
                "Mã nguồn trước đó của bạn đã gặp lỗi khi thực thi. "
                "Hãy đọc kỹ báo cáo lỗi dưới đây, phân tích nguyên nhân và viết lại toàn bộ mã cho chính xác. "
                "Hãy chắc chắn bạn tuân thủ nghiêm ngặt 'Sổ tay Lập trình Manim' trong vai trò của mình.\n"
                f"--- BÁO CÁO LỖI TỪ QA ---\n{current_error_report}\n--- HẾT BÁO CÁO LỖI ---\n\n"
                "Nhiệm vụ ban đầu: "
                f"Đọc phần [VISUAL SCRIPT] từ tệp '{tasks.script_file}' và viết mã Manim hoàn chỉnh. "
                f"Lưu mã vào tệp '{tasks.manim_code_file}'."
            )
        
        print("👨‍💻 Lập trình viên đang viết/sửa mã...")
        code_result = code_task.execute(agent=manim_dev)
        print(f"✅ Mã đã được viết/sửa: {code_result}")

        print("🕵️  QA đang kiểm tra mã...")
        qa_task = tasks.qa_task(qa_engineer)
        qa_result = qa_task.execute(agent=qa_engineer)

        print(f"📝 Kết quả từ QA:\n{qa_result}")

        # Kiểm tra kết quả từ QA
        if "THÀNH CÔNG" in qa_result.upper():
            print("\n🎉 QA đã phê duyệt mã! Chuyển sang giai đoạn sản xuất.")
            is_code_approved = True
            break # Thoát khỏi vòng lặp sửa lỗi
        else:
            print("🐞 QA đã tìm thấy lỗi. Chuẩn bị cho lần sửa tiếp theo.")
            current_error_report = qa_result # Lưu báo cáo lỗi cho lần lặp sau
    
    # Kiểm tra xem vòng lặp có thành công không
    if not is_code_approved:
        print(f"\n❌ LỖI NGHIÊM TRỌNG: Lập trình viên không thể sửa lỗi sau {max_retries} lần thử. Dừng quy trình.")
        return # Dừng toàn bộ chương trình

    # --- GIAI ĐOẠN 3: SẢN XUẤT (TẠO ÂM THANH & DỰNG PHIM) ---
    print("\n🎬 GIAI ĐOẠN 3: SẢN XUẤT...")
    
    # Tạo lời thoại
    print("🎤 Đang tạo lời thoại...")
    voice_task = tasks.voiceover_task(voice_artist)
    voice_result = voice_task.execute(agent=voice_artist)
    print(f"✅ Lời thoại đã được tạo: {voice_result}")

    # Dựng video cuối cùng
    print("🎥 Đang dựng video cuối cùng...")
    production_task = tasks.production_task(producer)
    final_result = production_task.execute(agent=producer)
    print(f"✅ Video cuối cùng đã được tạo: {final_result}")
    
    print("\n✨✨✨ QUY TRÌNH SẢN XUẤT VIDEO ĐÃ HOÀN TẤT! ✨✨✨")


# --------------------------------------------------------------------------
# BƯỚC 5: ĐIỂM KHỞI ĐẦU CỦA CHƯƠNG TRÌNH
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()