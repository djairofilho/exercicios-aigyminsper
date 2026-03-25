---
name: aigyminsper-workflow
description: "Use when: defining aigyminsper State problems (successors, is_goal, description, cost, env), configuring search comparisons, or implementing BuscaLargura, BuscaProfundidade, BuscaProfundidadeIterativa, BuscaCustoUniforme, BuscaGananciosa, and AEstrela."
---

# Aigyminsper Workflow Skill

## Goal
Create a minimal, reproducible search workflow for aigyminsper with clear definitions, algorithm implementations, and evaluation.

## Use When
- The user asks to create definitions/configs for aigyminsper.
- The user asks for BFS, DFS, IDS, uniform-cost, greedy, or A* implementations.
- The user asks for clean project structure to compare search strategies.
- The user asks to follow the official User Guide interface and naming.

## Inputs to Confirm
- Environment or problem name.
- Algorithm target (BuscaLargura, BuscaProfundidade, BuscaProfundidadeIterativa, BuscaCustoUniforme, BuscaGananciosa, AEstrela).
- Primary metric (solution cost, nodes expanded, depth, execution time).
- Pruning mode (`without`, `father-son`, or `general`) when relevant.

## Workflow
1. Create typed configuration objects (`ProblemConfig`, `SearchConfig`).
2. Implement a `State` subclass with required methods: `successors`, `is_goal`, `description`, `cost`, `env`.
3. Implement successor function and goal test wrappers.
4. Use official library algorithms for execution and comparison.
5. Add optional pruning comparisons (`without`, `father-son`, `general`).
6. Provide comparison checklist (cost, expansions, depth, runtime).

## Output Template
- `definitions.py`: enums, dataclasses, protocol/type aliases.
- `problem.py`: initial state, goal test, successors, cost function.
- `search.py`: runs with BuscaLargura/BuscaProfundidade/BuscaProfundidadeIterativa/BuscaCustoUniforme/BuscaGananciosa/AEstrela.
- `evaluate.py`: algorithm benchmarking and summary stats.

## Quality Bar
- Reproducible runs through deterministic tie-break rules.
- No hidden constants in frontier or cost handling.
- Clear separation between problem model and search strategy.
- Minimal but complete docstrings in public functions.

## Trigger Phrases
- "crie as definicoes para aigyminsper"
- "configure skill e instructions para busca em IA"
- "implemente bfs dfs ids ucs gulosa e a*"
- "estrutura comparacao de algoritmos de busca"
- "use a interface State oficial do ai gym"
