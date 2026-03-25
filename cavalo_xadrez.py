from __future__ import annotations

import argparse
import time

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import (
    AEstrela,
    BuscaCustoUniforme,
    BuscaGananciosa,
    BuscaLargura,
    BuscaProfundidade,
    BuscaProfundidadeIterativa,
)


class MyAgent(State):
    """Passeio do cavalo 8x8 no formato simples do User Guide."""

    KNIGHT_DELTAS: tuple[tuple[int, int], ...] = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )

    def __init__(
        self,
        op: str,
        row: int = 0,
        col: int = 0,
        start_row: int = 0,
        start_col: int = 0,
        visited: tuple[tuple[int, int], ...] | None = None,
        board_size: int = 8,
        returned_to_start: bool = False,
        use_warnsdorff: bool = False,
    ) -> None:
        super().__init__(op)
        self.row = row
        self.col = col
        self.start_row = start_row
        self.start_col = start_col
        self.visited = visited if visited is not None else ((row, col),)
        self.board_size = board_size
        self.returned_to_start = returned_to_start
        self.use_warnsdorff = use_warnsdorff

    def successors(self) -> list[MyAgent]:
        successors: list[MyAgent] = []

        if self.returned_to_start:
            return successors

        visited_set = set(self.visited)

        # Fase 1: visitar todas as casas sem repetir.
        if len(self.visited) < self.board_size * self.board_size:
            candidates: list[tuple[int, int]] = []
            for d_row, d_col in self.KNIGHT_DELTAS:
                new_row = self.row + d_row
                new_col = self.col + d_col
                if not (0 <= new_row < self.board_size and 0 <= new_col < self.board_size):
                    continue
                if (new_row, new_col) in visited_set:
                    continue
                candidates.append((new_row, new_col))

            # Warnsdorff: prioriza movimentos com menor numero de continuacoes.
            if self.use_warnsdorff:
                candidates.sort(
                    key=lambda pos: self._onward_degree(
                        pos[0],
                        pos[1],
                        visited_set | {pos},
                    )
                )

            for new_row, new_col in candidates:

                successors.append(
                    MyAgent(
                        op=f"({self.row},{self.col})->({new_row},{new_col})",
                        row=new_row,
                        col=new_col,
                        start_row=self.start_row,
                        start_col=self.start_col,
                        visited=self.visited + ((new_row, new_col),),
                        board_size=self.board_size,
                        returned_to_start=False,
                        use_warnsdorff=self.use_warnsdorff,
                    )
                )
            return successors

        # Fase 2: depois de visitar 64 casas, retornar ao inicio em um salto.
        for d_row, d_col in self.KNIGHT_DELTAS:
            new_row = self.row + d_row
            new_col = self.col + d_col
            if not (0 <= new_row < self.board_size and 0 <= new_col < self.board_size):
                continue
            if (new_row, new_col) == (self.start_row, self.start_col):
                successors.append(
                    MyAgent(
                        op="retorna_inicio",
                        row=new_row,
                        col=new_col,
                        start_row=self.start_row,
                        start_col=self.start_col,
                        visited=self.visited,
                        board_size=self.board_size,
                        returned_to_start=True,
                        use_warnsdorff=self.use_warnsdorff,
                    )
                )
        return successors

    def is_goal(self) -> bool:
        return (
            self.returned_to_start
            and len(self.visited) == self.board_size * self.board_size
            and (self.row, self.col) == (self.start_row, self.start_col)
        )

    def description(self) -> str:
        return "Passeio do cavalo 8x8: visitar todas as casas e retornar ao inicio"

    def cost(self) -> int:
        return 1

    def h(self) -> int:
        # Heuristica simples: quanto menor, melhor.
        return self.board_size * self.board_size - len(self.visited)

    def env(self) -> tuple[int, int, tuple[tuple[int, int], ...], bool]:
        # Representacao de estado usada na poda dos algoritmos de busca.
        return (self.row, self.col, self.visited, self.returned_to_start)

    def _onward_degree(
        self,
        row: int,
        col: int,
        visited_set: set[tuple[int, int]],
    ) -> int:
        degree = 0
        for d_row, d_col in self.KNIGHT_DELTAS:
            new_row = row + d_row
            new_col = col + d_col
            if not (0 <= new_row < self.board_size and 0 <= new_col < self.board_size):
                continue
            if (new_row, new_col) in visited_set:
                continue
            degree += 1
        return degree


def build_algorithm(name: str):
    if name == "largura":
        return BuscaLargura(), False, "BuscaLargura"
    if name == "profundidade":
        return BuscaProfundidade(), True, "BuscaProfundidade"
    if name == "profundidade_iterativa":
        return BuscaProfundidadeIterativa(), False, "BuscaProfundidadeIterativa"
    if name == "custo_uniforme":
        return BuscaCustoUniforme(), False, "BuscaCustoUniforme"
    if name == "gulosa":
        return BuscaGananciosa(), False, "BuscaGananciosa"
    if name == "a_estrela":
        return AEstrela(), False, "AEstrela"
    raise ValueError(f"Algoritmo desconhecido: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Passeio do cavalo 8x8 com aigyminsper")
    parser.add_argument(
        "--algoritmo",
        choices=[
            "largura",
            "profundidade",
            "profundidade_iterativa",
            "custo_uniforme",
            "gulosa",
            "a_estrela",
        ],
        default="profundidade",
        help="Algoritmo de busca para executar",
    )
    parser.add_argument(
        "--pruning",
        choices=["without", "father-son", "general"],
        default="general",
        help="Tipo de poda da biblioteca",
    )
    parser.add_argument(
        "--warnsdorff",
        action="store_true",
        help="Ativa heuristica de grau de Warnsdorff para ordenar sucessores",
    )
    args = parser.parse_args()

    initial_state = MyAgent(op="", use_warnsdorff=args.warnsdorff)
    algorithm, needs_depth_limit, class_name = build_algorithm(args.algoritmo)

    print(f"\nExecutando: {args.algoritmo} ({class_name})")
    print(f"Warnsdorff: {'ativo' if args.warnsdorff else 'inativo'}")
    started = time.perf_counter()

    if needs_depth_limit:
        # m=64: 63 movimentos para visitar as outras casas + 1 para retornar.
        result = algorithm.search(initial_state, m=64, pruning=args.pruning)
    else:
        result = algorithm.search(initial_state, pruning=args.pruning)

    elapsed = time.perf_counter() - started

    if result is not None:
        print("Achou!")
        print(result.show_path())
        print(f"Custo total: {result.g}")
        print(f"Tempo: {elapsed:.2f}s")
    else:
        print("Nao achou solucao")
        print(f"Tempo: {elapsed:.2f}s")

if __name__ == "__main__":
    main()
