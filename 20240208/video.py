from manimlib import *
import numpy as np

class S01ShowProblem(Scene):
    def construct(self):
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
        self.wait()

class S04ReadCode(Scene):
    def construct(self):
        image = ImageMobject('./S04-code.png')
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
        return True
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
        self.wait(5)
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
        self.wait()

class S07GuessConclusions(Scene):
    def construct(self):
        winningstates1 = VGroup(
            Tex("2"), Tex("6"), Tex("8"),
            Tex("10"), Tex("14"), Tex("18"),
        )
        winningstates2 = VGroup(
            Tex("22"), Tex("24"), Tex("26"),
            Tex("30"), Tex("32"), Tex("34"),
        )
        expressions1 = VGroup(
            Tex("2^1", color=YELLOW), Tex("2^1\\times 3", color=YELLOW), Tex("2^3", color=YELLOW),
            Tex("2^1\\times 5", color=YELLOW), Tex("2^1\\times 7", color=YELLOW), Tex("2^1\\times 9", color=YELLOW),
        )
        expressions2 = VGroup(
            Tex("2^1\\times 11", color=YELLOW), Tex("2^3\\times 8", color=YELLOW), Tex("2^1\\times 13", color=YELLOW),
            Tex("2^1\\times 15", color=YELLOW), Tex("2^5", color=YELLOW), Tex("2^1\\times 17", color=YELLOW),
        )
        winningstates1.arrange(RIGHT, buff=LARGE_BUFF * 2)
        winningstates2.arrange(RIGHT, buff=LARGE_BUFF * 2)
        lines = VGroup(winningstates1, winningstates2)
        lines.arrange(DOWN, buff=LARGE_BUFF * 2.5)
        lines.move_to(UP * 0.5)
        self.play(*(Write(x) for x in winningstates1))
        self.play(*(Write(x) for x in winningstates2))
        self.wait(2)
        for i in range(0, 6):
            expressions1[i].next_to(winningstates1[i], DOWN, buff=MED_LARGE_BUFF)
            self.play(TransformMatchingTex(winningstates1[i].copy(), expressions1[i]), run_time=0.25)
        for i in range(0, 6):
            expressions2[i].next_to(winningstates2[i], DOWN, buff=MED_LARGE_BUFF)
            self.play(TransformMatchingTex(winningstates2[i].copy(), expressions2[i]), run_time=0.25)
        self.play(*(FadeOut(group, UP) for group in [lines, expressions1, expressions2]))

        answer = Tex("2^{2p+1}\\cdot(2k+1)")
        self.play(Write(answer))
        self.wait(2)
        self.play(Uncreate(answer))

class S08ProofSameNumbersSituation(Scene):
    def construct(self):
        origin = Tex("(0,0,n) \\to (n,k,n-k)")
        origin.move_to(LEFT * 2)
        new1 = Tex("k < n-k")
        new2 = Tex("n = 2k")
        new1.next_to(origin, RIGHT * 1.5 + UP * 0.8, buff=LARGE_BUFF)
        new2.next_to(origin, RIGHT * 1.5 + DOWN * 0.8, buff=LARGE_BUFF)
        self.play(Write(origin))
        arrow1 = Arrow(RIGHT * 0.8, RIGHT * 2 + UP)
        arrow2 = Arrow(RIGHT * 0.8, RIGHT * 2 + DOWN)
        self.play(Write(new1), GrowArrow(arrow1))
        self.play(Write(new2), GrowArrow(arrow2))
        self.wait()
        self.play(*(FadeOut(x) for x in [origin, new1, arrow1, new2, arrow2]))
        l = Tex("(0,0,n)\\to(0,\\dfrac 12n,\\dfrac 12n)")
        r = Tex("\\Leftrightarrow(0,0,\\dfrac 12n)")
        group = VGroup(l, r)
        group.arrange(RIGHT, buff=SMALL_BUFF)
        self.play(Write(l))
        self.wait()
        self.play(Write(r))
        self.wait()
        d = Tex("\\left(0,0,2^{2p}\\cdot(2k+1)\\right)\\to\\left(0,0,2^p\\cdot(2k+1)\\right)", color=YELLOW)
        d.next_to(group, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(d))
        self.wait()

