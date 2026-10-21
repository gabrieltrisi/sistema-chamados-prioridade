"""
Benchmark: mede o custo de inserir N chamados e depois atender todos,
em cada uma das estruturas, com a MESMA lista de chamados.

Duas medidas:
    - tempo (segundos), que varia de computador para computador;
    - comparações entre prioridades, que NÃO depende do computador
      e mostra diretamente a complexidade de cada ED.
"""

import random
import time

from chamado import Chamado
from estruturas import (
    GerenciadorBST,
    GerenciadorHeap,
    GerenciadorHeapq,
    GerenciadorListaEncadeada,
)

ESTRUTURAS = [
    ("Max-Heap (implementação própria)", GerenciadorHeap),
    ("Lista Encadeada Ordenada", GerenciadorListaEncadeada),
    ("Árvore Binária de Busca", GerenciadorBST),
]

REFERENCIA = ("Max-Heap com heapq (referência em C)", GerenciadorHeapq)

CENARIOS = [
    ("Cenário A - prioridades espalhadas (1 a 1.000)", 1000),
    ("Cenário B - níveis reais de urgência (1 a 5)", 5),
]


def gerar_chamados(quantidade, prioridade_max, semente=42):
    rng = random.Random(semente)
    return [
        Chamado(i, f"Chamado gerado #{i}", rng.randint(1, prioridade_max))
        for i in range(1, quantidade + 1)
    ]


def medir(classe, chamados):
    gerenciador = classe()

    inicio = time.perf_counter()
    for c in chamados:
        gerenciador.inserir(c)
    tempo_insercao = time.perf_counter() - inicio

    ordem = []
    inicio = time.perf_counter()
    while len(gerenciador):
        ordem.append(gerenciador.remover_mais_urgente().id)
    tempo_remocao = time.perf_counter() - inicio

    return {
        "insercao": tempo_insercao,
        "remocao": tempo_remocao,
        "total": tempo_insercao + tempo_remocao,
        "comparacoes": getattr(gerenciador, "comparacoes", None),
        "ordem": ordem,
    }


def formatar_numero(valor):
    return f"{valor:,}".replace(",", ".")


def executar_benchmark(quantidade=10_000):
    linha = "=" * 92
    print(f"\n{linha}")
    print(f" BENCHMARK - {formatar_numero(quantidade)} chamados aleatórios: inserir todos e depois atender todos")
    print(linha)

    for titulo, prioridade_max in CENARIOS:
        chamados = gerar_chamados(quantidade, prioridade_max)
        print(f"\n{titulo}")
        print("-" * 92)
        print(f"{'Estrutura':<38}{'Inserção (s)':>13}{'Remoção (s)':>13}{'Total (s)':>11}{'vs Heap':>9}{'Comparações':>14}")
        print("-" * 92)

        resultados = [(nome, medir(classe, chamados)) for nome, classe in ESTRUTURAS + [REFERENCIA]]
        base = resultados[0][1]["total"]
        ordem_ok = all(r["ordem"] == resultados[0][1]["ordem"] for _, r in resultados)

        for nome, r in resultados:
            comps = formatar_numero(r["comparacoes"]) if r["comparacoes"] is not None else "-"
            fator = f"{r['total'] / base:.1f}x"
            print(f"{nome:<38}{r['insercao']:>13.4f}{r['remocao']:>13.4f}{r['total']:>11.4f}{fator:>9}{comps:>14}")

        principais = resultados[:3]
        vencedor = min(principais, key=lambda item: item[1]["total"])
        print("-" * 92)
        print(f"Mais rápida entre as 3 EDs: {vencedor[0]}")
        print(f"As estruturas atenderam os chamados na mesma ordem? {'SIM' if ordem_ok else 'NÃO'}")

    print(f"\n{linha}\n")


def executar_crescimento(tamanhos=(1_000, 2_500, 5_000, 10_000)):
    """Mostra como o número de comparações cresce com a quantidade de chamados (cenário B)."""
    print("\nCRESCIMENTO DAS COMPARAÇÕES - prioridades de 1 a 5")
    print(f"{'N':>8}" + "".join(f"{nome.split(' (')[0]:>28}" for nome, _ in ESTRUTURAS))
    for n in tamanhos:
        chamados = gerar_chamados(n, 5)
        comps = [medir(classe, chamados)["comparacoes"] for _, classe in ESTRUTURAS]
        print(f"{formatar_numero(n):>8}" + "".join(f"{formatar_numero(c):>28}" for c in comps))
    print()


if __name__ == "__main__":
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    executar_benchmark()
    executar_crescimento()
