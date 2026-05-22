from manim import *

# ==========================================================
# PARTE 1: Introdução e Órbita
# ==========================================================
class Scene1(Scene):
    def construct(self):
        title = Tex("Momento Angular e Magnetismo").scale(1.1).to_edge(UP)
        self.play(Write(title))
        self.wait(5) 
        
        centro_ponto = Dot(color=YELLOW, radius=0.15).move_to(ORIGIN + DOWN*0.5)
        orbita = Ellipse(width=6.0, height=2.0, color=WHITE, stroke_opacity=0.5).move_to(centro_ponto)
        
        carga = Dot(color=BLUE, radius=0.15)
        carga.move_to(orbita.point_from_proportion(0))
        label_carga = always_redraw(lambda: MathTex(r"q").next_to(carga, UR, buff=0.1))
        
        self.play(FadeIn(centro_ponto), Create(orbita), FadeIn(carga), FadeIn(label_carga))
        
        vec_L = Arrow(centro_ponto.get_center(), centro_ponto.get_center() + UP*2.5, buff=0, color=GREEN)
        # Deslocamento aplicado para subir o texto levemente
        label_L = MathTex(r"\vec{L}").next_to(vec_L, RIGHT).shift(UP * 0.4).set_color(GREEN)
        
        self.play(GrowArrow(vec_L), Write(label_L))
        self.play(MoveAlongPath(carga, orbita), run_time=10, rate_func=linear) 
        
        vec_mu = Arrow(centro_ponto.get_center(), centro_ponto.get_center() + DOWN*1.5, buff=0, color=RED)
        label_mu = MathTex(r"\vec{\mu}").next_to(vec_mu, RIGHT, buff=0.1).set_color(RED)
        
        # Suavização da entrada do vetor com GrowArrow e controle de tempo
        self.play(GrowArrow(vec_mu), FadeIn(label_mu), run_time=2, rate_func=smooth)
        self.play(MoveAlongPath(carga, orbita), run_time=10, rate_func=linear) 
        self.wait(5)
        
        self.play(FadeOut(centro_ponto, orbita, carga, label_carga, vec_L, label_L, vec_mu, label_mu))

        eq = MathTex(r"\vec{\mu}", r"=", r"\gamma", r"\vec{L}").scale(2)
        eq[0].set_color(RED)
        eq[2].set_color(YELLOW)
        eq[3].set_color(GREEN)
        
        # Ajuste de posicionamento dos rótulos para evitar sobreposição (deslocando para as laterais)
        t_mag = Tex("Momento Magnético").scale(0.6).set_color(RED).next_to(eq[0], UP, buff=0.6).shift(LEFT * 0.7)
        t_ang = Tex("Momento Angular").scale(0.6).set_color(GREEN).next_to(eq[3], UP, buff=0.6).shift(RIGHT * 0.7)
        
        # Alinha t_mag e t_ang verticalmente para garantir simetria
        t_mag.match_y(t_ang)
        
        # Centraliza a legenda do gamma abaixo de toda a equação para melhor distribuição
        t_gam = Tex(r"Razão Giromagnética ($\gamma < 0$)").scale(0.6).set_color(YELLOW).next_to(eq, DOWN, buff=0.6)
        
        # Caixa atualizada para englobar as equações e todos os textos de forma harmoniosa
        eq_box = SurroundingRectangle(VGroup(eq, t_mag, t_ang, t_gam), buff=0.4, color=BLUE)
        
        self.play(Write(eq))
        self.play(Write(t_mag), Write(t_ang), Write(t_gam))
        self.play(Create(eq_box))
        self.wait(15)
        self.play(FadeOut(eq, t_mag, t_ang, t_gam, eq_box, title))

