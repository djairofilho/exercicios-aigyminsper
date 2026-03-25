# Lista de exercícios adicionais sobre busca em espaço de estados

## Comparacao dos algoritmos de busca

Parametros:

- b: fator de ramificacao medio.
- d: profundidade da solucao (ou limite efetivo de busca).

### Busca em largura (BuscaLargura)

- Beneficios: completa e encontra menor numero de movimentos quando custo e unitario.
- Maleficios: consome muita memoria em espacos de busca grandes.
- Melhor quando: problema pequeno/medio e objetivo de caminho minimo em passos.
- Tempo: O(b^d)
- Memoria: O(b^d)

### Busca em profundidade (BuscaProfundidade)

- Beneficios: pouca memoria e implementacao simples.
- Maleficios: pode entrar em ramos ruins e nao garante melhor caminho.
- Melhor quando: simplicidade e baixo uso de memoria.
- Tempo: O(b^d) no caso limitado pela profundidade d.
- Memoria: O(bd)

### Busca em profundidade iterativa (BuscaProfundidadeIterativa)

- Beneficios: memoria baixa como DFS e completude em profundidade como BFS.
- Maleficios: repete exploracoes das camadas rasas.
- Melhor quando: profundidade da solucao desconhecida com restricao de memoria.
- Tempo: O(b^d)
- Memoria: O(bd)

### Busca de custo uniforme (BuscaCustoUniforme)

- Beneficios: otima para menor custo total com custos nao uniformes.
- Maleficios: pode expandir muitos nos antes da meta.
- Melhor quando: minimizar custo total real.
- Tempo: O(b^d) em aproximacao por camadas de custo/profundidade.
- Memoria: O(b^d)

### Busca gulosa (BuscaGananciosa)

- Beneficios: geralmente encontra resposta rapido com heuristica boa.
- Maleficios: nao garante solucao otima e depende da heuristica.
- Melhor quando: prioridade em velocidade e aceitacao de solucao nao otima.
- Tempo: O(b^d) no pior caso.
- Memoria: O(b^d) no pior caso.

### Busca A* (AEstrela)

- Beneficios: combina custo acumulado e heuristica; com heuristica admissivel e consistente, encontra solucao otima.
- Maleficios: custo alto de memoria em problemas grandes.
- Melhor quando: equilibrio entre qualidade da solucao e desempenho.
- Tempo: O(b^d) no pior caso.
- Memoria: O(b^d) no pior caso.

Resumo pratico:

- Melhor geral: A* (se houver heuristica boa).
- Mais simples: Profundidade.
- Melhor para custo minimo real: Custo Uniforme.

## Cavalo e tabuleiro de xadrez

Considerando um tabuleiro de xadrez (`8x8`) com um
  único cavalo, quais os movimentos que o cavalo deve fazer para
  percorrer todas as posições do tabuleiro uma única vez e
  retornar ao ponto de partida?

Implemente um agente usando a biblioteca `aigyminsper` que resolve este problema.

Implementacao simples (padrao `State` da `aigyminsper`) em `cavalo_xadrez.py`.

Execucao:

```bash
python cavalo_xadrez.py --algoritmo profundidade
```

Outras opcoes de algoritmo:

```bash
python cavalo_xadrez.py --algoritmo largura
python cavalo_xadrez.py --algoritmo profundidade
python cavalo_xadrez.py --algoritmo profundidade_iterativa
python cavalo_xadrez.py --algoritmo custo_uniforme
python cavalo_xadrez.py --algoritmo gulosa
python cavalo_xadrez.py --algoritmo a_estrela
```

Tipo de poda (opcional):

```bash
python cavalo_xadrez.py --algoritmo profundidade --pruning general
```

Observacao: para o problema do cavalo em 8x8, buscas cegas podem demorar bastante.

## Aspirador de Pó em uma casa 10 por 10.

Neste exercício o agente sabe executar outras ações, mas o objetivo dele permanece o mesmo. As ações são: 

* ir para frente;
* virar para a esquerda;
* virar para a direita, e;
* limpar

E as dimensões da casa são de $10 \times 10$ quartos. 

* O que é relevante representar nos estados do mundo? Como os
    estados são estruturados (estrutura de dados) e qual o significado
    dela (dos campos)?
