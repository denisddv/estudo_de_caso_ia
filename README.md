# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

**Disciplina:** Artificial Intelligence Fundamentals — UniFECAF

## Problema e objetivos
A Sabor Express define suas rotas manualmente e enfrenta atrasos durante os picos de demanda. O projeto investiga como algoritmos clássicos de IA podem reduzir deslocamentos e tempo de entrega. A cidade é fictícia; os dados não foram coletados de uma empresa real.

## Abordagem
O mapa é um grafo direcionado com 11 vértices (restaurante D e dez destinos) e 35 arcos. Os pesos representam quilômetros e minutos estimados. A rua E → K não admite o sentido inverso direto. A busca A* minimiza minutos entre dois pontos. A heurística é a distância euclidiana multiplicada por 1 minuto/km; os tempos de cada arco excedem essa distância. O vizinho mais próximo escolhe o próximo pedido pelo menor tempo de percurso. K-Means agrupa coordenadas em duas zonas, usando semente 42 e dez inicializações. Não há garantia de ótimo global para a ordem de visitas.

## Algoritmos
BFS minimiza o número de arestas; DFS explora um ramo antes de retroceder; A* combina custo acumulado e heurística (f=g+h); K-Means minimiza a soma das distâncias quadráticas aos centroides. Dijkstra valida os menores caminhos ponderados. Para D até J, BFS e A* obtiveram 16,014 min e DFS 51,574 min.

## Experimento
Dez pedidos, dois entregadores, retorno ao restaurante, três minutos por atendimento, prazo hipotético de 35 minutos e custo variável de R$ 0,22/km. O cenário manual distribui pedidos alternadamente por ordem de chegada e usa A* em cada trecho. O segundo cenário conserva a atribuição e muda a ordem; o terceiro altera também o agrupamento.

| Cenário | km | minutos somados | conclusão (min) | atrasos | custo (R$) |
|---|---:|---:|---:|---:|---:|---:|
| Manual | 57,34 | 236,17 | 119,54 | 7 | 12,61 |
| A* + vizinho | 39,21 | 178,13 | 96,72 | 5 | 8,63 |
| K-Means + A* | 26,50 | 132,93 | 71,07 | 4 | 5,83 |

A solução combinada reduziu a distância em 53,8% e o tempo de conclusão em 40,5%. Os atrasos passaram de sete para quatro. Resultados simulados.

## Validação e limitações
O programa verifica a cobertura dos pedidos e compara A* com Dijkstra nos 121 pares ordenados. K-Means considera proximidade geométrica, não capacidade, barreiras ou prazos. O vizinho mais próximo pode ser subótimo. Próximos passos: GPS, trânsito dinâmico, capacidade, janelas de entrega e VRP.

## Execução
Python 3.11+ (recomendado 3.12).
```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
python -m unittest discover -s tests -v
```
Os gráficos PNG e arquivos de resultados são gerados em outputs/ ao executar o programa.

## Referências
- Russell e Norvig. Artificial Intelligence: A Modern Approach. 4. ed. Pearson, 2021.
- Hart, Nilsson e Raphael. A Formal Basis for the Heuristic Determination of Minimum Cost Paths. IEEE, 1968.
- NetworkX: https://networkx.org/documentation/stable/
- Scikit-learn: https://scikit-learn.org/stable/
- UniFECAF. Orientações de entrega da disciplina.
