from manimlib import *
import numpy as np

class S01ShowProblem(Scene):
    def construct(self):
        # Gym 104639 (The 2023 ICPC Asia EC Regionals Online Contest (I)) Problem F
        problem_description_words = TexText("""
            Alice 和 Bob 正在玩游戏。\\\\
            游戏中有三个整数 $a_1,a_2,a_3$。Alice 和 Bob 轮流操作，\\\\
            Alice 先手。\\\\
            每次操作可以选择两个互不相同的整数 $a_i,a_j$ 改变它们的值。\\\\
            设更改后的值为 $a_i'$ 和 $a_j'$，满足 $a_i+a_j=a_i'+a_j'$ \\\\
            且 $|a_i'-a_j'| < |a_i-a_j|$ 时操作才是合法的。\\\\
            不能进行合法操作者输。问谁有必胜策略？
        """, alignment="")
        problem_description_words.to_corner(LEFT)
        self.play(Write(problem_description_words), run_time=10)
        self.wait(2)

class S02DescribeProblem(Scene):
    def construct(self):
        l_lines = VGroup(
            Tex("x_1", ",\\ ", "x_2", ",\\ ", "x_3"),
            Tex("\\Downarrow"),
            Tex("x_1", "+k", ",\\ ", "x_2", "-k", ",\\ ", "x_3"),
        )
        l_lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        r_lines = VGroup(
            Tex("0", ",\\ ", "x_2", "-x_1", ",\\ ", "x_3", "-x_1"),
            Tex("\\Downarrow"),
            Tex("k", ",\\ ", "x_2", "-x_1", "-k", ",\\ ", "x_3", "-x_1"),
        )
        r_lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        columns = VGroup(l_lines, Tex("\\Longleftrightarrow"), r_lines)
        columns.arrange(RIGHT, buff=MED_LARGE_BUFF)
        for column in [l_lines, r_lines]:
            for line in column:
                line.set_color_by_tex_to_color_map({
                    "+k": BLUE,
                    "k": BLUE,
                    "-k": TEAL,
                    "-x_1": GREEN,
                })

        self.play(Write(l_lines[0]))
        self.wait()
        self.play(FadeIn(l_lines[1], DOWN))
        self.play(
            TransformMatchingTex(l_lines[0].copy(), l_lines[2]),
            run_time=2,
        )
        self.wait()
        self.play(FadeIn(columns[1], RIGHT))
        self.play(
            TransformMatchingTex(l_lines[0].copy(), r_lines[0]),
            TransformMatchingTex(l_lines[1].copy(), r_lines[1]),
            TransformMatchingTex(l_lines[2].copy(), r_lines[2]),
            run_time=3,
        )
        self.wait()
        self.play(FadeOut(columns))

        convert_problem = VGroup(Tex("(0,\\ x,\\ y)"), Tex("0 \\leq x \\leq y", font_size=36))
        convert_problem.arrange(DOWN, buff=LARGE_BUFF)
        self.play(FadeIn(convert_problem[0], DOWN))
        self.play(Write(convert_problem[1]))

class S04ReadCode(Scene):
    def construct(self):
        image = ImageMobject('./S04ReadCode.png')
        image.scale(1.4)
        self.play(FadeIn(image))
        note1 = Tex("\\texttt{result[i][j]} \\to (k,i-k,j)")
        note1.move_to(UP * 3.2)
        note2 = Tex("(0,i,j) \\to (k,i-k,j) \\Leftrightarrow (0,i-2k,j-k)", font_size=40)
        note2.move_to(UP * 2 + RIGHT * 3)
        note3 = Tex("(0,i,j) \\to (0,i+k,j-k)", font_size=40)
        note3.move_to(DOWN * 0.5 + RIGHT * 3)
        note4 = Tex("(0,i,j) \\to (k,i,j-k)", font_size=40)
        note4.move_to(DOWN * 2.3 + RIGHT * 4.5)
        self.play(Write(note1))
        self.wait()
        self.play(Write(note2))
        self.wait()
        self.play(Write(note3))
        self.wait()
        self.play(Write(note4))
        self.wait()

def isWinStatusWithSameNumbers(n: int):
    if n == 0:
        return False
    total = 0
    while n % 2 == 0:
        n = n / 2
        total = total + 1
    return total % 2 == 1

def isWinStatus(x: int, y: int):
    if x != 0 and y != x:
        return False
    else:
        return isWinStatusWithSameNumbers(y)

class S05ReadBruteForceResult(Scene):
    def construct(self):
        n = 25
        rows = VGroup(*(
            VGroup(*(
                Square(0.3, stroke_width=1.5, fill_color=GREEN if isWinStatus(i, j) else RED, fill_opacity=1.0) if i <= j else Square(0.3, stroke_width=0)
                for j in range(0, n + 1)
            ))
            for i in range(0, n + 1)
        ))
        for row in rows:
            row.arrange(RIGHT, buff=0)
        rows.arrange(DOWN, buff=0)
        for i in range(0, n + 1):
            self.play(*(
                DrawBorderThenFill(rows[i][j])
                for j in range(i, n + 1)
            ), run_time=0.1)
        arrow1 = Arrow(LEFT * 5 + UP * 2.5, LEFT * 3.6 + UP * 3.9)
        self.play(GrowArrow(arrow1), run_time=0.3)
        note1 = TexText("$(0,0,0)$ is not a winning state", font_size=30)
        note1.move_to(LEFT * 5 + UP * 2.35)
        self.play(Write(note1))
        arrow2 = Arrow(LEFT * 3.2 + UP * 0.7, LEFT * 1.8 + UP * 2.1)
        self.play(GrowArrow(arrow2), run_time=0.3)
        note2 = TexText("$(0,6,6)$ is a winning state", font_size=30)
        note2.move_to(LEFT * 3.2 + UP * 0.55)
        self.play(Write(note2))
        self.wait(5)

class S06AnalysisResult(Scene):
    def construct(self):
        lines = VGroup(
            Tex("(0,0,n)"),
            Tex("(0,n,n)"),
        )
        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(lines[0]), Write(lines[1]))
        self.wait(2)
        self.play(lines.animate.shift(LEFT * 3))
        notes = VGroup(
            Tex("\\Leftrightarrow"),
            Tex("(-n,0,0)"),
            Tex("\\Leftrightarrow"),
            Tex("(0,0,n)"),
        )
        notes.arrange(RIGHT, buff=MED_SMALL_BUFF)
        notes.next_to(lines[1], RIGHT, buff=MED_SMALL_BUFF)
        self.play(FadeIn(notes[0], RIGHT))
        self.play(TransformMatchingTex(lines[1].copy(), notes[1]))
        self.wait(0.3)
        self.play(TransformMatchingTex(notes[1].copy(), notes[3]), FadeIn(notes[2], RIGHT))
