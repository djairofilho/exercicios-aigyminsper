from __future__ import annotations

import argparse
from typing import Iterable

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import (
    AEstrela,
    BuscaGananciosa,
    BuscaLargura,
    BuscaProfundidade,
)


DIRECTIONS: tuple[str, ...] = ("N", "L", "S", "O")
DELTAS: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


class AspiradorPo10x10(State):
    def __init__(
        self,
        op: str,
        row: int,
        col: int,
        direction: int,
        grid: tuple[tuple[int, ...], ...],
    ) -> None:
        super().__init__(op)
        self.row = row
        self.col = col
        self.direction = direction
        self.grid = grid
        self.size = len(grid)

    def successors(self) -> list[AspiradorPo10x10]:
        successors: list[AspiradorPo10x10] = []

        # virar para a esquerda
        successors.append(
            AspiradorPo10x10(
                "virar_esquerda",
                self.row,
                self.col,
                (self.direction - 1) % 4,
                self.grid,
            )
        )

        # virar para a direita
        successors.append(
            AspiradorPo10x10(
                "virar_direita",
                self.row,
                self.col,
                (self.direction + 1) % 4,
                self.grid,
            )
        )

        # ir para frente (somente se estiver dentro da grade)
        d_row, d_col = DELTAS[self.direction]
        new_row = self.row + d_row
        new_col = self.col + d_col
        if 0 <= new_row < self.size and 0 <= new_col < self.size:
            successors.append(
                AspiradorPo10x10(
                    "ir_frente",
                    new_row,
                    new_col,
                    self.direction,
                    self.grid,
                )
            )

        # limpar (somente se a posicao atual estiver suja)
        if self.grid[self.row][self.col] == 1:
            new_grid = [list(line) for line in self.grid]
            new_grid[self.row][self.col] = 0
            clean_grid = tuple(tuple(line) for line in new_grid)
            successors.append(
                AspiradorPo10x10(
                    "limpar",
                    self.row,
                    self.col,
                    self.direction,
                    clean_grid,
                )
            )

        return successors

    def is_goal(self) -> bool:
        return all(cell == 0 for row in self.grid for cell in row)

    def description(self) -> str:
        return "Aspirador de Po em casa NxN com frente/esquerda/direita/limpar"

    def cost(self) -> int:
        return 1

    def h(self) -> int:
        dirty_positions = self._dirty_positions()
        if not dirty_positions:
            return 0

        nearest = min(
            abs(self.row - d_row) + abs(self.col - d_col)
            for d_row, d_col in dirty_positions
        )

        # Termo principal: quantidade de quartos sujos.
        return len(dirty_positions) + nearest

    def env(self) -> str:
        flat = "".join(str(cell) for row in self.grid for cell in row)
        return f"{self.row}#{self.col}#{self.direction}#{flat}"

    def _dirty_positions(self) -> list[tuple[int, int]]:
        dirties: list[tuple[int, int]] = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 1:
                    dirties.append((i, j))
        return dirties


def build_grid(size: int, mode: str) -> tuple[tuple[int, ...], ...]:
    if mode == "all_dirty":
        return tuple(tuple(1 for _ in range(size)) for _ in range(size))

    if mode == "sample":
        # Configuracao exemplo: sujeira espalhada, mantendo o problema leve para teste.
        grid = [[0 for _ in range(size)] for _ in range(size)]
        for idx in range(0, size, 2):
            grid[idx][idx] = 1
            grid[idx][size - 1 - idx] = 1
        return tuple(tuple(line) for line in grid)

    raise ValueError("mode invalido")


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
    parser = argparse.ArgumentParser(description="Aspirador de Po em casa 10x10")
    parser.add_argument(
        "--algoritmo",
        choices=["largura", "profundidade", "gulosa", "a_estrela"],
        default="gulosa",
    )
    parser.add_argument(
        "--pruning",
        choices=["without", "father-son", "general"],
        default="general",
    )
    parser.add_argument("--size", type=int, default=10)
    parser.add_argument(
        "--mode",
        choices=["sample", "all_dirty"],
        default="sample",
        help="sample: teste rapido | all_dirty: todos os quartos sujos",
    )
    args = parser.parse_args()

    grid = build_grid(args.size, args.mode)
    initial_state = AspiradorPo10x10("", 0, 0, 1, grid)
    algorithm, needs_depth = build_algorithm(args.algoritmo)

    if needs_depth:
        result = algorithm.search(
            initial_state,
            m=args.size * args.size * 4,
            pruning=args.pruning,
        )
    else:
        result = algorithm.search(initial_state, pruning=args.pruning)

    if result is not None:
        print("Achou!")
        print(result.show_path())
        print(f"Custo total: {result.g}")
    else:
        print("Nao achou solucao")


if __name__ == "__main__":
    main()
