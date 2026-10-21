# Sistema de Distribuição de Chamados Técnicos por Prioridade

Trabalho da disciplina **Estrutura de Dados** (UniRuy Wyden), professor Heleno Cardoso.
Aluno: Gabriel Trisi.

> **Pergunta do trabalho:** dado um problema real, qual Estrutura de Dados é mais adequada para solucioná-lo e por quê?
>
> **Resposta:** para distribuir chamados técnicos por prioridade, a estrutura mais adequada é o **Max-Heap (fila de prioridade)**. O problema só precisa de três coisas: inserir chamados, saber qual é o mais urgente e retirá-lo. O heap faz as três em O(log n) ou menos, **garantido**, sem piorar quando muitos chamados têm a mesma prioridade, que é justamente o que acontece numa central de suporte.

## Sumário

1. [Situação-problema](#1-situação-problema)
2. [Solução proposta](#2-solução-proposta)
3. [ED 1: Max-Heap](#3-ed-1-max-heap-fila-de-prioridade)
4. [ED 2: Lista Encadeada Ordenada](#4-ed-2-lista-encadeada-ordenada)
5. [ED 3: Árvore Binária de Busca](#5-ed-3-árvore-binária-de-busca-bst)
6. [Comparação entre as três EDs](#6-comparação-entre-as-três-eds)
7. [Escolha da melhor ED e justificativa](#7-escolha-da-melhor-ed-e-justificativa)
8. [Como executar](#8-como-executar)
9. [Organização do código](#9-organização-do-código)
10. [Referências](#10-referências)

---

## 1. Situação-problema

A equipe de TI de uma empresa recebe chamados de suporte o dia inteiro: impressora sem toner, senha esquecida, VPN instável, servidor fora do ar. Hoje esses pedidos chegam por e-mail e WhatsApp, e cada técnico pega o que vê primeiro.

O resultado é conhecido: **um servidor parado espera na fila atrás de uma troca de toner**. Enquanto isso, a empresa inteira fica sem sistema.

Cada chamado recebe um nível de urgência:

| Prioridade | Nível   | Exemplo                               |
|:----------:|---------|---------------------------------------|
| 5          | Crítica | Servidor de banco de dados fora do ar |
| 4          | Urgente | VPN caindo para a equipe comercial    |
| 3          | Alta    | Lentidão no sistema de vendas         |
| 2          | Normal  | Usuário esqueceu a senha do e-mail    |
| 1          | Baixa   | Impressora do RH sem toner            |

### Regras que o sistema precisa cumprir

- **R1.** Quando um técnico fica livre, ele recebe sempre o chamado **mais urgente** da fila.
- **R2.** Entre chamados de mesma urgência, é atendido primeiro o **mais antigo**, para nenhum chamado ficar esquecido.
- **R3.** Chamados entram e saem **o tempo todo**, intercalados, e em dias de crise podem ser milhares.

### Características do problema que decidem a escolha da ED

1. As operações frequentes são só **inserir** e **retirar o mais urgente**.
2. O sistema **não precisa** manter a fila inteira ordenada. Precisa apenas saber quem é o próximo.
3. Há **poucos níveis de prioridade (1 a 5) e muitos chamados**. Portanto, **prioridades repetidas são a regra**, não a exceção.

---

## 2. Solução proposta

Um sistema em Python que funciona como a **central de chamados**. O técnico usa um menu no terminal para:

- abrir um chamado (descrição + prioridade);
- atender o chamado mais urgente;
- ver a fila na ordem em que será atendida;
- ver por dentro as estruturas de dados que guardam a fila;
- rodar um teste de estresse com milhares de chamados.

**Papel da Estrutura de Dados:** a ED **é a fila da central**. É ela que decide qual chamado sai a cada atendimento. Se a ED for lenta para inserir ou para achar o mais urgente, a central inteira fica lenta. Se a ED errar a ordem, um chamado crítico é atendido tarde.

O mesmo problema foi implementado com **três EDs diferentes**, todas com as mesmas operações (`inserir`, `remover_mais_urgente`, `espiar`). Assim dá para comparar as três de forma justa, com os mesmos dados. O sistema usa o **Max-Heap** como estrutura principal. A lista e a árvore recebem os mesmos chamados em paralelo, só para comparação na demonstração.

Todas as três estruturas foram **implementadas do zero**, sem bibliotecas prontas. O módulo `heapq` do Python aparece apenas no benchmark, como referência de velocidade.

---

## 3. ED 1: Max-Heap (fila de prioridade)

Arquivo: [`estruturas/max_heap.py`](estruturas/max_heap.py)

### Como a ED é utilizada

O Max-Heap é uma árvore binária **completa** (todos os níveis cheios, menos talvez o último, que é preenchido da esquerda para a direita) guardada dentro de um **array**. Ele segue uma única regra: **todo pai é mais urgente que seus filhos**. Por isso, o chamado mais urgente está sempre na **posição 0**.

```
         array:  [ 5 | 4 | 3 | 2 | 1 ]
         índice:   0   1   2   3   4

         a mesma coisa vista como árvore:
                    [5]            <- posição 0: o mais urgente
                   /   \
                 [4]   [3]
                /   \
              [2]   [1]

   filhos da posição i: 2i+1 e 2i+2        pai da posição i: (i-1)//2
```

Não há ponteiros: as posições de pai e filhos são calculadas com essas fórmulas.

Cada posição guarda `(prioridade, -ordem_de_chegada, chamado)`. Comparar duas tuplas compara primeiro a prioridade e, no empate, a ordem de chegada. Isso cumpre a regra R2 sem código extra.

### Operações necessárias

| Operação | Como funciona | Custo |
|---|---|---|
| `inserir` | Coloca o chamado no fim do array e o faz **subir** (*sift-up*), trocando com o pai enquanto for mais urgente que ele | O(log n) |
| `remover_mais_urgente` | Retira a posição 0, coloca o último elemento no lugar e o faz **descer** (*sift-down*), trocando com o filho mais urgente | O(log n) |
| `espiar` | Lê a posição 0 | O(1) |

O número de trocas nunca passa da **altura** da árvore, que é `log₂ n`. Com 1.000.000 de chamados, são no máximo 20 trocas.

### Vantagens

- Inserir e remover custam **O(log n) sempre**. A árvore é completa por construção, então não existe caso em que ela fique desequilibrada.
- Consultar o mais urgente é imediato: **O(1)**.
- O desempenho **não depende dos dados**: prioridades repetidas ou chamados chegando em ordem não pioram nada.
- Fica num **array contíguo**: usa pouca memória (sem ponteiros) e aproveita bem a memória cache do processador.
- A implementação é curta: duas operações (subir e descer).

### Limitações

- **Não serve para buscar um chamado qualquer** (por exemplo, o #57 para cancelá-lo): é preciso percorrer o array, O(n).
- Fora a posição 0, o array **não está ordenado**. Listar a fila inteira em ordem exige ordenar uma cópia, O(n log n).
- Alterar a prioridade de um chamado que já está na fila exige primeiro achá-lo, o que custa O(n).

### Impacto na solução

O heap atende exatamente às operações que a central faz o tempo todo, e com custo baixo e previsível. As limitações estão em operações **raras** neste problema (cancelar chamado, listar a fila toda), que só seriam usadas de vez em quando por um supervisor.

---

## 4. ED 2: Lista Encadeada Ordenada

Arquivo: [`estruturas/lista_encadeada.py`](estruturas/lista_encadeada.py)

### Como a ED é utilizada

Cada chamado é um **nó** que aponta para o próximo. A lista é mantida **sempre em ordem**, do mais urgente para o menos urgente, então o próximo a ser atendido está sempre na **cabeça**.

```
cabeça -> [5] -> [4] -> [3] -> [2] -> [1] -> None
```

### Operações necessárias

| Operação | Como funciona | Custo |
|---|---|---|
| `inserir` | Percorre a lista desde a cabeça até achar a posição certa (depois dos chamados de mesma prioridade, para cumprir R2) e encaixa o nó ali | **O(n)** |
| `remover_mais_urgente` | Retira a cabeça | O(1) |
| `espiar` | Lê a cabeça | O(1) |

### Vantagens

- Remover e consultar o mais urgente são **imediatos**: O(1).
- A fila está **sempre ordenada**. Listar todos os chamados em ordem é só percorrer a lista, O(n).
- É a ideia mais **intuitiva** e fácil de implementar.
- Cresce sem precisar realocar memória.

### Limitações

- **Inserir custa O(n)**. Cada chamado novo pode ter de passar por todos os que já estão na fila.
- Inserir *n* chamados custa **O(n²)** no total. Dobrar a quantidade de chamados **quadruplica** o trabalho.
- Com muitas prioridades repetidas, um chamado novo precisa passar por **todos** os de mesma prioridade para chegar ao fim do seu grupo. Isso é o pior caso, e no nosso problema ele acontece sempre.
- Cada nó guarda um ponteiro extra, e os nós ficam espalhados na memória.

### Impacto na solução

A lista coloca todo o trabalho na inserção, que é uma das operações mais frequentes da central. Em um dia normal isso passa despercebido. Num pico de chamados, a abertura de chamados fica lenta justamente quando há mais gente pedindo ajuda.

---

## 5. ED 3: Árvore Binária de Busca (BST)

Arquivo: [`estruturas/arvore_bst.py`](estruturas/arvore_bst.py)

### Como a ED é utilizada

A chave da árvore é a prioridade: valores **menores à esquerda e maiores à direita**. O chamado mais urgente é o **nó mais à direita** da árvore.

```
            [3]
           /   \
         [2]   [5]   <- nó mais à direita = mais urgente
         /     /
       [1]   [4]
```

Chamados de mesma prioridade vão para a esquerda. Assim, o mais antigo fica mais à direita e é atendido primeiro (regra R2).

### Operações necessárias

| Operação | Como funciona | Custo |
|---|---|---|
| `inserir` | Desce comparando (maior vai para a direita, menor ou igual para a esquerda) até achar um espaço vazio | O(h) |
| `remover_mais_urgente` | Desce sempre para a direita até o último nó. Como ele não tem filho direito, basta o pai apontar para o filho esquerdo dele | O(h) |
| `espiar` | Desce sempre para a direita | O(h) |

O custo depende da **altura `h`** da árvore:

- árvore equilibrada → `h ≈ log n` → rápida;
- árvore **degenerada** (chaves repetidas ou chegando em ordem) → `h ≈ n` → tão lenta quanto uma lista.

### Vantagens

- Com prioridades bem variadas, inserir e remover custam perto de **O(log n)**.
- Mantém **ordem total**: percorrer em ordem lista a fila inteira em O(n).
- Permite **buscar por prioridade** em O(h) (por exemplo, "existe algum chamado de prioridade 4?").

### Limitações

- **Não tem garantia de desempenho**: depende da ordem e da distribuição dos dados.
- No nosso problema há só 5 prioridades possíveis, então quase todas as chaves se repetem e **a árvore degenera em uma lista**. Com 10.000 chamados, a árvore medida ficou com **2.074 níveis** de altura (com prioridades de 1 a 1.000, foram 36). O heap, com os mesmos 10.000 chamados, tem **14 níveis**.
- Evitar a degeneração exige uma árvore **autobalanceada** (AVL ou Rubro-Negra), com rotações e bem mais código.
- Cada nó guarda dois ponteiros.
- As operações precisaram ser escritas **sem recursão**: com a árvore degenerada, a recursão estoura o limite de chamadas do Python (`RecursionError`).

### Impacto na solução

A BST funciona bem em testes "de laboratório" com prioridades bem espalhadas. No cenário real da central, com prioridades de 1 a 5, ela degenera e perde a vantagem. Ela também oferece recursos (ordem total, busca por chave) que a central não usa.

---

## 6. Comparação entre as três EDs

### Critérios pedidos no trabalho

| Critério | Max-Heap | Lista Encadeada Ordenada | Árvore Binária de Busca |
|---|---|---|---|
| **Facilidade de implementação** | Média: duas rotinas curtas (subir e descer) e fórmulas de índice | **Fácil**: só percorrer e encaixar | Média: remoção com casos de ponteiros; balancear seria difícil |
| **Custo das operações** | Inserir O(log n), remover O(log n), espiar O(1) | Inserir **O(n)**, remover O(1), espiar O(1) | Inserir O(h), remover O(h), espiar O(h); h vai de log n a **n** |
| **Desempenho (10.000 chamados, prioridades 1–5)** | **234 mil comparações** | 30,1 milhões de comparações | 10,0 milhões de comparações |
| **Organização dos dados** | Array; ordem **parcial** (só pai ≥ filhos) | Nós encadeados; ordem **total** | Nós com 2 ponteiros; ordem **total** pela chave |
| **Inserção e remoção** | Equilibradas: as duas O(log n) | Desequilibradas: remoção barata, inserção cara | Boas só se a árvore estiver equilibrada |
| **Busca e acesso** | Acesso ao mais urgente O(1); busca de chamado qualquer O(n) | Acesso ao mais urgente O(1); busca O(n) | Acesso ao mais urgente O(h); busca por prioridade O(h), por id O(n) |
| **Adequação ao problema real** | **Alta**: faz exatamente o que a central precisa, sem degenerar | Baixa: fica lenta nos picos de abertura de chamados | Baixa: degenera com prioridades repetidas |

### Resultados medidos

O arquivo `benchmark.py` gera 10.000 chamados aleatórios (sempre os mesmos, com semente fixa), insere todos e depois atende todos, em cada estrutura. Ele mede duas coisas:

- **comparações entre prioridades**: não dependem do computador e mostram a complexidade de cada ED;
- **tempo em segundos**: varia de máquina para máquina e de execução para execução.

Em todas as execuções, **as três estruturas atenderam os chamados exatamente na mesma ordem**. A diferença entre elas é só o custo.

**Cenário A: prioridades espalhadas de 1 a 1.000** (o caso mais favorável para a árvore)

| Estrutura | Comparações | Tempo total (s) |
|---|---:|---:|
| Max-Heap | 239.213 | 0,035 |
| Lista Encadeada Ordenada | 25.078.773 | 1,832 |
| Árvore Binária de Busca | 228.553 | 0,024 |

**Cenário B: prioridades de 1 a 5** (o caso real de uma central de suporte)

| Estrutura | Comparações | Tempo total (s) |
|---|---:|---:|
| **Max-Heap** | **234.436** | **0,050** |
| Lista Encadeada Ordenada | 30.149.661 | 1,819 |
| Árvore Binária de Busca | 10.036.610 | 0,488 |

**Crescimento das comparações conforme aumenta o número de chamados** (cenário B)

| Chamados | Max-Heap | Lista Encadeada | Árvore BST |
|---:|---:|---:|---:|
| 1.000 | 16.828 | 291.337 | 103.347 |
| 2.500 | 48.701 | 1.845.001 | 633.890 |
| 5.000 | 107.217 | 7.489.877 | 2.517.160 |
| 10.000 | 234.436 | 30.149.661 | 10.036.610 |

### O que os números mostram

- **No cenário A, a árvore empata com o heap** (até um pouco melhor). Esse resultado era esperado: com chaves bem espalhadas, a árvore fica equilibrada. Ele mostra que a árvore só é boa quando os dados ajudam.
- **No cenário B, o caso real, a árvore faz 43 vezes mais comparações que o heap.** Mudou só a distribuição das prioridades, e o desempenho dela desabou. O heap fez praticamente o mesmo número de comparações nos dois cenários.
- **A lista** faz mais de 100 vezes mais comparações que o heap nos dois cenários. Na tabela de crescimento, cada vez que o número de chamados dobra, o trabalho da lista **quadruplica** (comportamento O(n²)), enquanto o do heap apenas **dobra e um pouco** (O(n log n)).
- O Max-Heap feito em C da biblioteca padrão (`heapq`) aparece no benchmark como referência: com a mesma lógica, ele é ainda mais rápido. Isso confirma que a escolha da ED pesa mais que a linguagem.

---

## 7. Escolha da melhor ED e justificativa

**A ED escolhida é o Max-Heap.** A justificativa liga cada característica dele a uma necessidade do problema:

| Necessidade da central | Característica do Max-Heap que atende |
|---|---|
| Saber na hora quem é o próximo a ser atendido | O mais urgente está **sempre na posição 0**: consulta O(1) |
| Abrir e atender chamados o tempo todo, inclusive em picos | Inserir e remover custam **O(log n)**: com 1 milhão de chamados, no máximo 20 trocas |
| Funcionar com poucos níveis de prioridade e muitos chamados repetidos | A árvore é **sempre completa**: a altura é log n **qualquer que seja o dado**, e repetições não a degeneram |
| Não deixar chamado antigo esquecido (R2) | A ordem de chegada entra na comparação, então o desempate é automático |
| Não precisa da fila toda ordenada | O heap mantém só a **ordem parcial** necessária. Ordem total (lista e árvore) é trabalho a mais que a central não usa |

### Por que não as outras

- **Lista Encadeada Ordenada:** é rápida para atender, mas paga O(n) a cada chamado aberto. Ela mantém a fila inteira ordenada, um trabalho que o problema não pede. No benchmark, fez 128 vezes mais comparações que o heap.
- **Árvore Binária de Busca:** em média é boa, mas **o problema real é o pior caso dela**. Poucos níveis de prioridade geram chaves repetidas e degeneram a árvore. Consertar isso exigiria uma árvore balanceada (AVL ou Rubro-Negra), muito mais complexa, para continuar oferecendo recursos que a central não usa.

### Conclusão

O que torna o Max-Heap a melhor escolha **para este problema** não é ser "a estrutura mais rápida" em geral. É fazer apenas o que a central precisa, isto é, achar e retirar o mais urgente, com custo garantido e independente do padrão dos dados. A limitação dele (não buscar um chamado qualquer) recai sobre uma operação rara neste cenário.

Por isso filas de prioridade baseadas em heap são usadas, na prática, em escalonadores de processos de sistemas operacionais, em sistemas de triagem e no algoritmo de Dijkstra.

---

## 8. Como executar

### Pré-requisitos

- Python 3.8 ou superior (`python --version`).
- Nenhuma biblioteca externa: o projeto usa só a biblioteca padrão.

### Passo a passo

```bash
# 1. Baixar o projeto
git clone https://github.com/gabrieltrisi/sistema-chamados-prioridade.git
cd sistema-chamados-prioridade

# 2. Abrir o sistema (menu interativo)
python sistema_prioridades.py

# 3. Rodar só o benchmark
python sistema_prioridades.py --benchmark

# 4. Rodar os testes unitários
python -m unittest -v test_sistema_prioridades
```

### O menu

O sistema começa com 5 chamados de exemplo na fila:

```
============================================================
 CENTRAL DE CHAMADOS TÉCNICOS - estrutura principal: MAX-HEAP
============================================================
 Chamados na fila: 5
 Próximo a ser atendido: #2 [5 - Crítica] Servidor de banco de dados fora do ar
------------------------------------------------------------
 1. Abrir novo chamado
 2. Atender o chamado mais urgente
 3. Ver a fila em ordem de atendimento
 4. Ver as 3 estruturas por dentro
 5. Rodar benchmark de estresse
 0. Sair
```

| Opção | O que mostra |
|:---:|---|
| 1 | Abre o chamado e mostra **cada troca que o heap fez** para reposicioná-lo, além de quantas comparações cada ED precisou |
| 2 | Atende o mais urgente e mostra as trocas feitas para reorganizar o heap |
| 3 | A fila na ordem em que será atendida |
| 4 | **O interior das 3 estruturas**: o array do heap (e a mesma informação como árvore), a lista com os ponteiros e a árvore desenhada |
| 5 | Benchmark com a quantidade de chamados que você escolher |

Exemplo da opção 4:

```
[ MAX-HEAP ]  (o mais urgente fica na posição 0)
  Array interno:
    índice:       0   1   2   3   4   5
    prioridade:   5   4   5   1   3   2
  Mesma informação vista como árvore (nível a nível):
    nível 0: [5]#2
    nível 1: [4]#4  [5]#6
    nível 2: [1]#1  [3]#5  [2]#3

[ LISTA ENCADEADA ORDENADA ]  (o mais urgente fica na cabeça)
  cabeça -> [5]#2 -> [5]#6 -> [4]#4 -> [3]#5 -> [2]#3 -> [1]#1 -> None

[ ÁRVORE BINÁRIA DE BUSCA ]  (deitada: o mais urgente é o nó mais alto à direita)
        [5]#2
                          [5]#6
                    [4]#4
                          [3]#5
              [2]#3
  [1]#1
  (altura da árvore: 5)
```

Com apenas 6 chamados, a árvore já tem altura 5: ela está virando uma lista. O heap, com os mesmos 6 chamados, tem 3 níveis.

### Testes unitários

São 15 testes. Os principais verificam o Max-Heap:

| Teste | O que garante |
|---|---|
| `test_maior_prioridade_sai_primeiro` | Os chamados saem do mais urgente para o menos urgente |
| `test_maior_fica_na_posicao_zero` | O mais urgente está sempre na posição 0 do array |
| `test_propriedade_de_heap_mantida_em_toda_operacao` | Depois de **cada** inserção e remoção, todo pai continua ≥ filhos |
| `test_empate_respeita_ordem_de_chegada` | Mesma prioridade: o mais antigo sai primeiro |
| `test_maior_sempre_sai_primeiro_com_dados_aleatorios` | 2.000 chamados aleatórios saem sempre em ordem |
| `test_insercao_intercalada_com_remocao` | Abrir e atender misturados mantém a regra |
| `test_insercao_custa_no_maximo_log_n_comparacoes` | No pior caso, inserir em um heap de 1.024 itens faz no máximo 10 comparações |
| `test_fila_vazia` / `test_espiar_nao_remove` / `test_listar_nao_altera_fila` | Casos de borda |
| `test_as_quatro_implementacoes_atendem_na_mesma_ordem` | Heap, lista, árvore e `heapq` produzem a mesma ordem de atendimento |

---

## 9. Organização do código

```
sistema-chamados-prioridade/
├── chamado.py                    # classe Chamado (id, descrição, prioridade)
├── estruturas/
│   ├── max_heap.py               # ED 1: Max-Heap (+ versão heapq, só para referência)
│   ├── lista_encadeada.py        # ED 2: Lista Encadeada Ordenada
│   └── arvore_bst.py             # ED 3: Árvore Binária de Busca
├── benchmark.py                  # comparação de desempenho
├── sistema_prioridades.py        # programa principal (menu da central)
├── test_sistema_prioridades.py   # testes unitários
└── docs/
    └── apresentacao.pptx         # slides da apresentação
```

---

## 10. Referências

- CORMEN, T. H. et al. *Algoritmos: Teoria e Prática*. 3. ed. Rio de Janeiro: Elsevier, 2012. Cap. 6 (Heapsort e filas de prioridade) e Cap. 12 (Árvores de busca binária).
- SZWARCFITER, J. L.; MARKENZON, L. *Estruturas de Dados e Seus Algoritmos*. 3. ed. Rio de Janeiro: LTC, 2010.
- PYTHON SOFTWARE FOUNDATION. *heapq: Heap queue algorithm*. Disponível em: https://docs.python.org/3/library/heapq.html.
