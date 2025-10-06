# src/tasks.py - Phiên bản đã được đơn giản hóa

from crewai import Task

class VideoTasks:
    def __init__(self):
        self.script_file = "video_script.txt"
        self.manim_code_file = "manim_animation.py"
        self.voiceover_file = "voiceover.mp3"
        self.silent_video_file = "animation_scene.mp4"
        self.final_video_file = "final_video.mp4"

    # --- TẤT CẢ CÁC HÀM DƯỚI ĐÂY ĐÃ ĐƯỢC SỬA ---

    def storytelling_task(self, agent, topic):
        return Task(
            description=(
                f"Nghiên cứu chủ đề '{topic}', sau đó viết một kịch bản video ngắn gọn. "
                "YÊU CẦU QUAN TRỌNG: Phần [VOICEOVER SCRIPT] phải có độ dài khoảng 130-150 từ. "
                "Phần [VISUAL SCRIPT] nên tập trung vào 2-3 cảnh chính. "
                "Kịch bản phải có hai phần: [VISUAL SCRIPT] và [VOICEOVER SCRIPT]. "
                f"Cuối cùng, sử dụng công cụ 'File Write Tool' để lưu toàn bộ kịch bản vào tệp '{self.script_file}'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ công cụ 'File Write Tool' cho biết tệp '{self.script_file}' đã được ghi thành công."
            ),
            agent=agent
            # Không có tham số 'context'
        )

    # Thay đổi ở đây: xóa tham số context_task
    def manim_development_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung từ tệp '{self.script_file}'. Dựa vào phần [VISUAL SCRIPT], hãy viết mã Manim hoàn chỉnh. "
                f"Sau đó, sử dụng công cụ 'File Write Tool' để lưu mã vào tệp '{self.manim_code_file}'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ 'File Write Tool' cho biết tệp '{self.manim_code_file}' đã được ghi thành công."
            ),
            agent=agent
            # Không có tham số 'context'
        )

    # Thay đổi ở đây: xóa tham số context_task
    def qa_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung mã Python từ tệp '{self.manim_code_file}'. "
                "Tìm tên của lớp Manim trong mã. "
                "Sử dụng công cụ 'Manim Code Execution Tool' với `manim_code` (nội dung mã) và `class_name` (tên lớp) để thực thi nó."
            ),
            expected_output=(
                "Một chuỗi xác nhận việc thực thi Manim thành công hoặc một báo cáo lỗi chi tiết nếu thất bại."
            ),
            agent=agent
            # Không có tham số 'context'
        )

    # Thay đổi ở đây: xóa tham số context_task
    def voiceover_task(self, agent):
        return Task(
            description=(
                f"Đọc nội dung từ tệp '{self.script_file}'. "
                f"Sử dụng phần [VOICEOVER SCRIPT] để tạo tệp âm thanh '{self.voiceover_file}' bằng công cụ 'Text to Speech Tool'."
            ),
            expected_output=(
                f"Chuỗi xác nhận từ 'Text to Speech Tool' cho biết tệp '{self.voiceover_file}' đã được lưu thành công."
            ),
            agent=agent
            # Không có tham số 'context'
        )

    # Thay đổi ở đây: xóa các tham số context
    def production_task(self, agent):
        return Task(
            description=(
                f"Sử dụng công cụ 'FFmpeg Video-Audio Merger' để ghép tệp video '{self.silent_video_file}' với tệp âm thanh '{self.voiceover_file}'. "
                f"Đặt tên tệp đầu ra cuối cùng là '{self.final_video_file}'."
            ),
            expected_output=(
                f"Một thông báo xác nhận video cuối cùng đã được tạo tại 'workspace/{self.final_video_file}'."
            ),
            agent=agent
            # Không có tham số 'context'
        )