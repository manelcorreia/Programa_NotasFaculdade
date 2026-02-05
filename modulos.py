class Disciplina:
    def __init__(self, nome, ano, semestre, eA=0.0, eB=0.0, eGlobal=0.0, exame=0.0):
        self.nome = nome
        self.ano = ano
        self.semestre = semestre
        self.eA = eA
        self.eB = eB
        self.eGlobal = eGlobal
        self.exame = exame
        self.nota_final = self.calcular_nota_final()
        self.aprovacao = self.verificar_aprovacao()

    def calcular_nota_final(self):
        # efolio A + B tem de ser >= 3.5 para ir a efolio Global
        soma_efolios = self.eA + self.eB

        if soma_efolios >= 3.5:
            return soma_efolios + self.eGlobal
        else:
            return self.exame

    def verificar_aprovacao(self):
        soma_efolios = self.eA + self.eB

        # 1º regra
        if soma_efolios >= 3.5:
            if self.eGlobal >= 5.5:
                return "Aprovado"
            return "Reprovado"

        # 2º regra
        else:
            if self.exame >= 9.5:
                return "Aprovado"
            return "Reprovado"

    def __str__(self):
        return f"{self.nome} | Nota Final: {self.nota_final:.2f}"
