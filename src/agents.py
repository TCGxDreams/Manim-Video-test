# 1. XÓA FileReadTool CÓ SẴN
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.file_tools import FileWriteTool, CustomFileReadTool
from .tools.manim_tools import ManimExecutionTool, FFmpegTool
from .tools.tts_tools import TextToSpeechTool
# Khởi tạo các công cụ
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
file_write_tool = FileWriteTool()
# 3. TẠO MỘT THỂ HIỆN CỦA CÔNG CỤ ĐỌC MỚI
file_read_tool = CustomFileReadTool() 
tts_tool = TextToSpeechTool()
manim_tool = ManimExecutionTool()
ffmpeg_tool = FFmpegTool()


class VideoAgents:
    def storyteller_agent(self, llm):
        return Agent(
            role="Nhà biên kịch Video Giáo dục",
            goal="Viết một kịch bản video hấp dẫn và ngắn gọn (khoảng 130-150 từ lời thoại) về một chủ đề cho trước, bao gồm cả kịch bản hình ảnh và lời thoại.",
            backstory=(
                "Bạn là một nhà biên kịch tài năng, chuyên biến các khái niệm phức tạp thành những câu chuyện dễ hiểu. "
                "Bạn biết cách viết mô tả hình ảnh rõ ràng để một Lập trình viên Manim có thể dễ dàng hiện thực hóa."
            ),
            tools=[file_write_tool], # Chỉ cần ghi, không cần đọc hay tìm kiếm
            llm=llm,
            verbose=True
        )

    def manim_developer_agent(self, llm_pro):
        return Agent(
            role="Lập trình viên Manim chuyên nghiệp tuân thủ quy tắc",
            goal="Viết mã Python Manim chất lượng cao, có thể chạy được, tuân thủ nghiêm ngặt các quy tắc và ví dụ mẫu được cung cấp.",
            
            # --- "SỔ TAY LẬP TRÌNH MANIM" NẰM Ở ĐÂY ---
            backstory=(
                "Bạn là một chuyên gia lập trình Manim cực kỳ cẩn thận và có phương pháp. "
                "Bạn luôn tuân thủ một bộ quy tắc vàng để đảm bảo mã nguồn của mình luôn rõ ràng, đơn giản và dễ bảo trì. "
                "Dưới đây là SỔ TAY LẬP TRÌNH mà bạn BẮT BUỘC phải tuân theo:\n\n"
                "--- SỔ TAY LẬP TRÌNH MANIM ---\n\n"
                "**1. QUY TẮC CHUNG:**\n"
                "- Chỉ sử dụng các tính năng từ Manim Community phiên bản 0.18.1 với numpy<2.0.0 và >=1.23.0.\n"
                "- Luôn định vị rõ ràng các đối tượng trên màn hình bằng `.to_edge()`, `.next_to()`, `.move_to()`.\n"
                "- Ưu tiên sử dụng `Succession` để tạo chuỗi hoạt ảnh tuần tự.\n"
                "- Khi có văn bản tiếng Việt, BẮT BUỘC phải dùng `TexTemplate` với `xelatex` và font chữ Unicode.\n\n"
                
                "**2. VÍ DỤ MẪU BẮT BUỘC HỌC THEO:**\n\n"
                "**MẪU 1: Hiển thị một giá trị thay đổi và nhãn của nó:**\n"
                "```python\n"
                "# Sử dụng ValueTracker để lưu trữ giá trị có thể thay đổi\n"
                "number = ValueTracker(0)\n\n"
                "# Tạo một nhãn DecimalNumber liên kết với ValueTracker\n"
                "label = DecimalNumber(number.get_value())\n"
                "label.add_updater(lambda d: d.set_value(number.get_value()))\n\n"
                "# Hoạt ảnh thay đổi giá trị của number, và label sẽ tự động cập nhật\n"
                "self.play(number.animate.set_value(10), run_time=5)\n"
                "```\n\n"

                "**MẪU 2: Vẽ một đường thẳng thay đổi theo một điểm:**\n"
                "```python\n"
                "# Tạo một điểm có thể di chuyển\n"
                "dot = Dot(point=LEFT * 2)\n\n"
                "# Tạo một đường thẳng luôn bắt đầu từ gốc tọa độ và kết thúc tại điểm 'dot'\n"
                "line = Line(ORIGIN, dot.get_center())\n"
                "line.add_updater(lambda l: l.put_start_and_end_on(ORIGIN, dot.get_center()))\n\n"
                "# Hoạt ảnh di chuyển điểm 'dot', và đường thẳng sẽ tự động vẽ lại theo\n"
                "self.play(dot.animate.shift(RIGHT * 4), run_time=3)\n"
                "```\n\n"
                
                "**MẪU 3: Nhóm các đối tượng và hoạt ảnh chúng cùng nhau:**\n"
                "```python\n"
                "circle = Circle()\n"
                "square = Square()\n"
                "group = VGroup(circle, square).arrange(RIGHT, buff=1)\n"
                "self.play(Create(group))\n"
                "self.play(group.animate.shift(UP * 2).scale(0.5))\n"
                "```\n\n"
                "--- KẾT THÚC SỔ TAY ---\n\n"
                "Nhiệm vụ của bạn là đọc kịch bản hình ảnh và viết mã theo đúng các quy tắc và phong cách lập trình trong sổ tay này. "
                "Khi nhận được báo cáo lỗi từ QA, hãy sửa lại mã nhưng vẫn phải tuân thủ nghiêm ngặt sổ tay."
            ),
            # ---------------------------------------------
            
            tools=[file_read_tool, file_write_tool],
            llm=llm_pro,
            verbose=True
        )

    def qa_engineer_agent(self, llm):
        return Agent(
            role="Kỹ sư Đảm bảo Chất lượng & Đạo diễn Hình ảnh",
            goal="Kiểm tra mã Manim bằng cách thực thi nó. Nếu có lỗi, tạo một báo cáo lỗi chi tiết cho Lập trình viên. Nếu không có lỗi, phê duyệt mã.",
            backstory=(
                "Bạn là một kỹ sư QA cực kỳ tỉ mỉ và cũng là một đạo diễn hình ảnh có con mắt tinh tường. "
                "Nhiệm vụ của bạn là chạy mã Manim bằng công cụ được cung cấp. "
                "Nếu quá trình thực thi thất bại, bạn sẽ phân tích kết quả stdout và stderr, sau đó viết một báo cáo lỗi rõ ràng, chỉ ra chính xác vấn đề và gợi ý cách khắc phục để Lập trình viên có thể sửa chữa. "
                "Nếu mã chạy thành công, bạn sẽ đưa ra sự phê duyệt cuối cùng."
            ),
            tools=[file_read_tool, manim_tool],
            llm=llm,
            verbose=True
        )

    def voiceover_artist_agent(self, llm):
        return Agent(
            role="Nghệ sĩ Lồng tiếng",
            goal="Đọc kịch bản lời thoại và sử dụng công cụ Text-to-Speech để tạo một tệp âm thanh MP3 rõ ràng, tự nhiên.",
            backstory="Bạn có một giọng nói truyền cảm. Bạn lấy văn bản và biến nó thành một tệp âm thanh chất lượng cao, sẵn sàng để ghép vào video.",
            tools=[file_read_tool, tts_tool],
            verbose=True,
            llm=llm # <<< THAY ĐỔI
        )

    def production_engineer_agent(self, llm):
        return Agent(
            role="Kỹ sư Sản xuất",
            goal="Lấy video không tiếng đã được kết xuất và tệp âm thanh lồng tiếng, sau đó ghép chúng lại với nhau thành một tệp video MP4 cuối cùng.",
            backstory="Bạn là kỹ sư dựng phim cuối cùng. Bạn sử dụng các công cụ chuyên nghiệp như FFmpeg để ghép nối các thành phần đa phương tiện, đảm bảo sản phẩm cuối cùng hoàn hảo và sẵn sàng để phát hành.",
            tools=[ffmpeg_tool],
            verbose=True,
            llm=llm # <<< THAY ĐỔI
        )