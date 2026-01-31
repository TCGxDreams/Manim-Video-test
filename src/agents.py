# src/agents.py - Bilingual MANIM COMMUNITY COMPATIBLE

from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.file_tools import FileWriteTool, CustomFileReadTool
from .tools.manim_tools import ManimExecutionTool, FFmpegTool, VideoDurationTool
from .tools.tts_tools import TextToSpeechTool, EnhancedTTSTool

# Initialize tools / Khoi tao cac cong cu
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
# MANIM HANDBOOK - MANIM COMMUNITY v0.18 COMPATIBLE
# SO TAY MANIM - TUONG THICH MANIM COMMUNITY v0.18
# ============================================================================
MANIM_HANDBOOK = '''
=== MANIM HANDBOOK / SO TAY MANIM - MANIM COMMUNITY v0.18 ===

[WARNING] This is Manim Community, NOT manimgl from 3B1B!
[CANH BAO] Day la Manim Community, KHONG phai manimgl cua 3B1B!

[WARNING] Do NOT use: get_tangent_line() - not available in this API
[CANH BAO] KHONG dung: get_tangent_line() - khong co trong API nay

---
COLOR PALETTE / BANG MAU
---

TEAL_E = "#49A88F"   # Graph / Do thi
GOLD_E = "#C78D46"   # Highlights / Noi bat
BLUE_E = "#1C758A"   # Area / Vung
GREY_A = "#DDDDDD"   # Axes / Truc toa do

---
[WARNING] DO NOT USE TANGENT LINE - TOO COMPLEX
[CANH BAO] KHONG DUNG TANGENT LINE - QUA PHUC TAP
---

Instead of dynamic tangent lines, use:
Thay vi dung tangent line dong, hay dung:
- Display derivative formula / Hien thi cong thuc dao ham
- Use arrows to show slope / Dung mui ten de chi do doc
- Use simple animations with Transform / Dung animations don gian voi Transform

---
TEMPLATE 1: SIMPLE DERIVATIVE VIDEO (TESTED)
MAU 1: VIDEO DAO HAM DON GIAN (DA TEST)
---

```python
from manim import *
import numpy as np

TEAL_E = "#49A88F"
GOLD_E = "#C78D46"  
BLUE_E = "#1C758A"
GREY_A = "#DDDDDD"

class DerivativeVideo(Scene):
    def construct(self):
        # === SCENE 1: Power Rule / Quy tac luy thua ===
        title = Text("Derivative x^n", font_size=36).to_corner(UL)
        # Vietnamese: title = Text("Dao ham x^n", font_size=36).to_corner(UL)
        
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
        
        # Transform formula / Bien doi cong thuc
        formula2 = MathTex(r"f'(x) = n \\cdot x^{n-1}", font_size=40, color=GOLD_E).to_edge(DOWN, buff=0.5)
        self.play(Transform(formula1, formula2), run_time=1.5)
        self.wait(2)
        
        # Cleanup / Don dep
        self.play(FadeOut(VGroup(title, axes, graph, formula1)), run_time=1)
        
        # === SCENE 2: sin(x) ===
        title2 = Text("Derivative sin(x)", font_size=36).to_corner(UL)
        
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
        title3 = Text("Derivative e^x", font_size=36).to_corner(UL)
        
        axes3 = Axes(
            x_range=[-1, 3, 1], y_range=[0, 8, 2],
            x_length=6, y_length=4,
            axis_config={"color": GREY_A}
        ).move_to(ORIGIN)
        
        exp_graph = axes3.plot(lambda x: np.exp(x), x_range=[-1, 2], color=TEAL_E, stroke_width=4)
        
        formula4 = MathTex(r"\\frac{d}{dx}[e^x] = e^x", font_size=40).to_edge(DOWN, buff=0.5)
        special = Text("Special function!", font_size=28, color=GOLD_E).next_to(formula4, UP, buff=0.3)
        # Vietnamese: special = Text("Ham so dac biet!", font_size=28, color=GOLD_E)
        
        self.play(Write(title3), Create(axes3), run_time=1.5)
        self.play(Create(exp_graph), run_time=2)
        self.play(Write(formula4), FadeIn(special), run_time=1.5)
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(VGroup(title3, axes3, exp_graph, formula4, special)), run_time=1)
        
        # === SCENE 4: Summary / Tong ket ===
        summary_title = Text("Summary", font_size=42, color=WHITE).shift(UP*2.5)
        # Vietnamese: summary_title = Text("Tong ket", font_size=42, color=WHITE)
        
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
        
        thanks = Text("Thanks for watching!", font_size=36).shift(DOWN*2.5)
        # Vietnamese: thanks = Text("Cam on ban da xem!", font_size=36)
        self.play(Write(thanks), run_time=1)
        self.wait(2)
```

---
MANDATORY RULES / LUAT BAT BUOC
---

[OK] USE / DUNG:
- axes.plot() to draw graphs / de ve do thi
- Create(), Write(), FadeIn(), FadeOut()
- Transform(), ReplacementTransform()
- VGroup() to group objects / de nhom objects
- .to_corner(UL), .to_edge(DOWN), .move_to(ORIGIN)

[ERROR] DO NOT USE / KHONG DUNG:
- get_tangent_line() - DOES NOT EXIST / KHONG TON TAI
- always_redraw() with tangent - TOO COMPLEX / QUA PHUC TAP
- ValueTracker with moving dots - ERROR PRONE / DE LOI

=== END OF HANDBOOK / KET THUC SO TAY ===
'''


