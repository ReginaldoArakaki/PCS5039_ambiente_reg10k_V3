"""Cenários próprios da Casa B (v3dt): C01–C04, com asserções de janela relativa.

Uso, na raiz do repositório da V3:  python tools/cenarios_v3dt.py
Os cenários das famílias F1–F9 (G*) vêm do gerador do núcleo:
    python nucleo/reg10k.py gerador --ambiente casa-b --versao v3dt
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRA = {"evento": "CRUZOU_PORTA", "sentido": "ENTRADA"}
INV = {"id": "INV", "nivel": "REQUISITO", "dado": "qualquer controlador", "quando": "o cenário termina",
       "entao": {"tipo": "invariantes"}}
BASE = {"versao": "v3dt", "ambiente": "casa-b", "modo": "IDEAL",
        "estado_inicial": {"ocupantes_na_sala": [], "luz": "APAGADA"}, "falhas": []}
PORTA = [4.45, 1.0]


def a(t, quem, acao, **kw):
    return {"t_ms": t, "ocupante": quem, "acao": acao, **kw}


def r(id_, n, dado, quando, entao):
    return {"id": id_, "nivel": n, "dado": dado, "quando": quando, "entao": entao}


def acende(i, comodo, nome):
    return r(f"L{i}", "REQUISITO", f"{nome} escuro", "o morador entra",
             {"tipo": "luz", "comodo": comodo, "valor": "ACESA", "apos": ENTRA, "ate_ms": 1_000})


CENARIOS = [
    ({**BASE, "id": "C01", "titulo": "Travessia até o quarto 3", "tipo": "NORMAL", "duracao_ms": 480_000,
      "descricao": "O morador entra e vai ao quarto 3 passando pela sala e pelo quarto (duas passagens internas); fica 1 min e volta para a rua.",
      "comportamento_ideal": "Cada cômodo acende ao ser atravessado e apaga depois.",
      "comportamento_referencia": "Acende em até 1 s a cada passagem; cada cômodo apaga 60 s depois da última evidência.",
      "requisitos": ["RF-OPR-01", "RNF-DES-03"], "regras": ["RN-I0-02", "RN-V2-02"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(9_000, "morador", "MUDAR_COMODO", para="quarto"),
                a(21_000, "morador", "MUDAR_COMODO", para="quartotres"),
                a(33_000, "morador", "ANDAR_ALEATORIO", duracao_ms=60_000),
                a(95_000, "morador", "MUDAR_COMODO", para="quarto"), a(107_000, "morador", "MUDAR_COMODO", para="sala"),
                a(119_000, "morador", "ANDAR", ate=PORTA), a(127_000, "morador", "SAIR")]},
     [acende(1, "sala", "sala"), acende(2, "quarto", "quarto"), acende(3, "quartotres", "quarto 3"),
      r("A1", "REQUISITO", "entrada em cômodo escuro", "a lâmpada acende",
        {"tipo": "metrica", "nome": "atraso_percebido_ms_max", "max": 1_000}),
      r("A2", "REQUISITO", "casa vazia", "depois da saída", {"tipo": "luz", "comodo": "quartotres", "valor": "APAGADA",
                                                            "em_ms": 127_000 + 120_000})]),

    ({**BASE, "id": "C02", "titulo": "Esperando a máquina na área de serviço", "tipo": "FALSO_NEGATIVO", "duracao_ms": 720_000,
      "descricao": "O morador vai à área de serviço (sala → cozinha → área), fica parado 6 min esperando a máquina de lavar, mexe-se, volta e sai.",
      "comportamento_ideal": "A luz da área de serviço fica acesa enquanto ele espera.",
      "comportamento_referencia": "Limitação conhecida (como o FN01): apaga 60 s depois do último movimento; acende de novo quando ele se mexe.",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-I0-03"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(9_000, "morador", "MUDAR_COMODO", para="cozinha"),
                a(21_000, "morador", "MUDAR_COMODO", para="servico"), a(33_000, "morador", "ANDAR", ate=[13.5, 3.0]),
                a(40_000, "morador", "PARADO"), a(400_000, "morador", "GESTO"),
                a(402_000, "morador", "ANDAR_ALEATORIO", duracao_ms=20_000),
                a(425_000, "morador", "MUDAR_COMODO", para="cozinha"), a(437_000, "morador", "MUDAR_COMODO", para="sala"),
                a(449_000, "morador", "ANDAR", ate=PORTA), a(457_000, "morador", "SAIR")]},
     [acende(1, "servico", "área de serviço"),
      r("A1", "REQUISITO", "morador se mexe depois de esperar", "o SP vê o movimento",
        {"tipo": "luz", "comodo": "servico", "valor": "ACESA", "desde_ms": 400_000, "ate_ms": 402_000}),
      r("A2", "CARACTERIZACAO", "morador parado e acordado", "60 s sem movimento",
        {"tipo": "metrica", "comodo": "servico", "nome": "escuro_com_ocupante_s", "min": 200})]),

    ({**BASE, "id": "C03", "titulo": "Dois quartos ocupados, longe um do outro", "tipo": "NORMAL", "duracao_ms": 600_000,
      "descricao": "O morador vai ao quarto 3 e o Rex ao quarto 2; os dois andam pelos quartos; os outros cômodos ficam vazios.",
      "comportamento_ideal": "Só os dois quartos ficam acesos; os cômodos de passagem apagam.",
      "comportamento_referencia": "Os cômodos de passagem acendem pelo SA e apagam 60 s depois; os quartos ficam acesos.",
      "requisitos": ["RF-OPR-01", "RN34"], "regras": ["RN-V1-02", "RN-I0-03"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(7_000, "rex", "ENTRAR"),
                a(10_000, "morador", "MUDAR_COMODO", para="quarto"), a(12_000, "rex", "MUDAR_COMODO", para="quartodois"),
                a(22_000, "morador", "MUDAR_COMODO", para="quartotres"),
                a(26_000, "rex", "ANDAR_ALEATORIO", duracao_ms=574_000), a(36_000, "morador", "ANDAR_ALEATORIO", duracao_ms=564_000)]},
     [r("A1", "REQUISITO", "morador no quarto 3", "o cenário corre",
        {"tipo": "luz_constante", "comodo": "quartotres", "valor": "ACESA", "entre_ms": [40_000, 600_000]}),
      r("A2", "REQUISITO", "Rex no quarto 2", "o cenário corre",
        {"tipo": "luz_constante", "comodo": "quartodois", "valor": "ACESA", "entre_ms": [30_000, 600_000]}),
      r("A3", "REQUISITO", "sala de passagem vazia", "passa o T_apagamento",
        {"tipo": "luz", "comodo": "sala", "valor": "APAGADA", "em_ms": 180_000}),
      r("A4", "REQUISITO", "ocupantes sempre se movendo", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "igual": 0})]),

    ({**BASE, "id": "C04", "titulo": "Desconexão com a casa ocupada nas pontas", "tipo": "GEMEO_DIGITAL", "duracao_ms": 780_000,
      "descricao": "O morador está no quarto 3 e o Rex na área de serviço quando o canal cai por 10 min.",
      "comportamento_ideal": "A automação local segue; o gêmeo de cada cômodo se declara desatualizado e reconcilia ao voltar.",
      "comportamento_referencia": "Fila persistente, um estado por cômodo, reconciliação em até 5 s.",
      "requisitos": ["RF-SYN-03", "RF-SYN-04", "RNF-CON-01", "CF06"], "regras": ["RN-DT-03", "RN-DT-04", "RN-V1-04"],
      "falhas": [{"t_ms": 90_000, "tipo": "CANAL_DESCONECTA", "duracao_ms": 600_000}],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(7_000, "rex", "ENTRAR"),
                a(10_000, "morador", "MUDAR_COMODO", para="quarto"), a(12_000, "rex", "MUDAR_COMODO", para="cozinha"),
                a(22_000, "morador", "MUDAR_COMODO", para="quartotres"), a(24_000, "rex", "MUDAR_COMODO", para="servico"),
                a(36_000, "morador", "ANDAR_ALEATORIO", duracao_ms=744_000), a(38_000, "rex", "ANDAR_ALEATORIO", duracao_ms=742_000)]},
     [r("A1", "REQUISITO", "canal caído", "logo depois da queda",
        {"tipo": "gemeo", "comodo": "quartotres", "em_ms": 91_000, "atualidade": "DESATUALIZADO", "conexao": "DESCONECTADO"}),
      r("A2", "REQUISITO", "canal volta", "o hub reconcilia", {"tipo": "metrica", "nome": "reconciliacao_ms_max", "max": 5_000}),
      r("A3", "REQUISITO", "fila persistente", "o cenário termina", {"tipo": "metrica", "nome": "eventos_nao_entregues", "igual": 0}),
      r("A4", "REQUISITO", "ocupantes se movendo", "o cenário termina",
        {"tipo": "metrica", "nome": "apagamentos_indevidos", "igual": 0})]),
]
FAMILIAS = {"C01": "F1", "C02": "F2", "C03": "F8", "C04": "F5"}


def main() -> int:
    for rot, asserc in CENARIOS:
        rot = {**rot, "acoes": sorted(rot["acoes"], key=lambda x: x["t_ms"])}
        for sub, doc in (("roteiros", rot), ("esperado", {"cenario": rot["id"], "modo": "IDEAL", "semente_referencia": 42,
                                                          "requisitos": rot["requisitos"], "assercoes": asserc + [INV]})):
            p = RAIZ / "cenarios" / sub / f"{rot['id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fp = RAIZ / "experimentos" / "familias.json"
    fam = json.loads(fp.read_text(encoding="utf-8"))
    for cid, f in FAMILIAS.items():
        fam["familias"][f] = sorted(set(fam["familias"].get(f, [])) | {cid})
    fp.write_text(json.dumps(fam, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(CENARIOS)} cenários próprios gravados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
