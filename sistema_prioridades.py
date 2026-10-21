"""
Sistema de Distribuição de Chamados Técnicos por Prioridade.

A central usa o MAX-HEAP como estrutura principal. A lista encadeada e a
árvore binária de busca recebem os mesmos chamados em paralelo, só para
comparação durante a demonstração.

Uso:
    python sistema_prioridades.py              -> menu interativo
    python sistema_prioridades.py --benchmark  -> só o benchmark
"""

import itertools
import sys

from benchmark import executar_benchmark, executar_crescimento
from chamado import NIVEIS, Chamado
from estruturas import GerenciadorBST, GerenciadorHeap, GerenciadorListaEncadeada

EXEMPLOS = [
    ("Impressora do RH sem toner", 1),
    ("Servidor de banco de dados fora do ar", 5),
    ("Usuário esqueceu a senha do e-mail", 2),
    ("VPN caindo para a equipe comercial", 4),
    ("Lentidão no sistema de vendas", 3),
]


class CentralDeChamados:

    def __init__(self):
        self.heap = GerenciadorHeap(registrar_passos=True)  # estrutura principal do sistema
        self.comparativas = {
            "Lista Encadeada": GerenciadorListaEncadeada(),
            "Árvore BST": GerenciadorBST(),
        }
        self._ids = itertools.count(1)

    def _todas(self):
        return [("Max-Heap", self.heap)] + list(self.comparativas.items())

    def abrir(self, descricao, prioridade):
        """Insere o chamado nas 3 EDs e devolve quantas comparações cada uma fez."""
        chamado = Chamado(next(self._ids), descricao, prioridade)
        custo = {}
        for nome, ed in self._todas():
            antes = ed.comparacoes
            ed.inserir(chamado)
            custo[nome] = ed.comparacoes - antes
        return chamado, custo

    def atender(self):
        """Remove o mais urgente. Quem decide é o heap; as outras EDs acompanham."""
        chamado = self.heap.remover_mais_urgente()
        for ed in self.comparativas.values():
            ed.remover_mais_urgente()
        return chamado


def ler_inteiro(mensagem, minimo=1):
    while True:
        valor = input(mensagem).strip()
        if valor.lstrip("-").isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"  Digite um número inteiro maior ou igual a {minimo}.")


def mostrar_passos(heap):
    if heap.ultimos_passos:
        print("  Reorganização do heap:")
        for passo in heap.ultimos_passos:
            print(f"    - {passo}")
    else:
        print("  Reorganização do heap: nenhuma troca foi necessária.")


def menu():
    central = CentralDeChamados()
    for descricao, prioridade in EXEMPLOS:
        central.abrir(descricao, prioridade)

    while True:
        topo = central.heap.espiar()
        print("\n" + "=" * 60)
        print(" CENTRAL DE CHAMADOS TÉCNICOS - estrutura principal: MAX-HEAP")
        print("=" * 60)
        print(f" Chamados na fila: {len(central.heap)}")
        print(f" Próximo a ser atendido: {topo if topo else '-'}")
        print("-" * 60)
        print(" 1. Abrir novo chamado")
        print(" 2. Atender o chamado mais urgente")
        print(" 3. Ver a fila em ordem de atendimento")
        print(" 4. Ver as 3 estruturas por dentro")
        print(" 5. Rodar benchmark de estresse")
        print(" 0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            descricao = input("Descrição do problema: ").strip() or "Sem descrição"
            print("  Prioridades: " + ", ".join(f"{k} = {v}" for k, v in NIVEIS.items()))
            prioridade = ler_inteiro("Prioridade: ")
            chamado, custo = central.abrir(descricao, prioridade)
            print(f"\n  Chamado aberto: {chamado}")
            mostrar_passos(central.heap)
            print("  Comparações feitas para inserir: "
                  + " | ".join(f"{nome}: {qtd}" for nome, qtd in custo.items()))

        elif opcao == "2":
            chamado = central.atender()
            if chamado is None:
                print("\n  Nenhum chamado na fila.")
            else:
                print(f"\n  RESOLVIDO: {chamado}")
                mostrar_passos(central.heap)

        elif opcao == "3":
            fila = central.heap.listar()
            if not fila:
                print("\n  Fila vazia.")
            for posicao, c in enumerate(fila, 1):
                print(f"  {posicao:>3}º  {c}")

        elif opcao == "4":
            print("\n[ MAX-HEAP ]  (o mais urgente fica na posição 0)")
            print(central.heap.desenhar())
            print("\n[ LISTA ENCADEADA ORDENADA ]  (o mais urgente fica na cabeça)")
            print(central.comparativas["Lista Encadeada"].desenhar())
            print("\n[ ÁRVORE BINÁRIA DE BUSCA ]  (deitada: o mais urgente é o nó mais alto à direita)")
            print(central.comparativas["Árvore BST"].desenhar())

        elif opcao == "5":
            quantidade = input("Quantidade de chamados [10000]: ").strip()
            n = int(quantidade) if quantidade.isdigit() and int(quantidade) > 0 else 10_000
            executar_benchmark(n)

        elif opcao == "0":
            print("Encerrando.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    # Garante que os acentos apareçam certo no terminal do Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    if "--benchmark" in sys.argv:
        executar_benchmark()
        executar_crescimento()
    else:
        menu()
