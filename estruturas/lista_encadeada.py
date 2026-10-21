"""
ED 2 — Lista Encadeada Ordenada

Cada nó aponta para o próximo. A lista é mantida SEMPRE ordenada da maior
para a menor prioridade, então o mais urgente fica na cabeça.

    Inserir:          O(n)  (percorre até achar a posição certa)
    Remover o máximo: O(1)  (retira a cabeça)
    Consultar o topo: O(1)
"""


class _No:
    __slots__ = ("chamado", "proximo")

    def __init__(self, chamado, proximo=None):
        self.chamado = chamado
        self.proximo = proximo


class GerenciadorListaEncadeada:

    def __init__(self):
        self._cabeca = None
        self._tamanho = 0
        self.comparacoes = 0

    def inserir(self, chamado):
        novo = _No(chamado)
        self.comparacoes += 1
        if self._cabeca is None or chamado.prioridade > self._cabeca.chamado.prioridade:
            novo.proximo = self._cabeca
            self._cabeca = novo
        else:
            # Anda até o último nó com prioridade >= à nova.
            # Assim o novo chamado fica DEPOIS dos de mesma prioridade (ordem de chegada).
            atual = self._cabeca
            while atual.proximo is not None:
                self.comparacoes += 1
                if atual.proximo.chamado.prioridade < chamado.prioridade:
                    break
                atual = atual.proximo
            novo.proximo = atual.proximo
            atual.proximo = novo
        self._tamanho += 1

    def remover_mais_urgente(self):
        if self._cabeca is None:
            return None
        no = self._cabeca
        self._cabeca = no.proximo
        self._tamanho -= 1
        return no.chamado

    def espiar(self):
        return self._cabeca.chamado if self._cabeca else None

    def __len__(self):
        return self._tamanho

    def desenhar(self):
        if self._cabeca is None:
            return "  (lista vazia)"
        partes = []
        atual = self._cabeca
        while atual is not None:
            partes.append(f"[{atual.chamado.prioridade}]#{atual.chamado.id}")
            atual = atual.proximo
        return "  cabeça -> " + " -> ".join(partes) + " -> None"