* Mostre como ficam representados os estados inicial e final
    segundo a representação adotada.
* Quais as operações sobre os estados?
    (detalhe como cada operação irá alterar os estados e quais as
    condições para cada operação ser executada)
* Qual a estimativa do tamanho do espaço de busca (número de
    estados possíveis)?
* Será que um algoritmo de busca cega consegue encontrar resposta para todas as configurações iniciais?
* Caso seja necessário utilizar um algoritmo que faz uso de heurísticas, quais seriam as heurísticas que você utilizaria?

Implemente um agente usando a biblioteca aigyminsper que resolve este problema.

## Conjectura de Knuth

O cientista da computação Donal Knuth em 1964 conjecturou que **todo** número inteiro positivo pode ser gerado a partir do número **4** aplicando-se uma combinação de:

* fatorial, 
* raiz quadrada e 
* arredondamento para baixo. 

Por exemplo: 

* o número 2 pode ser gerado por `sqrt(4)`, 
* o número 1 por `round_down(sqrt(sqrt(4)))` e 
* o número 5 por `round_down(sqrt(sqrt(sqrt(sqrt(sqrt(factorial(factorial(4))))))))`.

Implemente um agente autônomo que dado um número inteiro positivo qualquer gere uma sequência de operações que transformam o número 4 no número informado. Nesta implementação você deve utilizar a biblioteca `aigyminsper`. 

## Espaço de busca

Considere um problema de busca em um espaço de estados, onde o objetivo é encontrar o caminho mais curto entre dois pontos em um labirinto bidimensional. O labirinto é representado por uma matriz onde cada célula pode ser um obstáculo ('X') ou um espaço livre ('O'). O agente pode se mover em quatro direções: cima, baixo, esquerda e direita, mas não pode atravessar obstáculos.

1. Descreva como você representaria o espaço de busca para esse problema, incluindo a representação do estado inicial e do estado objetivo.
1. Explique como você implementaria um algoritmo de busca em largura para resolver esse problema.
1. Discuta a eficiência do algoritmo de busca em largura para encontrar o caminho mais curto em termos de tempo e espaço. 1. Você acha que este algoritmo é adequado para este problema? Por quê ou por que não?

**Observações**:

- Você pode assumir que todas as células adjacentes são consideradas vizinhas.
- Considere que a matriz do labirinto é uma representação discreta do espaço contínuo do labirinto.

## Problema das Torres de Hanói

O problema das Torres de Hanói é um quebra-cabeça clássico que envolve mover uma pilha de discos de um poste inicial para um poste final, seguindo certas regras, usando um poste intermediário, de forma que nenhum disco seja colocado sobre um disco menor.

Considere o problema das Torres de Hanói com n discos e 3 postes (A, B e C), onde o objetivo é mover todos os discos do poste inicial para o poste final, obedecendo às seguintes regras:

- Você só pode mover um disco por vez.
- Um disco maior nunca pode ser colocado sobre um disco menor.
- Você pode usar o poste intermediário como auxílio para mover os discos.

Implemente um agente usando a biblioteca `aigyminsper` que resolve este problema.

## Problema do quebra-cabeça de 8 peças

O quebra-cabeça de 8 peças é um quebra-cabeça deslizante que consiste em um tabuleiro de 3x3 com 8 peças numeradas de 1 a 8 e um espaço vazio. O objetivo do quebra-cabeça é mover as peças para que elas estejam ordenadas de forma crescente, com o espaço vazio na posição inferior direita.

1. Descreva como você representaria o espaço de busca para esse problema, incluindo a representação do estado inicial e do estado objetivo.
1. Que algoritmo de busca você usaria para resolver esse problema? Explique por que você escolheu esse algoritmo.
1. É necessário algum tipo de heurística? Se sim, qual heurística você usaria e por quê? 

Implemente um agente usando a biblioteca `aigyminsper` que resolve este problema.

## As 8 rainhas

Coloque oito rainhas em um tabuleiro de
  xadrez (`8x8` casas) de maneira que nenhuma rainha ameace
  outra, i.e., as rainhas não devem compartilhar colunas, linhas ou
  diagonais do tabuleiro.

Implemente um agente usando a biblioteca `aigyminsper` que resolve este problema.