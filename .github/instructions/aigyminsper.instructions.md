---
description: "Use when: implementing aigyminsper search problems with State (successors, is_goal, description, cost, env) and running BuscaLargura, BuscaProfundidade, BuscaProfundidadeIterativa, BuscaCustoUniforme, BuscaGananciosa, or AEstrela."
applyTo: "**/*.py"
---

# Aigyminsper Python Search Instructions

Use these defaults for Python code related to state-space search algorithms.

## Structure
- Implement problem classes by inheriting from `aigyminsper.search.graph.State`.
- Keep problem definitions separated from search execution scripts.
- Keep node expansion logic decoupled from frontier strategy.

## Definitions and Config
- Implement all required State methods: `successors`, `is_goal`, `description`, `cost`, and `env`.
- Centralize problem and search parameters in dataclasses or typed config objects.
- Avoid magic numbers for costs and actions; prefer `Enum` or named constants.

## Algorithm Quality
- Track expansions, generated nodes, frontier size, solution cost, and depth.
- Add loop guards (`max_expansions`, `max_depth`) to avoid runaway execution.
- Ensure deterministic tie-break rules for reproducible comparisons.
- When applicable, compare pruning modes supported by the library: `without`, `father-son`, and `general`.

## Safety and Robustness
- Validate transitions and costs before pushing nodes into the frontier.
- Use a visited/closed policy appropriate for each algorithm.
- Ensure `env()` returns a stable state representation for pruning consistency.

## Code Style
- Use concise, readable functions.
- Add short comments only around non-obvious logic.
- Keep examples aligned with comparative experiments across BFS/DFS/IDS/UCS/Greedy/A*.
