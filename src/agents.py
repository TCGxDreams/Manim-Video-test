# src/agents.py - 3BLUE1BROWN AESTHETIC + MANIM COMMUNITY COMPATIBLE

from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.file_tools import FileWriteTool, CustomFileReadTool
from .tools.manim_tools import ManimExecutionTool, FFmpegTool, VideoDurationTool
from .tools.tts_tools import TextToSpeechTool, EnhancedTTSTool

# Khởi tạo các công cụ
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
file_write_tool = FileWriteTool()
file_read_tool = CustomFileReadTool() 
tts_tool = TextToSpeechTool()
enhanced_tts_tool = EnhancedTTSTool()
manim_tool = ManimExecutionTool()
ffmpeg_tool = FFmpegTool()
duration_tool = VideoDurationTool()


# ============================================================================
# SỔ TAY MANIM - MANIM COMMUNITY v0.18 COMPATIBLE
# ============================================================================
MANIM_HANDBOOK = '''
=== SỔ TAY MANIM - MANIM COMMUNITY v0.18 ===

[WARNING] QUAN TRỌNG: Đây là Manim Community, KHÔNG phải manimgl của 3B1B!
[WARNING] KHÔNG dùng: get_tangent_line() - không có trong API này


[COLORS] BẢNG MÀU


TEAL_E = "#49A88F"   # Graph 
GOLD_E = "#C78D46"   # Highlights
BLUE_E = "#1C758A"   # Area
GREY_A = "#DDDDDD"   # Axes


[WARNING] KHÔNG DÙNG TANGENT LINE - QUÁ PHỨC TẠP


Thay vì dùng tangent line động, hãy dùng:
- Hiển thị công thức đạo hàm
- Dùng arrow để chỉ độ dốc
- Dùng animations đơn giản với Transform


MẪU 1: VIDEO ĐẠO HÀM ĐƠN GIẢN (ĐÃ TEST)


```python
from manim import *
import numpy as np

TEAL_E = "#49A88F"
GOLD_E = "#C78D46"  
BLUE_E = "#1C758A"
GREY_A = "#DDDDDD"

class DerivativeVideo(Scene):
    def construct(self):
        # === SCENE 1: Power Rule ===
        title = Text("Đạo hàm x^n", font_size=36).to_corner(UL)
        
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 10, 2],
            x_length=6, y_length=4,
            axis_config={"color": GREY_A}
        ).move_to(ORIGIN)
        
        graph = axes.plot(lambda x: x**2, x_range=[0.1, 3], color=TEAL_E, stroke_width=4)
        
        formula1 = MathTex(r"f(x) = x^n", font_size=40).to_edge(DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(Create(axes), run_time=2)
        self.play(Create(graph), run_time=2)
        self.play(Write(formula1), run_time=1)
        self.wait(1)
        
        # Transform formula
        formula2 = MathTex(r"f'(x) = n \\cdot x^{n-1}", font_size=40, color=GOLD_E).to_edge(DOWN, buff=0.5)
        self.play(Transform(formula1, formula2), run_time=1.5)
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(VGroup(title, axes, graph, formula1)), run_time=1)
        
        # === SCENE 2: sin(x) ===
        title2 = Text("Đạo hàm sin(x)", font_size=36).to_corner(UL)
        
        axes2 = Axes(
            x_range=[0, 2*PI, PI/2], y_range=[-1.5, 1.5, 0.5],
            x_length=8, y_length=3,
            axis_config={"color": GREY_A}
        ).move_to(ORIGIN)
        
        sin_graph = axes2.plot(lambda x: np.sin(x), color=TEAL_E, stroke_width=4)
        cos_graph = axes2.plot(lambda x: np.cos(x), color=GOLD_E, stroke_width=3)
        
        formula3 = MathTex(r"\\frac{d}{dx}[\\sin(x)] = \\cos(x)", font_size=40).to_edge(DOWN, buff=0.5)
        
        self.play(Write(title2), Create(axes2), run_time=1.5)
        self.play(Create(sin_graph), run_time=2)
        self.play(Create(cos_graph), Write(formula3), run_time=2)
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(VGroup(title2, axes2, sin_graph, cos_graph, formula3)), run_time=1)
        
        # === SCENE 3: e^x ===
        title3 = Text("Đạo hàm e^x", font_size=36).to_corner(UL)
        
        axes3 = Axes(
            x_range=[-1, 3, 1], y_range=[0, 8, 2],
            x_length=6, y_length=4,
            axis_config={"color": GREY_A}
        ).move_to(ORIGIN)
        
        exp_graph = axes3.plot(lambda x: np.exp(x), x_range=[-1, 2], color=TEAL_E, stroke_width=4)
        
        formula4 = MathTex(r"\\frac{d}{dx}[e^x] = e^x", font_size=40).to_edge(DOWN, buff=0.5)
        special = Text("Hàm số đặc biệt!", font_size=28, color=GOLD_E).next_to(formula4, UP, buff=0.3)
        
        self.play(Write(title3), Create(axes3), run_time=1.5)
        self.play(Create(exp_graph), run_time=2)
        self.play(Write(formula4), FadeIn(special), run_time=1.5)
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(VGroup(title3, axes3, exp_graph, formula4, special)), run_time=1)
        
        # === SCENE 4: Summary ===
        summary_title = Text("Tổng kết", font_size=42, color=WHITE).shift(UP*2.5)
        
        formulas = VGroup(
            MathTex(r"\\frac{d}{dx}[x^n] = n \\cdot x^{n-1}"),
            MathTex(r"\\frac{d}{dx}[\\sin(x)] = \\cos(x)"),
            MathTex(r"\\frac{d}{dx}[e^x] = e^x"),
        ).arrange(DOWN, buff=0.6).scale(1.1)
        
        self.play(Write(summary_title), run_time=1)
        for f in formulas:
            self.play(Write(f), run_time=1)
            self.play(f.animate.set_color(GOLD_E), run_time=0.3)
            self.play(f.animate.set_color(WHITE), run_time=0.3)
        
        thanks = Text("Cảm ơn bạn đã xem!", font_size=36).shift(DOWN*2.5)
        self.play(Write(thanks), run_time=1)
        self.wait(2)
```


LUẬT BẮT BUỘC


[OK] DÙNG:
- axes.plot() để vẽ đồ thị
- Create(), Write(), FadeIn(), FadeOut()
- Transform(), ReplacementTransform()
- VGroup() để nhóm objects
- .to_corner(UL), .to_edge(DOWN), .move_to(ORIGIN)

[ERROR] KHÔNG DÙNG:
- get_tangent_line() - KHÔNG TỒN TẠI
- always_redraw() với tangent - QUÁ PHỨC TẠP
- ValueTracker với moving dots - DỄ LỖI

=== KẾT THÚC SỔ TAY ===
'''