# ==========================================================
# PARTE 2: O Experimento
# ==========================================================
class Scene2(Scene):
    def construct(self):
        sg_title = Tex("O Experimento de Stern-Gerlach").to_edge(UP)
        self.play(Write(sg_title))
        
        forno = Rectangle(width=2.4, height=1.0, color=GRAY).shift(LEFT*5 + DOWN*1)
        forno_txt = Tex("Forno (Ag)").scale(0.7).move_to(forno)
        tela = Line(UP*2.5, DOWN*2.5, color=WHITE).shift(RIGHT*5 + DOWN*1)
        
        im_n = Polygon([-0.8,0.8,0],[0.8,0.8,0],[0,-0.4,0], color=RED, fill_opacity=0.2).shift(UP*0.5 + LEFT*1)
        im_s = Rectangle(width=1.6, height=0.6, color=BLUE, fill_opacity=0.2).shift(DOWN*2.5 + LEFT*1)
        
        grupo_exp = VGroup(forno, forno_txt, tela, im_n, im_s)
        self.play(FadeIn(grupo_exp))
        self.wait(5)
        
        f_eq = MathTex(r"\vec{F} = \nabla(\vec{\mu} \cdot \vec{B})").scale(1.1).to_edge(UP, buff=1.2).set_color(ORANGE)
        f_desc = Tex("Variação do campo no espaço").scale(0.6).next_to(f_eq, DOWN).set_color(ORANGE)
        
        self.play(Write(f_eq), FadeIn(f_desc))
        self.wait(8)
        
        # Posicionamento corrigido para alinhar organicamente ao topo da tela de projeção
        exp_txt = Tex("Expectativa Clássica").scale(0.8).next_to(tela, LEFT, buff=0.5).shift(LEFT)
        
        linhas_c = VGroup(*[Line(forno.get_right(), tela.get_center() + UP*(i/12), stroke_width=1, color=YELLOW).set_opacity(0.1) for i in range(-20,21)])
        mancha = Rectangle(width=0.2, height=3.5, color=YELLOW, fill_opacity=0.5).move_to(tela.get_center())
        
        self.play(Write(exp_txt))
        self.play(Create(linhas_c), FadeIn(mancha), run_time=5)
        self.wait(10)
        self.play(FadeOut(grupo_exp, f_eq, f_desc, exp_txt, linhas_c, mancha, sg_title))

