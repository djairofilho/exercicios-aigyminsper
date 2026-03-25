from aigyminsper.search.search_algorithms import BuscaLargura, BuscaProfundidade
from aigyminsper.search.graph import State


class AspiradorPo(State):
    def __init__(self, op, posicao_robo, condicao_esq="sujo", condicao_dir="sujo"):
        # voce sempre deve usar esta chamada para inicializar a superclasse
        super().__init__(op)
        # posicao robo = esq ou dir
        self.posicao_robo = posicao_robo

        # condicao esq e dir = sujo ou limpo
        self.condicao_esq = condicao_esq
        self.condicao_dir = condicao_dir

    def successors(self):
        successors = []

        # esq
        successors.append(
            AspiradorPo("ir p esq", "esq", self.condicao_esq, self.condicao_dir)
        )

        # dir
        successors.append(
            AspiradorPo("ir p dir", "dir", self.condicao_esq, self.condicao_dir)
        )

        # limpar
        if self.posicao_robo == "esq" and self.condicao_esq == "sujo":
            successors.append(
                AspiradorPo("limpar esq", "esq", "limpo", self.condicao_dir)
            )
        elif self.posicao_robo == "dir" and self.condicao_dir == "sujo":
            successors.append(
                AspiradorPo("limpar dir", "dir", self.condicao_esq, "limpo")
            )

        return successors

    def is_goal(self):
        return self.condicao_esq == "limpo" and self.condicao_dir == "limpo"

    def description(self):
        return "Aspirador de Po 2 quartos"

    def cost(self):
        return 1

    def env(self):
        # Representacao completa do estado para poda correta.
        return f"{self.posicao_robo}#{self.condicao_esq}#{self.condicao_dir}"


def main():
    # print("Busca em largura")
    state = AspiradorPo("", "esq", "sujo", "sujo")
    # algorithm = BuscaLargura()
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, m=10)
    if result is not None:
        print("Achou!")
        print(result.show_path())
    else:
        print("Nao achou solucao")


if __name__ == "__main__":
    main()
