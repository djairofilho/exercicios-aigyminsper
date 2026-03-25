from __future__ import annotations

import argparse


def hanoi_backtracking(
	n: int,
	origem: str,
	destino: str,
	auxiliar: str,
	movimentos: list[str],
) -> None:
	if n == 0:
		return

	# Move n-1 discos para liberar o maior disco.
	hanoi_backtracking(n - 1, origem, auxiliar, destino, movimentos)

	# Move o maior disco disponivel da origem para o destino.
	movimentos.append(f"mover disco {n} de {origem} para {destino}")

	# Move os n-1 discos para cima do maior disco no destino.
	hanoi_backtracking(n - 1, auxiliar, destino, origem, movimentos)


def resolver_torres_hanoi(n_discos: int) -> list[str]:
	if n_discos < 1:
		raise ValueError("n_discos deve ser >= 1")

	movimentos: list[str] = []
	hanoi_backtracking(n_discos, "A", "C", "B", movimentos)
	return movimentos


def main() -> None:
	parser = argparse.ArgumentParser(description="Torres de Hanoi (backtracking classico)")
	parser.add_argument("--disks", type=int, default=4, help="Numero de discos")
	parser.add_argument(
		"--show-steps",
		action="store_true",
		help="Mostra cada movimento no terminal",
	)
	args = parser.parse_args()

	movimentos = resolver_torres_hanoi(args.disks)

	print("Achou!")
	print(f"Total de movimentos: {len(movimentos)}")
	print(f"Minimo teorico (2^n - 1): {(2 ** args.disks) - 1}")

	if args.show_steps:
		print("\nPasso a passo:")
		for i, movimento in enumerate(movimentos, start=1):
			print(f"{i:03d}: {movimento}")


if __name__ == "__main__":
	main()
