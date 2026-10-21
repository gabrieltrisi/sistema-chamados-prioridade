import random
import unittest

from chamado import Chamado
from estruturas import (
    GerenciadorBST,
    GerenciadorHeap,
    GerenciadorHeapq,
    GerenciadorListaEncadeada,
)


class TestGerenciadorHeap(unittest.TestCase):

    def setUp(self):
        self.fila = GerenciadorHeap()

    def assert_propriedade_de_heap(self):
        """Todo pai deve ter prioridade maior ou igual à dos filhos."""
        dados = self.fila._dados
        for i in range(1, len(dados)):
            pai = (i - 1) // 2
            self.assertGreaterEqual(dados[pai][0], dados[i][0])

    def test_fila_vazia(self):
        self.assertEqual(len(self.fila), 0)
        self.assertIsNone(self.fila.remover_mais_urgente())
        self.assertIsNone(self.fila.espiar())

    def test_insercao_aumenta_tamanho(self):
        for i in range(5):
            self.fila.inserir(Chamado(i, "x", i))
        self.assertEqual(len(self.fila), 5)

    def test_maior_prioridade_sai_primeiro(self):
        self.fila.inserir(Chamado(1, "Impressora", 1))
        self.fila.inserir(Chamado(2, "Servidor caiu", 5))
        self.fila.inserir(Chamado(3, "Senha", 2))

        self.assertEqual(self.fila.remover_mais_urgente().id, 2)
        self.assertEqual(self.fila.remover_mais_urgente().id, 3)
        self.assertEqual(self.fila.remover_mais_urgente().id, 1)
        self.assertEqual(len(self.fila), 0)

    def test_maior_fica_na_posicao_zero(self):
        for i, p in enumerate([2, 7, 1, 9, 4]):
            self.fila.inserir(Chamado(i, "x", p))
        self.assertEqual(self.fila._dados[0][0], 9)

    def test_espiar_nao_remove(self):
        self.fila.inserir(Chamado(1, "a", 3))
        self.fila.inserir(Chamado(2, "b", 9))
        self.assertEqual(self.fila.espiar().id, 2)
        self.assertEqual(len(self.fila), 2)

    def test_empate_respeita_ordem_de_chegada(self):
        for i in range(1, 6):
            self.fila.inserir(Chamado(i, "mesma prioridade", 3))
        ids = [self.fila.remover_mais_urgente().id for _ in range(5)]
        self.assertEqual(ids, [1, 2, 3, 4, 5])

    def test_propriedade_de_heap_mantida_em_toda_operacao(self):
        rng = random.Random(1)
        for i in range(300):
            self.fila.inserir(Chamado(i, "x", rng.randint(1, 50)))
            self.assert_propriedade_de_heap()
        for _ in range(150):
            self.fila.remover_mais_urgente()
            self.assert_propriedade_de_heap()

    def test_maior_sempre_sai_primeiro_com_dados_aleatorios(self):
        rng = random.Random(123)
        for i in range(2000):
            self.fila.inserir(Chamado(i, "aleatorio", rng.randint(1, 100)))

        anterior = float("inf")
        while len(self.fila):
            atual = self.fila.remover_mais_urgente().prioridade
            self.assertLessEqual(atual, anterior)
            anterior = atual

    def test_insercao_intercalada_com_remocao(self):
        self.fila.inserir(Chamado(1, "a", 2))
        self.fila.inserir(Chamado(2, "b", 4))
        self.assertEqual(self.fila.remover_mais_urgente().id, 2)

        self.fila.inserir(Chamado(3, "c", 10))
        self.fila.inserir(Chamado(4, "d", 1))
        self.assertEqual(self.fila.remover_mais_urgente().id, 3)
        self.assertEqual(self.fila.remover_mais_urgente().id, 1)
        self.assertEqual(self.fila.remover_mais_urgente().id, 4)

    def test_listar_nao_altera_fila(self):
        for i, p in enumerate([3, 1, 5, 2]):
            self.fila.inserir(Chamado(i, "x", p))
        self.assertEqual([c.prioridade for c in self.fila.listar()], [5, 3, 2, 1])
        self.assertEqual(len(self.fila), 4)

    def test_insercao_custa_no_maximo_log_n_comparacoes(self):
        # Inserir em ordem crescente é o pior caso: cada novo item sobe até a raiz.
        for i in range(1, 1025):
            antes = self.fila.comparacoes
            self.fila.inserir(Chamado(i, "x", i))
            self.assertLessEqual(self.fila.comparacoes - antes, 10)  # log2(1024) = 10


class TestEstruturasComparativas(unittest.TestCase):
    """A lista e a árvore também precisam atender na ordem correta."""

    def ordem_de_atendimento(self, classe, chamados):
        ed = classe()
        for c in chamados:
            ed.inserir(c)
        return [ed.remover_mais_urgente().id for _ in range(len(chamados))]

    def test_lista_encadeada_maior_primeiro_e_fifo(self):
        chamados = [Chamado(1, "a", 2), Chamado(2, "b", 5), Chamado(3, "c", 2), Chamado(4, "d", 5)]
        self.assertEqual(self.ordem_de_atendimento(GerenciadorListaEncadeada, chamados), [2, 4, 1, 3])

    def test_bst_maior_primeiro_e_fifo(self):
        chamados = [Chamado(1, "a", 2), Chamado(2, "b", 5), Chamado(3, "c", 2), Chamado(4, "d", 5)]
        self.assertEqual(self.ordem_de_atendimento(GerenciadorBST, chamados), [2, 4, 1, 3])

    def test_estruturas_vazias(self):
        for classe in (GerenciadorListaEncadeada, GerenciadorBST, GerenciadorHeapq):
            self.assertIsNone(classe().remover_mais_urgente())

    def test_as_quatro_implementacoes_atendem_na_mesma_ordem(self):
        rng = random.Random(7)
        chamados = [Chamado(i, "x", rng.randint(1, 5)) for i in range(500)]

        referencia = self.ordem_de_atendimento(GerenciadorHeap, chamados)
        for classe in (GerenciadorListaEncadeada, GerenciadorBST, GerenciadorHeapq):
            self.assertEqual(self.ordem_de_atendimento(classe, chamados), referencia)


if __name__ == "__main__":
    unittest.main(verbosity=2)
