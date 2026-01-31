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
                f"Nghiên cứu chủ đề '{topic}', sau đó viết một kịch bản video ngắn gọn.\n\n"
                "YÊU CẦU QUAN TRỌNG:\n"
                "1. Phần [VOICEOVER SCRIPT] phải có độ dài khoảng 130-150 từ (cho video 1 phút).\n"
                "2. Phần [VISUAL SCRIPT] nên chia thành 3-4 SCENE với timing.\n"
                "3. Thêm phần [TIMING] ở cuối với tổng thời lượng ước tính.\n\n"
                "FORMAT:\n"
                "```\n"
                "[VISUAL SCRIPT]\n"
                "SCENE 1 (10s): Mô tả scene 1\n"
                "SCENE 2 (15s): Mô tả scene 2\n"
                "...\n\n"
                "[VOICEOVER SCRIPT]\n"
                "Nội dung lời thoại...\n\n"
                "[TIMING]\n"
                "- Tổng thời lượng video: ~60s (1 phút)\n"
                "- Tổng thời lượng audio ước tính: ~55s\n"
                "```\n\n"
                f"Cuối cùng, sử dụng công cụ 'File Write Tool' để lưu toàn bộ kịch bản vào tệp '{self.script_file}'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ công cụ 'File Write Tool' cho biết tệp '{self.script_file}' đã được ghi thành công."
            ),
            agent=agent
        )

    def manim_development_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung từ tệp '{self.script_file}'. Dựa vào phần [VISUAL SCRIPT], hãy viết mã Manim hoàn chỉnh.\n\n"
                "YÊU CẦU QUAN TRỌNG:\n"
                "1. Tuân thủ nghiêm ngặt SỔ TAY LẬP TRÌNH MANIM trong backstory của bạn.\n"
                "2. Sử dụng timing từ script để đặt run_time phù hợp cho mỗi animation.\n"
                "3. Thêm self.wait() giữa các scene để người xem có thời gian hiểu.\n"
                "4. Render với chất lượng 'h' (1080p) khi hoàn tất.\n\n"
                f"Sau đó, sử dụng công cụ 'File Write Tool' để lưu mã vào tệp '{self.manim_code_file}'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ 'File Write Tool' cho biết tệp '{self.manim_code_file}' đã được ghi thành công."
            ),
            agent=agent
        )

    def qa_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung mã Python từ tệp '{self.manim_code_file}'.\n"
                "Tìm tên của lớp Manim trong mã.\n\n"
                "Sử dụng công cụ 'Manim Code Execution Tool' với các tham số:\n"
                "- manim_code: nội dung mã Python\n"
                "- class_name: tên lớp Manim\n"
                "- quality: 'h' (1080p - mặc định, chất lượng cao)\n"
                "- fps: 30 (frame rate mặc định)\n\n"
                "NẾU THẤT BẠI: Tạo báo cáo lỗi theo format trong backstory của bạn.\n"
                "NẾU THÀNH CÔNG: Ghi nhận thời lượng video và xác nhận thành công."
            ),
            expected_output=(
                "Một chuỗi xác nhận việc thực thi Manim thành công (bao gồm đường dẫn video và thời lượng) "
                "hoặc một báo cáo lỗi chi tiết theo format chuẩn nếu thất bại."
            ),
            agent=agent
        )

    def voiceover_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung từ tệp '{self.script_file}'.\n\n"
                "Sử dụng phần [VOICEOVER SCRIPT] để tạo tệp âm thanh bằng công cụ 'Text to Speech Tool'.\n\n"
                "LƯU Ý:\n"
                "1. Công cụ sẽ tự động detect ngôn ngữ (English/Vietnamese).\n"
                "2. Ghi nhận thời lượng audio được trả về.\n"
                "3. Nếu nội dung phức tạp, có thể dùng slow=True để đọc chậm hơn.\n\n"
                f"Lưu audio vào tệp '{self.voiceover_file}'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ 'Text to Speech Tool' cho biết tệp '{self.voiceover_file}' đã được lưu thành công, "
                "bao gồm thông tin về thời lượng audio."
            ),
            agent=agent
        )

    def production_task(self, agent):
        return Task(
            description=(
                f"Ghép tệp video '{self.silent_video_file}' với tệp âm thanh '{self.voiceover_file}'.\n\n"
                "Sử dụng công cụ 'FFmpeg Video-Audio Merger' với các tham số:\n"
                "- video_file: '{self.silent_video_file}'\n"
                "- audio_file: '{self.voiceover_file}'\n"
                "- output_file: '{self.final_video_file}'\n"
                "- speed_adjust: True (tự động điều chỉnh tốc độ video để khớp audio)\n\n"
                "TRƯỚC KHI MERGE: Có thể dùng 'Media Duration Tool' để kiểm tra thời lượng của cả hai file."
            ),
            expected_output=(
                f"Một thông báo xác nhận video cuối cùng đã được tạo tại 'workspace/{self.final_video_file}', "
                "bao gồm thông tin về duration và speed adjustment nếu có."
            ),
            agent=agent
        )