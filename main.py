import customtkinter as ctk
from tkinter import messagebox
from Programa_NotasFaculdade.DatabaseManagement import DatabaseManager
from Programa_NotasFaculdade.modulos import Disciplina


class AppNotas(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.bind("<Return>", lambda event: self.submeter_nota())

        # configuração da janela principal
        self.title("Gestor Académico")
        self.geometry("600x700")
        ctk.set_appearance_mode("dark")

        # criação do menu de abas (Interface Inicial)
        self.tabview = ctk.CTkTabview(self, width=550, height=650)
        self.tabview.pack(padx=20, pady=20)

        # criar duas abas
        self.tab_add = self.tabview.add("Adicionar Notas")
        self.tab_hist = self.tabview.add("Ver Histórico Académico")

        # configurar a aba de adicionar (chama a função que desenha o "formulário")
        self.configurar_aba_adicionar()
        self.configurar_aba_historico()

    def configurar_aba_adicionar(self):
        # titulo
        ctk.CTkLabel(self.tab_add, text="Novas Notas", font=("Arial", 20, "bold")).pack(pady=10)

        # obter o catalogo da base de dados
        self.catalogo_completo = self.db_manager.obter_catalogo()
        # extrair só os nomes para mostrar na lista
        nomes_cadeiras = [d["nome"] for d in self.catalogo_completo]

        # novo dropdown
        ctk.CTkLabel(self.tab_add, text="Selecione a cadeira:").pack(pady=(10, 0))
        self.combo_disciplina = ctk.CTkOptionMenu(self.tab_add, values=nomes_cadeiras, width=300)
        self.combo_disciplina.pack(pady=5)

        # notas (efolioA e B)
        frame_efolios = ctk.CTkFrame(self.tab_add, fg_color="transparent")
        frame_efolios.pack(pady=10)

        self.entry_ea = ctk.CTkEntry(frame_efolios, placeholder_text="Nota efolio A", width=140)
        self.entry_ea.pack(side="left", padx=5)      # exemplo de posicionamento manual

        self.entry_eb = ctk.CTkEntry(frame_efolios, placeholder_text="Nota efolio B", width=140)
        self.entry_eb.pack(side="left", padx=5)

        # botão para verificar se vai a exame ou efolio global
        self.btn_verificar = ctk.CTkButton(self.tab_add, text="Verificar se vai a efolio Global ou exame", command=self.verificar_fase, fg_color="#E59400")
        self.btn_verificar.pack(pady=20)

        # campos dinâmicos (começam escondidos)
        self.label_status = ctk.CTkLabel(self.tab_add, text="", font=("Arial", 20, "bold"), text_color="yellow")
        self.label_status.pack(pady=5)

        self.entry_eg = ctk.CTkEntry(self.tab_add, placeholder_text="Nota efolio Global (0-4)", width=300)
        self.entry_exame = ctk.CTkEntry(self.tab_add, placeholder_text="Nota Exame (0-20)", width=300)

        # botão guardar (também começa escondido)
        self.btn_guardar = ctk.CTkButton(self.tab_add, text="Guardar na base de dados", command=self.submeter_nota, fg_color="green", state="disabled")
        self.btn_guardar.pack(pady=20)

    def configurar_aba_historico(self):
        # botão para atualizar (carregar dados novos)
        self.btn_atualizar = ctk.CTkButton(self.tab_hist, text="Atualizar", command=self.atualizar_lista)
        self.btn_atualizar.pack(pady=10)

        # --- NOVO: PAINEL DE PROGRESSO ---
        self.frame_progresso = ctk.CTkFrame(self.tab_hist)
        self.frame_progresso.pack(fill="x", padx=10, pady=10)

        self.label_progresso = ctk.CTkLabel(self.frame_progresso, text="Progresso da Licenciatura: 0% (0 / 180 ECTS)",
                                            font=("Arial", 14, "bold"))
        self.label_progresso.pack(pady=5)

        self.barra_progresso = ctk.CTkProgressBar(self.frame_progresso, width=400, progress_color="#4CAF50")
        self.barra_progresso.pack(pady=10)
        self.barra_progresso.set(0)  # Começa a zero

        # cabeçalho da tabela (fixo)
        frame_header = ctk.CTkFrame(self.tab_hist, height=30, fg_color="gray30")
        frame_header.pack(fill="x", padx=10)

        # labels do cabeçalho (define colunas fixas visualmente)
        ctk.CTkLabel(frame_header, text="DISCIPLINA", width=200, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(frame_header, text="NOTA", width=50, font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(frame_header, text="ESTADO", width=100, font=("Arial", 12, "bold")).pack(side="left", padx=5)

        # área de scroll onde as notas vão aparecer
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_hist, width=500, height=500)
        self.scroll_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # carregar a lista automaticamente ao abrir
        self.atualizar_lista()

    def atualizar_lista(self):
        # limpar a lista antiga (destruir widgets dentro do scroll_frame)
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # buscar dados à base de dados
        notas = self.db_manager.buscar_todas_notas()

        # variáveis para a barra de progresso
        total_ects_curso = 180
        ects_feitos = 0

        # criar uma linha para cada disciplina
        for i, n in enumerate(notas):
            # criei uma frame para cada linha como se fosse uma linha de tabela
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            # nome da disciplina
            ctk.CTkLabel(row_frame, text=n.nome, width=200, anchor="w").pack(side="left", padx=5)

            # nota final
            ctk.CTkLabel(row_frame, text=f"{n.nota_final:.2f}", width=50).pack(side="left", padx=5)

            # estado (com cor dinâmica para aprovado ou reprovado)
            cor_texto = "#4CAF50" if n.aprovacao == "Aprovado" else "#FF5555"

            ctk.CTkLabel(row_frame, text=n.aprovacao, width=100, text_color=cor_texto, font=("Arial", 12, "bold")).pack(side="left", padx=5)

            if n.aprovacao == "Aprovado":
                ects_feitos += n.creditos

        # atualizar barra de progresso visualmente
        if notas:
            percentagem = ects_feitos / total_ects_curso

            # garantir que a barra não passa dos 100% (1.0)
            if percentagem > 1.0:
                percentagem = 1.0

            self.barra_progresso.set(percentagem)

            texto_progresso = f"Progresso de licenciatura: {percentagem*100:.1f}% ({ects_feitos} / {total_ects_curso} ECTS)"
            self.label_progresso.configure(text=texto_progresso)
        else:
            # se não houver notas na base de dados
            self.barra_progresso.set(0)
            self.label_progresso.configure(text=f"Progresso da Licenciatura: 0.0%  (0 / {total_ects_curso} ECTS)")

    def verificar_fase(self):
        """Lógica que decide se o programa mostra o campo Exame ou efolio Global"""
        try:
            ea = float(self.entry_ea.get())
            eb = float(self.entry_eb.get())
            soma = ea + eb

            # limpar campos anteriores para evitar confusão
            self.entry_eg.pack_forget()
            self.entry_exame.pack_forget()

            if soma >= 3.5:
                # cenário em que vai a efolio Global
                self.label_status.configure(text=f"Soma: {soma:.2f} -> Admitido a efolio Global!", text_color="#4CAF50") # verde
                self.entry_eg.pack(pady=10)   # aparece o campo efolio global
                self.modo_atual = "efolio global"
            else:
                # cenário em que vai a exame
                self.label_status.configure(text=f"Soma: {soma:.2f} -> Reprovado na avaliação contínua. Vai a exame.", text_color="#FF5555")  # vermelho
                self.entry_exame.pack(pady=10)    # aparece o campo exame
                self.modo_atual = "exame"

            # agora é que o botão guardar aparece
            self.btn_guardar.configure(state="normal")

        except ValueError:
            messagebox.showerror("Erro", "Por favor preencha os efolios com números (ponto para decimais em vez de vírgula).")

    def submeter_nota(self):
        # 1. recolher dados da interface
        try:
            # 1. Qual foi a cadeira escolhida no Dropdown?
            nome_selecionado = self.combo_disciplina.get()

            # 2. Procurar os dados dessa cadeira no nosso catálogo
            dados_cadeira = next(d for d in self.catalogo_completo if d["nome"] == nome_selecionado)

            # Extrair a info fixa automaticamente!
            ano = dados_cadeira["ano"]
            semestre = dados_cadeira["semestre"]
            creditos = dados_cadeira["creditos"]

            # 3. Ler as notas que o utilizador escreveu
            ea = float(self.entry_ea.get())
            eb = float(self.entry_eb.get())

            eg, ex = 0.0, 0.0
            if self.modo_atual == "efolio global":
                eg = float(self.entry_eg.get())
            else:
                ex = float(self.entry_exame.get())

            # 4. Criar o objeto e Guardar
            nova_disciplina = Disciplina(nome_selecionado, ano, semestre, creditos, ea, eb, eg, ex)
            self.db_manager.guardar_nota(nova_disciplina)

            messagebox.showinfo("Sucesso",
                                f"{nome_selecionado} guardada com sucesso!\nResultado: {nova_disciplina.aprovacao}")
            self.limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Introduza valores numéricos válidos!")
        except StopIteration:
            messagebox.showerror("Erro", "Disciplina não encontrada no catálogo.")

    def limpar_campos(self):
        self.entry_ea.delete(0, "end")
        self.entry_eb.delete(0, "end")
        self.entry_eg.delete(0, "end")
        self.entry_exame.delete(0, "end")
        self.entry_eg.pack_forget()
        self.entry_exame.pack_forget()
        self.label_status.configure(text="")
        self.btn_guardar.configure(state="disabled")

# Nova classe de login
class LoginApp(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.title("Login/Registo - Gestor Notas Faculdade")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self, text="Bem-Vindo", font=("Arial", 24, "bold")).pack(pady=40)

        self.entry_user = ctk.CTkEntry(self , placeholder_text="Username", width=250)
        self.entry_user.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self , placeholder_text="Password", show="*", width=250)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Entrar", command=self.fazer_login, width=250)
        self.btn_login.pack(pady=20)

        ctk.CTkLabel(self, text="Ainda não tens conta?").pack(pady=5)
        self.btn_registo = ctk.CTkButton(self, text="Criar nova conta", command=self.fazer_registo, fg_color="transparent", border_width=1, width=250)
        self.btn_registo.pack(pady=5)

    def fazer_login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()

        if self.db_manager.validar_login(user, password):
            messagebox.showinfo("Sucesso", f"Login com sucesso! Bem_vindo, {user}!")
            self.abrir_app_principal()
        else:
            messagebox.showerror("Erro", "Utilizador ou Password incorretos.")

    def fazer_registo(self):
        user = self.entry_user.get()
        password = self.entry_password.get()

        if user and password:
            sucesso, mensagem = self.db_manager.registar_utilizador(user, password)
            if sucesso:
                messagebox.showinfo("Registo com sucesso", f"Conta criada! Tabela 'notas_{user}' configurada.")
            else:
                messagebox.showerror("Erro", mensagem)
        else:
            messagebox.showwarning("Atenção", "Preencha o nome e a password.")

    def abrir_app_principal(self):
        # "destruir" a janela de login
        self.destroy()

        # iniciar a janela principal
        app_principal = AppNotas(self.db_manager)
        app_principal.mainloop()

if __name__ == "__main__":
    # inicializar base de dados
    meu_db_manager = DatabaseManager()

    # iniciar app
    app_login = LoginApp(meu_db_manager)
    app_login.mainloop()