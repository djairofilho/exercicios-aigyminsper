from __future__ import annotations

import argparse

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import (
    AEstrela,
    BuscaGananciosa,
    BuscaLargura,
    BuscaProfundidade,
)


class OitoRainhas(State):
    def __init__(self, op: str, cols: tuple[int, ...], size: int = 8) -> None:
        super().__init__(op)
        self.cols = cols
        self.size = size

    def successors(self) -> list[OitoRainhas]:
        successors: list[OitoRainhas] = []
        next_row = len(self.cols)

        if next_row >= self.size:
            return successors

        for col in range(self.size):
            if self._is_safe(next_row, col):
                successors.append(
                    OitoRainhas(
                        op=f"linha {next_row} -> coluna {col}",
                        cols=self.cols + (col,),
                        size=self.size,
                    )
                )

        return successors

    def is_goal(self) -> bool:
        return len(self.cols) == self.size

    def description(self) -> str:
        return "Problema das N rainhas sem conflitos por coluna e diagonal"

    def cost(self) -> int:
        return 1

    def h(self) -> int:
        # Heuristica simples: quantas rainhas faltam posicionar.
        return self.size - len(self.cols)

    def env(self) -> str:
        return f"N{self.size}#{self.cols}"

    def _is_safe(self, row: int, col: int) -> bool:
        for r, c in enumerate(self.cols):
            if c == col:
                return False
            if abs(row - r) == abs(col - c):
                return False
        return True


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


def render_board(cols: tuple[int, ...], size: int) -> str:
    board_lines: list[str] = []
    for row in range(size):
        line = []
        for col in range(size):
            if row < len(cols) and cols[row] == col:
                line.append("Q")
            else:
                line.append(".")
        board_lines.append(" ".join(line))
    return "\n".join(board_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Problema das N rainhas com aigyminsper")
    parser.add_argument("--size", type=int, default=8, help="Tamanho do tabuleiro NxN")
    parser.add_argument(
        "--algoritmo",
        choices=["largura", "profundidade", "gulosa", "a_estrela"],
        default="profundidade",
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

    if args.size < 1:
        raise ValueError("--size deve ser >= 1")

    state = OitoRainhas("", tuple(), size=args.size)
    algorithm, needs_depth = build_algorithm(args.algoritmo)

    if needs_depth:
        depth_limit = args.depth_limit if args.depth_limit is not None else args.size
        result = algorithm.search(state, m=depth_limit, pruning=args.pruning)
    else:
        result = algorithm.search(state, pruning=args.pruning)

    if result is not None:
        print("Achou!")
        print(result.show_path())
        print(f"Custo total: {result.g}")
        print("\nTabuleiro:")
        print(render_board(result.state.cols, args.size))
    else:
        print("Nao achou solucao")


if __name__ == "__main__":
    main()