class S09ProofDifferentNumbersSituation(Scene):
    def construct(self):
        state1 = Tex("(0,x,y)")
        state2 = Tex("(x,x,y-x)")
        state3 = Tex("(x,x+k,y-x-k)")
        group = VGroup(state1, Tex("\\to"), state2, Tex("\\to"), state3)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.move_to(UP * 0.7)
        state1_note = TexText("defeat state", color=RED, font_size=40)
        state1_note.next_to(state1, DOWN, buff=MED_SMALL_BUFF)
        state1_note2 = TexText("winning state", color=GREEN, font_size=40)
        state1_note2.next_to(state1_note, DOWN, buff=MED_SMALL_BUFF)
        state1_range = Tex("0 < x < y, x < y-x", font_size=36)
        state1_range.next_to(state1, UP, buff=MED_SMALL_BUFF)
        state2_note = TexText("winning state", color=GREEN, font_size=40)
        state2_note.next_to(state2, DOWN, buff=MED_SMALL_BUFF)
        state3_note = TexText("defeat state", color=RED, font_size=40)
        state3_note.next_to(state3, DOWN, buff=MED_SMALL_BUFF)
        self.play(Write(state1))
        self.wait(2)
        self.play(Write(state1_note))
        self.play(Write(state1_range))
        self.wait(2)
        self.play(Write(state2), FadeIn(group[1], RIGHT))
        self.play(Write(state2_note))
        self.wait(2)
        self.play(Write(state3), FadeIn(group[3], RIGHT))
        self.play(Write(state3_note))
        self.wait(2)
        self.play(GrowArrow(Arrow(state1_note, state3_note, path_arc=1)))
        self.wait()
        self.play(ShowCreation(Cross(state1_note)))
        self.play(Write(state1_note2))
        self.wait(2)

class S10ShowConclusions(Scene):
    def construct(self):
        title = TexText("The 7th Romanian Master of Mathematics Competition Problem 2", font_size=42)
        title.move_to(UP * 3.5)
        image = ImageMobject('./S10-origin-problem.png')
        image.move_to(UP * 0.9)
        self.play(FadeIn(image, UP), Write(title))
        columns = VGroup(
            Tex("(0,0,n-3)"),
            Tex("n-3=2^{2p+1}\\cdot(2k+1)"),
            TexText("otherwise"),
        )
        columns.arrange(RIGHT, buff=LARGE_BUFF)
        columns.move_to(DOWN * 2)
        note1 = TexText("winning state", color=GREEN, font_size=40)
        note2 = TexText("defeat state", color=RED, font_size=40)
        note1.next_to(columns[1], DOWN, buff=MED_SMALL_BUFF)
        note2.next_to(columns[2], DOWN, buff=MED_SMALL_BUFF)
        self.wait()
        self.play(Write(columns[0]))
        self.wait()
        self.play(Write(columns[1]), Write(note1))
        self.play(Write(columns[2]), Write(note2))
        self.wait()

class S11ShowGymProblem(Scene):
    def construct(self):
        title = TexText("The 2023 ICPC Asia EC Regionals Online Contest (I) Problem F", font_size=36)
        title.move_to(UP * 3.5)
        image = ImageMobject("./S11-gym-problem.png")
        image.scale(1.35)
        image.move_to(UP * 0.5)
        self.play(FadeIn(image, UP), Write(title))
        arr = VGroup(
            Tex("a_1"), Tex("a_2"), Tex("a_3"), Tex("a_4"),
            Tex("a_5"), Tex("a_6"), Tex("a_7"), Tex("\cdots"),
        )
        arr.arrange(RIGHT, buff=MED_LARGE_BUFF)
        arr.move_to(DOWN * 2.8)
        self.wait()
        self.play(*(Write(tex) for tex in arr))
        self.wait(2)
        self.play(ShowCreation(SurroundingRectangle(arr[1])), run_time=1/3)
        self.play(ShowCreation(SurroundingRectangle(arr[3])), run_time=1/3)
        self.play(ShowCreation(SurroundingRectangle(arr[6])), run_time=1/3)
        self.wait()
        note = TexText("calculate total of winning states", color=BLUE, font_size=40)
        note.next_to(arr, DOWN, buff=MED_SMALL_BUFF)
        self.play(Write(note))
        self.wait()

class S12InclusionExclusion(Scene):
    def construct(self):
        title = TexText("Inclusion-Exclusion Principle")
        type1 = TexText("$S=$ total number of situations", font_size=40)
        type2 = TexText("$S_1=$ total number of all 3 numbers are the same", font_size=40)
        type3 = TexText("""
            $S_2=$ total number of only 2 numbers are the same\\\\
            and must be defeated
        """, font_size=40)
        difficulty1 = TexText("SUPER simple!", color=GREEN)
        difficulty2 = TexText("VERY simple!", color=YELLOW)
        difficulty3 = TexText("a little difficult ...", color=RED)
        lines = VGroup(title, type1, type2, type3, difficulty3)
        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        lines.move_to(LEFT * 1.5 + UP * 0.4)
        answer1 = Tex("=\\dbinom n3")
        answer1.next_to(type1, RIGHT, buff=MED_SMALL_BUFF)
        difficulty1.next_to(answer1, RIGHT, buff=MED_LARGE_BUFF)
        difficulty2.next_to(type2, RIGHT, buff=MED_LARGE_BUFF)
        difficulty3.next_to(type3, RIGHT + DOWN, buff=-MED_SMALL_BUFF)
        self.play(Write(title))
        self.wait()
        for target in [type1, answer1, difficulty1, type2, difficulty2, type3, difficulty3]:
            self.play(Write(target))
            self.wait()
        answer = TexText("answer $=S-S_1-S_2$", color=PURPLE_B)
        answer.move_to(DOWN * 2.2)
        self.wait()
        self.play(Write(answer))
        self.wait()
