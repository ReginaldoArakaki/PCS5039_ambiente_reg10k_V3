"""Cenários do aprendizado do gêmeo (v3dt.1): S01–S05, na Casa B com a família.

Uso, na raiz do repositório da V3:  python tools/cenarios_v3dt1.py
O protocolo de semanas (14 dias de treino + 7 de teste) não é cenário do catálogo:
    python nucleo/reg10k.py aprendizado --sementes 10
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INV = {"id": "INV", "nivel": "REQUISITO", "dado": "qualquer controlador", "quando": "o cenário termina",
       "entao": {"tipo": "invariantes"}}
BASE = {"versao": "v3dt.1", "ambiente": "casa-b-familia", "modo": "IDEAL", "tipo": "APRENDIZADO", "falhas": []}
SALA = [6.0, 2.6]
SUG_SALA = {"id": "SUG-sala-20-23", "comodo": "sala", "de": "20:00", "ate": "23:00", "t_apagamento_ms": 300_000,
            "evidencia": {"dias": 14, "apagamentos": 412, "reacoes": 409, "imoveis": 0},
            "motivo": "em 409 de 412 apagamentos com alguém dentro, houve movimento logo depois: alguém parado e acordado ficou no escuro",
            "efeito": "menos apagamentos com gente acordada; mais tempo aceso depois que o cômodo esvazia"}


def a(t, quem, acao, **kw):
    return {"t_ms": t, "ocupante": quem, "acao": acao, **kw}


def r(id_, n, dado, quando, entao):
    return {"id": id_, "nivel": n, "dado": dado, "quando": quando, "entao": entao}


def leitura(extra=()):
    return [a(1_000, "idoso", "ANDAR", ate=SALA), a(6_000, "idoso", "LER"), *extra]


INI_SALA = {"ocupantes_na_sala": [{"id": "idoso", "comodo": "sala", "pos": SALA}], "luz": "APAGADA"}
REQ_SUG = ["RF-SYN-06", "RNF-PRI-01"]
REG_SUG = ["RN-V3-01", "RN-V3-02", "RN-V3-03", "RN-DT-07"]

CENARIOS = [
    ({**BASE, "id": "S01", "titulo": "Leitura na sala, sem faixa", "duracao_ms": 1_200_000, "hora_inicio": "20:00",
      "estado_inicial": INI_SALA,
      "descricao": "O idoso lê na sala às 20h, parado. Sem aprendizado, vale o T_apagamento de 60 s: a luz apaga e ele acena para acender de novo.",
      "comportamento_ideal": "A luz fica acesa enquanto alguém lê.",
      "comportamento_referencia": "Apaga cerca de 60 s depois do último movimento; o leitor acena em 3 a 10 s e a luz volta. É o padrão que o gêmeo aprende.",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-I0-03", "RN-V3-01"],
      "acoes": leitura()},
     [r("A1", "CARACTERIZACAO", "leitor parado e acordado", "passa o T_apagamento de 60 s",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "min": 12}),
      r("A2", "CARACTERIZACAO", "leitor reage ao escuro", "o cenário termina",
        {"tipo": "metrica", "comodo": "sala", "nome": "escuro_com_ocupante_s", "min": 60})]),

    ({**BASE, "id": "S02", "titulo": "Sugestão aceita: sala das 20h às 23h com 5 min", "duracao_ms": 1_200_000,
      "hora_inicio": "20:00", "estado_inicial": INI_SALA, "sugestoes": [SUG_SALA],
      "descricao": "Mesma leitura do S01. O gêmeo sugeriu T_apagamento de 5 min na sala das 20h às 23h; o titular aceita no app em 1 min.",
      "comportamento_ideal": "Depois do aceite, a luz fica acesa durante a leitura.",
      "comportamento_referencia": "Aceite → versão pendente → hub aplica a faixa (CONFIG_APLICADA e FAIXA_APLICADA). A luz passa a apagar só depois de 5 min parado.",
      "requisitos": REQ_SUG, "regras": REG_SUG,
      "acoes": leitura([a(60_000, "app", "APP_ACEITAR", sugestoes=["SUG-sala-20-23"])])},
     [r("A1", "REQUISITO", "faixa aceita em 1 min", "o leitor fica parado quase 5 min",
        {"tipo": "luz_constante", "comodo": "sala", "valor": "ACESA", "entre_ms": [70_000, 300_000]}),
      r("A2", "CARACTERIZACAO", "faixa de 5 min", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "max": 5})]),

    ({**BASE, "id": "S03", "titulo": "Sugestão recusada", "duracao_ms": 1_200_000, "hora_inicio": "20:00",
      "estado_inicial": INI_SALA, "sugestoes": [SUG_SALA],
      "descricao": "Mesma leitura e mesma sugestão do S02, mas o titular recusa no app.",
      "comportamento_ideal": "A recusa é registrada e nada muda na casa.",
      "comportamento_referencia": "Nenhuma versão de configuração é criada; o comportamento é o do S01.",
      "requisitos": REQ_SUG, "regras": REG_SUG,
      "acoes": leitura([a(60_000, "app", "APP_RECUSAR", sugestoes=["SUG-sala-20-23"])])},
     [r("A1", "REQUISITO", "sugestão recusada", "passa o T_apagamento de 60 s",
        {"tipo": "luz", "comodo": "sala", "valor": "APAGADA", "desde_ms": 140_000, "ate_ms": 400_000}),
      r("A2", "CARACTERIZACAO", "nada muda", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "min": 12})]),

    ({**BASE, "id": "S04", "titulo": "Quarto à noite com a faixa curta já aceita", "duracao_ms": 1_200_000,
      "hora_inicio": "22:50",
      "config_inicial": {"versao": 2, "faixas": {"quarto": [{"de": "23:00", "ate": "06:00", "t_apagamento_ms": 30_000}]},
                         "sugestoes_aceitas": ["SUG-quarto-23-06"]},
      "estado_inicial": {"ocupantes_na_sala": [{"id": "morador", "comodo": "quarto", "pos": [7.5, 6.8]},
                                               {"id": "moradora", "comodo": "quarto", "pos": [6.0, 6.8]}], "luz": "APAGADA"},
      "descricao": "O casal no quarto: o morador dorme; a moradora lê até 22h55 e dorme. Em dias anteriores, o titular aceitou T_apagamento de 30 s no quarto das 23h às 6h.",
      "comportamento_ideal": "Luz acesa enquanto ela lê; apagada logo que os dois dormem.",
      "comportamento_referencia": "Antes das 23h vale 60 s; às 23h o hub troca para 30 s (FAIXA_APLICADA). Com os dois dormindo, a luz apaga 30 s depois do último movimento.",
      "requisitos": ["RF-OPR-01", "RN-V1-05"], "regras": ["RN-V3-03", "RN-V1-05", "RN-DT-07"],
      "acoes": [a(1_000, "morador", "DORMIR"), a(2_000, "moradora", "LER"),
                a(900_000, "moradora", "GESTO"), a(902_000, "moradora", "DORMIR")]},
     [r("A1", "REQUISITO", "os dois dormindo, depois das 23h", "passa o T_apagamento da faixa (30 s)",
        {"tipo": "luz", "comodo": "quarto", "valor": "APAGADA", "apos": {"evento": "ADORMECEU", "ocupante": "moradora"},
         "ate_ms": 40_000}),
      r("A2", "CARACTERIZACAO", "faixa curta", "o cenário termina",
        {"tipo": "metrica", "nome": "luz_com_todos_dormindo_s", "max": 40})]),

    ({**BASE, "id": "S05", "titulo": "Aceite com o canal fora", "duracao_ms": 900_000, "hora_inicio": "20:00",
      "estado_inicial": INI_SALA, "sugestoes": [SUG_SALA],
      "falhas": [{"t_ms": 30_000, "tipo": "CANAL_DESCONECTA", "duracao_ms": 300_000}],
      "descricao": "O titular aceita a sugestão da sala com o canal entre hub e plataforma fora por 5 min.",
      "comportamento_ideal": "O aceite vira versão pendente; o hub só a aplica quando a sessão volta.",
      "comportamento_referencia": "A versão fica PENDENTE e é distribuída na reconexão (RF-SYN-06); até lá, vale 60 s.",
      "requisitos": REQ_SUG + ["RF-SYN-03"], "regras": REG_SUG,
      "acoes": leitura([a(60_000, "app", "APP_ACEITAR", sugestoes=["SUG-sala-20-23"])])},
     [r("A1", "REQUISITO", "canal fora", "antes da reconexão vale 60 s",
        {"tipo": "luz", "comodo": "sala", "valor": "APAGADA", "desde_ms": 140_000, "ate_ms": 300_000}),
      r("A2", "REQUISITO", "canal volta", "o hub aplica a faixa",
        {"tipo": "luz_constante", "comodo": "sala", "valor": "ACESA", "entre_ms": [340_000, 600_000]})]),
]
FAMILIAS = {}


def main() -> int:
    for rot, asserc in CENARIOS:
        rot = {**rot, "acoes": sorted(rot["acoes"], key=lambda x: x["t_ms"])}
        for sub, doc in (("roteiros", rot), ("esperado", {"cenario": rot["id"], "modo": "IDEAL", "semente_referencia": 42,
                                                          "requisitos": rot["requisitos"], "assercoes": asserc + [INV]})):
            p = RAIZ / "cenarios" / sub / f"{rot['id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(CENARIOS)} cenários do aprendizado gravados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