# ==========================================================
# PARTE 3: Natureza Quântica
# ==========================================================
class Scene3(Scene):
    def construct(self):
        q_title = Tex("A Natureza Quântica").to_edge(UP)
        self.play(Write(q_title))
        
        rampa = Line(LEFT*3+DOWN*1.5, RIGHT*3+UP*1.5, color=GRAY).shift(DOWN*0.5)
        escada = VGroup(*[Line(LEFT*(3-i*1.2)+DOWN*(1.5-i*0.6), LEFT*(1.8-i*1.2)+DOWN*(1.5-i*0.6), color=BLUE).shift(DOWN*0.5) for i in range(6)])
        for i in range(5):
            dv = Line(LEFT*(1.8-i*1.2)+DOWN*(1.5-i*0.6), LEFT*(1.8-i*1.2)+DOWN*(0.9-i*0.6), color=BLUE).shift(DOWN*0.5)
            escada.add(dv)
        
        self.play(Create(rampa))
        self.wait(5)
        self.play(Transform(rampa, escada), run_time=3)
        self.wait(8)
        self.play(FadeOut(rampa))
        
        forno_q = Rectangle(width=1.5, height=0.8).shift(LEFT*5.5 + DOWN*1)
        tela_q = Line(UP*3, DOWN*3).shift(RIGHT*5.5 + DOWN*1)
        
        info_q = VGroup(
            Tex("Projeções: $2L+1$").set_color(BLUE),
            Tex("Sempre Ímpar").set_color(YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=0.8).shift(UP*1)
        
        self.play(FadeIn(forno_q, tela_q), Write(info_q))
        
        p_u = Dot(tela_q.get_center() + UP*2, color=YELLOW)
        p_c = Dot(tela_q.get_center(), color=YELLOW)
        p_d = Dot(tela_q.get_center() + DOWN*2, color=YELLOW)
        l_u = Line(forno_q.get_right(), p_u.get_center(), color=YELLOW, stroke_width=2)
        l_c = Line(forno_q.get_right(), p_c.get_center(), color=YELLOW, stroke_width=2)
        l_d = Line(forno_q.get_right(), p_d.get_center(), color=YELLOW, stroke_width=2)
        
        label_nulo = Tex("Estado sem desvios").scale(0.8).next_to(p_c, LEFT, buff=1.2).shift(UP*0.3).set_color(GREEN)
        
        self.play(Create(l_u), Create(l_c), Create(l_d), FadeIn(p_u, p_c, p_d))
        self.play(Write(label_nulo))
        self.wait(12)
        
        res_txt = Tex("Resultado Real: PAR (2 pontos)").to_edge(UP, buff=1.2).set_color(RED)
        cruz = Cross(p_c, stroke_width=8)
        self.play(Write(res_txt), Create(cruz))
        self.wait(3)
        self.play(FadeOut(l_c, p_c, label_nulo, cruz, forno_q, tela_q, info_q, l_u, l_d, p_u, p_d, res_txt, q_title))


class Scene4(Scene):
    def construct(self):
        # ==========================================================
        # PRIMEIRA PARTE: Equações Centralizadas (Sem Título)
        # ==========================================================
        # Posicionado em UP*1.0 para que, junto com o resultado abaixo, o bloco fique perfeitamente centralizado
        eq_spin = MathTex(r"2", r"L", r"+ 1 = 2").scale(1.8).move_to(UP * 1.8)
        eq_spin[1].set_color(BLUE)
        self.play(Write(eq_spin))
        self.wait(5)
        
        eq_resultado = MathTex(r"L", r"=", r"\frac{1}{2}").scale(2.5).next_to(eq_spin, DOWN, buff=0.8)
        eq_resultado[0].set_color(BLUE)
        eq_resultado[2].set_color(YELLOW)
        
        self.play(TransformFromCopy(eq_spin, eq_resultado), run_time=3)
        self.wait(5)
        
        box_spin = SurroundingRectangle(eq_resultado, color=GREEN, buff=0.4)
        txt_spin = Tex("SPIN").scale(1.5).next_to(box_spin, RIGHT, buff=0.6).set_color(GREEN)
        
        self.play(Create(box_spin), Write(txt_spin))
        self.wait(10)
        self.play(FadeOut(eq_spin, eq_resultado, box_spin, txt_spin))
        
        # ==========================================================
        # SEGUNDA PARTE: Título, Eixos e Vetores (Sem a Esfera)
        # ==========================================================
        spin_title = Tex("O Spin").scale(1.5).to_edge(UP)
        
        centro_esfera = DOWN * 0.2
        
        e_z = Line(DOWN * 2.2, UP * 2.2, color=GRAY, stroke_opacity=0.5).move_to(centro_esfera)
        e_x = Line(LEFT * 2.2, RIGHT * 2.2, color=GRAY, stroke_opacity=0.5).move_to(centro_esfera)
        
        v_u = Arrow(centro_esfera, centro_esfera + UP * 1.6, color=YELLOW, buff=0)
        v_d = Arrow(centro_esfera, centro_esfera + DOWN * 1.6, color=RED, buff=0)
        l_u = MathTex(r"|+\rangle").next_to(v_u, UR, buff=0.1)
        l_d = MathTex(r"|-\rangle").next_to(v_d, DR, buff=0.1)
        
        self.play(
            Write(spin_title), 
            FadeIn(e_z, e_x), 
            Create(v_u), 
            Create(v_d), 
            Write(l_u), 
            Write(l_d)
        )
        self.wait(10)
        
        final_msg = Tex("Uma propriedade intrínseca da natureza.").to_edge(DOWN, buff=0.5)
        self.play(Write(final_msg))
        self.wait(15)
        self.play(FadeOut(e_z, e_x, v_u, v_d, l_u, l_d, final_msg, spin_title))