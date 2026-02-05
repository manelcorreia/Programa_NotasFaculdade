import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.tabela_atual = None     # vai ser definido após login
        self._criar_tabela_users()   # garante que a tabela de logins existe

    def _obter_conexao(self):
        return mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

    def _criar_tabela_users(self):
        """cria a tabela que gere os logins"""
        conn = self._obter_conexao()
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50)
        )
        """
        cursor.execute(query)
        conn.close()

    def registar_utilizador(self, username, password):
        """Cria o login e a tabela pessoal do utilizador"""
        conn = self._obter_conexao()
        cursor = conn.cursor()
        try:
            # inserir na tabela de users
            cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))

            # criar a tabela pessoal (ex: notas_manuel)
            # nota: removi espaços para evitar erros no SQL
            nome_tabela = f"notas_{username.replace(' ', '')}"

            query_tabela = f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                disciplina VARCHAR(100),
                ano INT,
                semestre VARCHAR(20),
                efolioA DECIMAL(4,2),
                efolioB DECIMAL(4,2),
                efolioGlobal DECIMAL(4,2),
                exame DECIMAL(4,2),
                nota_final DECIMAL(4,2),
                aprovado_reprovado VARCHAR(20)
            )
            """
            cursor.execute(query_tabela)
            conn.commit()
            return True, "Utilizador registado com sucesso!"
        except mysql.connector.Error as err:
            return False, f"Erro: {err}"
        finally:
            cursor.close()

    def validar_login(self, username, password):
        """verifica se o user existe e define a tabela atual"""
        conn = self._obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s and password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # se der para fazer login, define-se qual é a tabela que vai se usar daqui para a frente
            self.tabela_atual = f"notas_{username.replace(' ', '')}"
            return True
        return False

    def guardar_nota(self, nota_obj):
        if not self.tabela_atual:
            return           # por segurança

        conn = self._obter_conexao()
        cursor = conn.cursor()
        query = f"""INSERT INTO {self.tabela_atual} 
                    (disciplina, ano, semestre, efolioA, efolioB, efolioGlobal, exame, nota_final, aprovado_reprovado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (nota_obj.nome, nota_obj.ano, nota_obj.semestre, nota_obj.eA, nota_obj.eB, nota_obj.eGlobal, nota_obj.exame, nota_obj.nota_final, nota_obj.aprovacao))
        conn.commit()
        conn.close()

    def buscar_todas_notas(self):
        if not self.tabela_atual:
            return []

        conn = self._obter_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM {self.tabela_atual}")
        rows = cursor.fetchall()
        conn.close()

        # importei a class disciplina aqui dentro
        from Programa_NotasFaculdade.modulos import Disciplina
        return [Disciplina(r['disciplina'], r['ano'], r['semestre'], r['efolioA'], r['efolioB'], r['efolioGlobal'], r['exame']) for r in rows]