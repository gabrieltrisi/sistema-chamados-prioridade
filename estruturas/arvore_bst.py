"""
ED 3 — Árvore Binária de Busca (BST)

Chave = prioridade. Menores à esquerda, maiores à direita.
O chamado mais urgente é o nó MAIS À DIREITA da árvore.

Prioridades iguais vão para a ESQUERDA: assim, entre chamados de mesma
prioridade, o mais antigo fica mais à direita e é atendido primeiro.

    Inserir:          O(h)  h = altura da árvore
    Remover o máximo: O(h)
    Árvore equilibrada: h ≈ log n   |   Árvore degenerada: h ≈ n

As operações são iterativas (com laço, sem recursão) porque, quando a árvore
degenera, a recursão estouraria o limite de chamadas do Python.
"""


class _No:
    __slots__ = ("chamado", "esquerda", "direita")

    def __init__(self, chamado):
        self.chamado = chamado
        self.esquerda = None
        self.direita = None


class GerenciadorBST:

    def __init__(self):
        self._raiz = None
        self._tamanho = 0
        self.comparacoes = 0

    def inserir(self, chamado):
        novo = _No(chamado)
        self._tamanho += 1
        if self._raiz is None:
            self._raiz = novo
            return
        atual = self._raiz
        while True:
            self.comparacoes += 1
            if chamado.prioridade > atual.chamado.prioridade:
                if atual.direita is None:
                    atual.direita = novo
                    return
                atual = atual.direita
            else:
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return
                atual = atual.esquerda

    def remover_mais_urgente(self):
        if self._raiz is None:
            return None
        pai = None
        atual = self._raiz
        while atual.direita is not None:
            self.comparacoes += 1
            pai = atual
            atual = atual.direita
        # O nó mais à direita nunca tem filho direito:
        # basta o pai passar a apontar para o filho esquerdo dele.
        if pai is None:
            self._raiz = atual.esquerda
        else:
            pai.direita = atual.esquerda
        self._tamanho -= 1
        return atual.chamado

    def espiar(self):
        if self._raiz is None:
            return None
        atual = self._raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.chamado

    def __len__(self):
        return self._tamanho

    def altura(self):
        """Altura da árvore (calculada nível a nível, sem recursão)."""
        if self._raiz is None:
            return 0
        altura, nivel = 0, [self._raiz]
        while nivel:
            altura += 1
            nivel = [f for no in nivel for f in (no.esquerda, no.direita) if f]
        return altura

    def desenhar(self):
        """Árvore deitada: a raiz fica à esquerda e o lado DIREITO aparece em cima."""
        if self._raiz is None:
            return "  (árvore vazia)"
        linhas = []
        pilha = [(self._raiz, 0, False)]
        while pilha:
            no, prof, visitado = pilha.pop()
            if no is None:
                continue
            if visitado:
                linhas.append("  " + "      " * prof + f"[{no.chamado.prioridade}]#{no.chamado.id}")
            else:
                # Ordem invertida (direita, nó, esquerda) para o maior ficar no topo.
                pilha.append((no.esquerda, prof + 1, False))
                pilha.append((no, prof, True))
                pilha.append((no.direita, prof + 1, False))
        linhas.append(f"  (altura da árvore: {self.altura()})")
        return "\n".join(linhas)
