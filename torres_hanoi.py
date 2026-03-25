from __future__ import annotations

import argparse

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import (
    AEstrela,
    BuscaGananciosa,
    BuscaLargura,
    BuscaProfundidade,
)


NOMES_PINOS: tuple[str, str, str] = ("A", "B", "C")


class TorresHanoi(State):
    def __init__(
        self,
        op: str,
        pinos: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
        pino_alvo: int = 2,
    ) -> None:
        super().__init__(op)
        self.pinos = pinos
        self.pino_alvo = pino_alvo
        self.disk_count = sum(len(pino) for pino in pinos)

    def successors(self) -> list[TorresHanoi]:
        successors: list[TorresHanoi] = []

        for src in range(3):
            if not self.pinos[src]:
                continue

            moving_disk = self.pinos[src][-1]

            for dst in range(3):
                if src == dst:
                    continue

                if self.pinos[dst] and self.pinos[dst][-1] < moving_disk:
                    continue

                novos_pinos_listas = [list(pino) for pino in self.pinos]
                novos_pinos_listas[src].pop()
                novos_pinos_listas[dst].append(moving_disk)
                novos_pinos = tuple(tuple(pino) for pino in novos_pinos_listas)

                successors.append(
                    TorresHanoi(
                        op=f"mover {moving_disk} de {NOMES_PINOS[src]} para {NOMES_PINOS[dst]}",
                        pinos=novos_pinos,
                        pino_alvo=self.pino_alvo,
                    )
                )

        return successors

    def is_goal(self) -> bool:
        return len(self.pinos[self.pino_alvo]) == self.disk_count

    def description(self) -> str:
        return "Torres de Hanoi com 3 pinos e n discos"

    def cost(self) -> int:
        return 1

    def h(self) -> int:
        # Heuristica simples: discos ainda fora do pino alvo.
        return self.disk_count - len(self.pinos[self.pino_alvo])

    def env(self) -> str:
        return f"{self.pinos[0]}|{self.pinos[1]}|{self.pinos[2]}|T{self.pino_alvo}"


def build_algorithm(name: str):
    if name == "largura":
        return BuscaLargura(), False
    if name == "profundidade":
        return BuscaProfundidade(), True
    if name == "gulosa":
        return BuscaGananciosa(), False
    if name == "a_estrela":
        return AEstrela(), False
    raise ValueError("algoritmo invalido")


def main() -> None:
    parser = argparse.ArgumentParser(description="Torres de Hanoi com aigyminsper")
    parser.add_argument("--disks", type=int, default=4, help="Numero de discos")
    parser.add_argument(
        "--algoritmo",
        choices=["largura", "profundidade", "gulosa", "a_estrela"],
        default="largura",
    )
    parser.add_argument(
        "--pruning",
        choices=["without", "father-son", "general"],
        default="general",
    )
    parser.add_argument(
        "--depth-limit",
        type=int,
        default=None,
        help="Limite de profundidade para busca em profundidade",
    )
    args = parser.parse_args()

    if args.disks < 1:
        raise ValueError("--disks deve ser >= 1")

    pinos_iniciais = (tuple(range(args.disks, 0, -1)), tuple(), tuple())
    state = TorresHanoi("", pinos_iniciais, pino_alvo=2)

    algorithm, needs_depth = build_algorithm(args.algoritmo)

    if needs_depth:
        depth_limit = (
            args.depth_limit
            if args.depth_limit is not None
            else (2 ** args.disks) - 1
        )
        result = algorithm.search(state, m=depth_limit, pruning=args.pruning)
    else:
        result = algorithm.search(state, pruning=args.pruning)

    if result is not None:
        print("Achou!")
        print(result.show_path())
        print(f"Custo total: {result.g}")
    else:
        print("Nao achou solucao")


if __name__ == "__main__":
    main()
