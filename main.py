import csv
from datetime import datetime

# =====================================
# Classe Base
# =====================================
class Imovel:
    def __init__(self, tipo, valor_base, quartos):
        self.tipo = tipo
        self.valor_base = valor_base
        self.quartos = quartos

    def calcular_quartos_extras(self, valor_extra):
        if self.quartos > 1:
            return (self.quartos - 1) * valor_extra
        return 0


# =====================================
# Apartamento
# =====================================
class Apartamento(Imovel):
    def __init__(self, quartos, garagem, tem_criancas):
        super().__init__("Apartamento", 700, quartos)
        self.garagem = garagem
        self.tem_criancas = tem_criancas

    def calcular_valor(self):
        valor = self.valor_base
        valor += self.calcular_quartos_extras(200)

        if self.garagem:
            valor += 300

        if not self.tem_criancas:
            valor *= 0.95  # desconto de 5%

        return valor


# =====================================
# Casa
# =====================================
class Casa(Imovel):
    def __init__(self, quartos, garagem):
        super().__init__("Casa", 900, quartos)
        self.garagem = garagem

    def calcular_valor(self):
        valor = self.valor_base
        valor += self.calcular_quartos_extras(250)

        if self.garagem:
            valor += 300

        return valor


# =====================================
# Estúdio
# =====================================
class Estudio(Imovel):
    def __init__(self, vagas):
        super().__init__("Estúdio", 1200, 1)
        self.vagas = vagas

    def calcular_valor(self):
        valor = self.valor_base

        if self.vagas >= 2:
            valor += 250
            if self.vagas > 2:
                valor += (self.vagas - 2) * 60

        return valor


# =====================================
# Orçamento
# =====================================
class Orcamento:
    def __init__(self, imovel):
        self.imovel = imovel
        self.valor_aluguel = imovel.calcular_valor()
        self.valor_contrato = 2000
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.hora = datetime.now().strftime("%H%M%S")

    def exibir(self):
        print("\n--- ORÇAMENTO FINAL ---")
        print(f"Tipo do imóvel: {self.imovel.tipo}")
        print(f"Quartos: {self.imovel.quartos}")
        print(f"Aluguel mensal: R$ {self.valor_aluguel:.2f}")
        print(f"Contrato imobiliário: R$ {self.valor_contrato:.2f}")

        print("\nParcelamento do contrato:")
        for i in range(1, 6):
            print(f"{i}x de R$ {self.valor_contrato / i:.2f}")

    def gerar_csv(self):
        nome_arquivo = (
            f"contrato_{self.imovel.tipo.lower()}_"
            f"{self.data.replace('/', '-')}_{self.hora}.csv"
        )

        with open(nome_arquivo, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Cabeçalho
            writer.writerow(["COMPROVANTE DE ORÇAMENTO IMOBILIÁRIO"])
            writer.writerow(["Empresa", "R.M Imobiliária"])
            writer.writerow(["Data", self.data])
            writer.writerow([])

            # Dados do imóvel
            writer.writerow(["Tipo do Imóvel", self.imovel.tipo])
            writer.writerow(["Quantidade de Quartos", self.imovel.quartos])

            if hasattr(self.imovel, "garagem"):
                writer.writerow(["Garagem", "Sim" if self.imovel.garagem else "Não"])

            if hasattr(self.imovel, "tem_criancas"):
                writer.writerow(["Possui Crianças", "Sim" if self.imovel.tem_criancas else "Não"])

            if hasattr(self.imovel, "vagas"):
                writer.writerow(["Vagas de Estacionamento", self.imovel.vagas])

            writer.writerow([])
            writer.writerow(["Valor do Aluguel Mensal", f"R$ {self.valor_aluguel:.2f}"])
            writer.writerow(["Valor do Contrato", f"R$ {self.valor_contrato:.2f}"])
            writer.writerow(["Parcelamento do Contrato", "Até 5x"])
            writer.writerow([])

            # Parcelas
            writer.writerow(["PARCELAS DO ALUGUEL"])
            writer.writerow(["Mês", "Valor (R$)"])

            for mes in range(1, 13):
                writer.writerow([mes, f"{self.valor_aluguel:.2f}"])

        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")


# =====================================
# Programa Principal
# =====================================
print("=== SISTEMA DE ORÇAMENTO IMOBILIÁRIO ===")
print("1 - Apartamento")
print("2 - Casa")
print("3 - Estúdio")

opcao = int(input("Escolha o tipo de imóvel: "))

if opcao == 1:
    quartos = int(input("Quantidade de quartos: "))
    garagem = input("Possui garagem? (s/n): ").lower() == "s"
    criancas = input("Possui crianças? (s/n): ").lower() == "s"
    imovel = Apartamento(quartos, garagem, criancas)

elif opcao == 2:
    quartos = int(input("Quantidade de quartos: "))
    garagem = input("Possui garagem? (s/n): ").lower() == "s"
    imovel = Casa(quartos, garagem)

elif opcao == 3:
    vagas = int(input("Quantidade de vagas de estacionamento: "))
    imovel = Estudio(vagas)

else:
    print("Opção inválida!")
    exit()

orcamento = Orcamento(imovel)
orcamento.exibir()
orcamento.gerar_csv()
