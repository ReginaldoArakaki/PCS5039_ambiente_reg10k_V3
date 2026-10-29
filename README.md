# Reg10k — versão V3: Casa B, sete cômodos, com gêmeo digital e espelho

Repositório de versão do ambiente de simulação Reg10k (PCS5039, EPUSP).
Linha de pesquisa: Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP.

O código (motor, hub, plataforma, oráculo, página) fica no **núcleo**, na subpasta `nucleo/`,
fixado numa tag (`nucleo-v1.3`). Esta pasta guarda só o que é da versão:

| Pasta | Conteúdo |
|---|---|
| `ambiente/` | Planta: `casa-b.json`. É a Casa A deslocada 3,5 m, mais quarto 2, quarto 3 e área de serviço (7 cômodos). Banheiro com T_apagamento de 5 min |
| `cenarios/` | Roteiros e resultados esperados: 56 cenários gerados por planta (G*, famílias F1–F9) e 4 próprios da Casa B (C01–C04) |
| `alunos/` | Controladores dos alunos (um pacote por grupo) |
| `experimentos/familias.json` | Famílias do protocolo de experimentos e os cenários de cada uma |
| `dados/` | CSV dos experimentos, manifestos e assinaturas de regressão |
| `tools/cenarios_v3dt.py` | Gera os cenários C01–C04. Os G* vêm de `python nucleo/reg10k.py gerador --ambiente casa-b --versao v3dt` |
| `docs/` | Plano da V3 (v3dt e v3dt.1) |
| `site/` | Página gerada |

Cenários próprios da Casa B:

| ID | O que testa | Família |
|---|---|---|
| C01 | Travessia até o quarto 3, que fica a duas passagens internas da sala | F1 |
| C02 | Pessoa parada 6 min na área de serviço, esperando a máquina (limitação conhecida, como o FN01) | F2 |
| C03 | Dois quartos ocupados, longe um do outro, enquanto os cômodos de passagem apagam | F8 |
| C04 | Desconexão de 10 min com o quarto 3 e a área de serviço ocupados | F5 |

## Como usar

```
git clone --recurse-submodules <endereço deste repositório>
cd <pasta>
pip install -r nucleo/requirements.txt
python nucleo/reg10k.py catalogo            # catálogo e site/index.html
python nucleo/reg10k.py sim --cenario C01
python nucleo/reg10k.py experimentos --sementes 30
```

Para trocar a versão do núcleo, rode `cd nucleo && git fetch --tags && git checkout <tag>`, depois
`cd ..`, `git add nucleo` e um commit. Dados de artigo só são gerados com o núcleo numa tag
(o manifesto registra o commit).

Exercícios da versão: E13 (parâmetros por cômodo) e E14, no roteiro dos alunos do núcleo (`nucleo/docs/roteiro-alunos.md`).
O E15 (aprendizado do gêmeo) entra na v3dt.1.

Resultados de simulação, não de medição.

Licenças: código MIT (`LICENSE`); dados e documentos CC BY 4.0 (`LICENSE-dados.md`).