class VideoAgents:
    def storyteller_agent(self, llm):
        return Agent(
            role="Nhà biên kịch Video đơn giản",
            goal="Viết kịch bản video đơn giản, không yêu cầu tangent line hay moving dots.",
            backstory=(
                "Bạn viết kịch bản đơn giản:\n"
                "- KHÔNG mô tả đường tiếp tuyến di chuyển\n"
                "- KHÔNG mô tả điểm di chuyển trên graph\n"
                "- CHỈ mô tả: vẽ graph, hiển thị công thức, transform formula\n"
            ),
            tools=[file_write_tool],
            llm=llm,
            verbose=True
        )

    def manim_developer_agent(self, llm_pro):
        return Agent(
            role="Lập trình viên Manim Community v0.18",
            goal="Viết mã Manim đơn giản, KHÔNG dùng tangent line, KHÔNG dùng always_redraw.",
            backstory=(
                "QUY TẮC NGHIÊM NGẶT:\n"
                "[ERROR] KHÔNG dùng get_tangent_line() - không có trong API\n"
                "[ERROR] KHÔNG dùng always_redraw() với moving tangent\n"
                "[ERROR] KHÔNG dùng ValueTracker phức tạp\n\n"
                "[OK] CHỈ dùng:\n"
                "- axes.plot() để vẽ graph\n"
                "- Create(), Write(), FadeOut(), Transform()\n"
                "- MathTex(), Text()\n"
                "- VGroup().arrange()\n\n"
                f"{MANIM_HANDBOOK}"
            ),
            tools=[file_read_tool, file_write_tool],
            llm=llm_pro,
            verbose=True
        )

    def qa_engineer_agent(self, llm):
        return Agent(
            role="Kỹ sư QA",
            goal="Chạy mã Manim.",
            backstory="Chạy mã. Nếu lỗi, báo lỗi cụ thể.",
            tools=[file_read_tool, manim_tool],
            llm=llm,
            verbose=True
        )

    def voiceover_artist_agent(self, llm):
        return Agent(
            role="Nghệ sĩ Lồng tiếng",
            goal="Tạo audio từ script.",
            backstory="Đọc [VOICEOVER SCRIPT] và tạo MP3.",
            tools=[file_read_tool, tts_tool],
            verbose=True,
            llm=llm
        )

    def production_engineer_agent(self, llm):
        return Agent(
            role="Kỹ sư Sản xuất",
            goal="Ghép video và audio.",
            backstory="Dùng FFmpeg merge.",
            tools=[ffmpeg_tool, duration_tool],
            verbose=True,
            llm=llm
        )