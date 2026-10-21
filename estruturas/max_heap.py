"""
ED 1 — Max-Heap (Fila de Prioridade)

Árvore binária COMPLETA guardada dentro de um array (lista do Python).
Propriedade do heap: todo pai é mais urgente que seus filhos.
Consequência: o chamado mais urgente está SEMPRE na posição 0.

Navegação no array (sem ponteiros):
    filho esquerdo de i  -> 2*i + 1
    filho direito de i   -> 2*i + 2
    pai de i             -> (i - 1) // 2

    Inserir:          O(log n)  (sobe no máximo a altura da árvore)
    Remover o máximo: O(log n)  (desce no máximo a altura da árvore)
    Consultar o topo: O(1)
"""

import heapq
import itertools


class GerenciadorHeap:
    """Max-Heap implementado do zero, sem bibliotecas."""

    def __init__(self, registrar_passos=False):
        # Cada posição guarda a tupla (prioridade, -ordem_de_chegada, chamado).
        # Comparar duas tuplas compara primeiro a prioridade; no empate, compara
        # -ordem_de_chegada, e quem chegou antes tem o valor MAIOR. Assim
        # "tupla maior" significa exatamente "deve ser atendido antes".
        self._dados = []
        self._chegada = itertools.count()
        self.comparacoes = 0     # total de comparações feitas (para análise)
        # Na demonstração guardamos cada troca para mostrar na tela.
        # No benchmark fica desligado, para não medir o tempo de montar textos.
        self.registrar_passos = registrar_passos
        self.ultimos_passos = []

    # ---------------------------------------------------------------- apoio

    def _trocar(self, i, j):
        if self.registrar_passos:
            self.ultimos_passos.append(
                f"troca posição {i} (prio {self._dados[i][0]}) <-> posição {j} (prio {self._dados[j][0]})"
            )
        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]

    # ------------------------------------------------------------- operações

    def inserir(self, chamado):
        self.ultimos_passos = []
        self._dados.append((chamado.prioridade, -next(self._chegada), chamado))
        self._subir(len(self._dados) - 1)

    def remover_mais_urgente(self):
        self.ultimos_passos = []
        if not self._dados:
            return None
        topo = self._dados[0][2]
        ultimo = self._dados.pop()
        if self._dados:
            # O último elemento vai para a raiz e desce até o lugar certo.
            self._dados[0] = ultimo
            self._descer(0)
        return topo

    def espiar(self):
        return self._dados[0][2] if self._dados else None

    def __len__(self):
        return len(self._dados)

    # ------------------------------------------------- reorganização do heap

    def _subir(self, i):
        """Sift-up: enquanto for mais urgente que o pai, troca com ele."""
        dados = self._dados
        while i > 0:
            pai = (i - 1) // 2
            self.comparacoes += 1
            if dados[i] <= dados[pai]:
                break
            self._trocar(i, pai)
            i = pai

    def _descer(self, i):
        """Sift-down: troca com o filho mais urgente até nenhum filho superar o pai."""
        dados = self._dados
        n = len(dados)
        while True:
            esq, dir_ = 2 * i + 1, 2 * i + 2
            maior = i
            if esq < n:
                self.comparacoes += 1
                if dados[esq] > dados[maior]:
                    maior = esq
            if dir_ < n:
                self.comparacoes += 1
                if dados[dir_] > dados[maior]:
                    maior = dir_
            if maior == i:
                break
            self._trocar(i, maior)
            i = maior

    # ---------------------------------------------------------- visualização

    def listar(self):
        """Chamados na ordem em que serão atendidos (não altera o heap)."""
        return [item[2] for item in sorted(self._dados, reverse=True)]

    def desenhar(self):
        if not self._dados:
            return "  (heap vazio)"
        linhas = ["  Array interno:"]
        linhas.append("    índice:     " + " ".join(f"{i:>3}" for i in range(len(self._dados))))
        linhas.append("    prioridade: " + " ".join(f"{t[0]:>3}" for t in self._dados))
        linhas.append("  Mesma informação vista como árvore (nível a nível):")
        nivel, inicio = 0, 0
        while inicio < len(self._dados):
            fim = min(inicio + 2 ** nivel, len(self._dados))
            nos = "  ".join(f"[{t[0]}]#{t[2].id}" for t in self._dados[inicio:fim])
            linhas.append(f"    nível {nivel}: {nos}")
            inicio, nivel = fim, nivel + 1
        return "\n".join(linhas)


class GerenciadorHeapq:
    """
    Mesmo Max-Heap, usando o módulo heapq da biblioteca padrão (escrito em C).
    Serve só de REFERÊNCIA no benchmark, para comparar com a implementação própria.

    O heapq é um MIN-heap; por isso a prioridade entra com sinal invertido.
    """

    def __init__(self):
        self._heap = []
        self._chegada = itertools.count()

    def inserir(self, chamado):
        heapq.heappush(self._heap, (-chamado.prioridade, next(self._chegada), chamado))

    def remover_mais_urgente(self):
        return heapq.heappop(self._heap)[2] if self._heap else None

    def espiar(self):
        return self._heap[0][2] if self._heap else None

    def __len__(self):
        return len(self._heap)