class VideoAgents:
    def storyteller_agent(self, llm):
        return Agent(
            role="Simple Video Scriptwriter / Nguoi viet kich ban video don gian",
            goal="Write simple video scripts without tangent lines or moving dots.",
            backstory=(
                "You write simple scripts (supports both English and Vietnamese):\n"
                "Ban viet kich ban don gian (ho tro ca tieng Anh va tieng Viet):\n"
                "- DO NOT describe moving tangent lines / KHONG mo ta duong tiep tuyen di chuyen\n"
                "- DO NOT describe moving points on graph / KHONG mo ta diem di chuyen tren graph\n"
                "- ONLY describe: draw graph, display formula, transform formula\n"
                "  CHI mo ta: ve graph, hien thi cong thuc, bien doi cong thuc\n"
            ),
            tools=[file_write_tool],
            llm=llm,
            verbose=True
        )

    def manim_developer_agent(self, llm_pro):
        return Agent(
            role="Manim Community v0.18 Developer",
            goal="Write simple Manim code, DO NOT use tangent line, DO NOT use always_redraw.",
            backstory=(
                "STRICT RULES / QUY TAC NGHIEM NGAT:\n"
                "[ERROR] DO NOT use get_tangent_line() - not in API\n"
                "[LOI] KHONG dung get_tangent_line() - khong co trong API\n"
                "[ERROR] DO NOT use always_redraw() with moving tangent\n"
                "[LOI] KHONG dung always_redraw() voi tangent di chuyen\n"
                "[ERROR] DO NOT use complex ValueTracker\n"
                "[LOI] KHONG dung ValueTracker phuc tap\n\n"
                "[OK] ONLY use / CHI dung:\n"
                "- axes.plot() to draw graph / de ve graph\n"
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
            role="QA Engineer / Ky su QA",
            goal="Run Manim code. / Chay ma Manim.",
            backstory="Run code. If error, report specific error. / Chay ma. Neu loi, bao loi cu the.",
            tools=[file_read_tool, manim_tool],
            llm=llm,
            verbose=True
        )

    def voiceover_artist_agent(self, llm):
        return Agent(
            role="Voiceover Artist / Nghe si Long tieng",
            goal="Create audio from script. / Tao audio tu script.",
            backstory="Read [VOICEOVER SCRIPT] and create MP3. / Doc [VOICEOVER SCRIPT] va tao MP3.",
            tools=[file_read_tool, tts_tool],
            verbose=True,
            llm=llm
        )

    def production_engineer_agent(self, llm):
        return Agent(
            role="Production Engineer / Ky su San xuat",
            goal="Merge video and audio. / Ghep video va audio.",
            backstory="Use FFmpeg merge. / Dung FFmpeg de ghep.",
            tools=[ffmpeg_tool, duration_tool],
            verbose=True,
            llm=llm
        )