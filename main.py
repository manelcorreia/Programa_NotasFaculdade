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
        self.tab_add = self.tabview.add("Adicionar Disciplina")
        self.tab_hist = self.tabview.add("Ver Histórico Académico")

        # configurar a aba de adicionar (chama a função que desenha o "formulário")
        self.configurar_aba_adicionar()
        self.configurar_aba_historico()

    def configurar_aba_adicionar(self):
        # titulo
        ctk.CTkLabel(self.tab_add, text="Nova Disciplina", font=("Arial", 20, "bold")).pack(pady=10)

        # campos de entrada
        self.entry_nome = ctk.CTkEntry(self.tab_add, placeholder_text="Nome da Disciplina", width=300)
        self.entry_nome.pack(pady=5)

        self.entry_ano = ctk.CTkEntry(self.tab_add, placeholder_text="Ano Letivo (ex:1)", width=300)
        self.entry_ano.pack(pady=5)

        self.entry_semestre = ctk.CTkEntry(self.tab_add, placeholder_text="Semestre (ex: 1)", width=300)
        self.entry_semestre.pack(pady=5)

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
            nome = self.entry_nome.get()
            ano = int(self.entry_ano.get())
            semestre = int(self.entry_semestre.get())
            ea = float(self.entry_ea.get())
            eb = float(self.entry_eb.get())

            eg, ex = 0.0, 0.0

            if self.modo_atual == "efolio global":
                eg = float(self.entry_eg.get())
            else:
                ex = float(self.entry_exame.get())

            # 2. criar o objeto
            nova_disciplina = Disciplina(nome, ano, semestre, ea, eb, eg, ex)

            # 3. guardar no MySQL
            self.db_manager.guardar_nota(nova_disciplina)

            messagebox.showinfo("Sucesso", f"{nome} guardada!\nResultado: {nova_disciplina.aprovacao}")

            # limpar tudo para a próxima
            self.limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Introduza valores numéricos válidos!")

    def limpar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_ano.delete(0, "end")
        self.entry_semestre.delete(0, "end")
        self.entry_ea.delete(0, "end")
        self.entry_eb.delete(0, "end")

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