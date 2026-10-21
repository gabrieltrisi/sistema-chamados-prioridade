from dataclasses import dataclass

NIVEIS = {1: "Baixa", 2: "Normal", 3: "Alta", 4: "Urgente", 5: "Crítica"}


@dataclass
class Chamado:
    """Um chamado técnico aberto na central de suporte.

    prioridade: quanto MAIOR o número, mais urgente o chamado.
    """

    id: int
    descricao: str
    prioridade: int

    def __str__(self):
        nivel = NIVEIS.get(self.prioridade)
        rotulo = f"{self.prioridade} - {nivel}" if nivel else str(self.prioridade)
        return f"#{self.id} [{rotulo}] {self.descricao}"
