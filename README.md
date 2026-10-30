# Reg10k — versão V3: Casa B, sete cômodos, com gêmeo digital e espelho

Repositório de versão do ambiente de simulação Reg10k (PCS5039, EPUSP).
Linha de pesquisa: Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP.

O código (motor, hub, plataforma, oráculo, página) fica no **núcleo**, na subpasta `nucleo/`,
fixado numa tag (`nucleo-v1.4` desde a v3dt.1; a v3dt foi feita no `nucleo-v1.3`). Esta pasta guarda só o que é da versão:

| Pasta | Conteúdo |
|---|---|
| `ambiente/` | Planta: `casa-b.json`. É a Casa A deslocada 3,5 m, mais quarto 2, quarto 3 e área de serviço (7 cômodos). Banheiro com T_apagamento de 5 min. Na v3dt.1, `casa-b-familia.json`: a mesma casa com morador, moradora, criança, idoso e o Rex |
| `cenarios/` | Roteiros e resultados esperados: 56 cenários gerados por planta (G*, famílias F1–F9), 4 próprios da Casa B (C01–C04) e 5 do aprendizado do gêmeo (S01–S05, v3dt.1) |
| `alunos/` | Controladores dos alunos (um pacote por grupo) |
| `experimentos/familias.json` | Famílias do protocolo de experimentos e os cenários de cada uma |
| `experimentos/rotina-familia.json` | Rotina da família das 17h à 1h, para o protocolo de semanas da v3dt.1 |
| `dados/` | CSV dos experimentos, manifestos e assinaturas de regressão |
| `tools/cenarios_v3dt.py` | Gera os cenários C01–C04. Os G* vêm de `python nucleo/reg10k.py gerador --ambiente casa-b --versao v3dt` |
| `tools/cenarios_v3dt1.py` | Gera os cenários S01–S05 (sugestão aceita, recusada, faixa já aceita, aceite com o canal fora) |
| `docs/` | Plano da V3, com a entrega da v3dt e da v3dt.1 |
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
python nucleo/reg10k.py aprendizado --sementes 10          # v3dt.1: 14 dias de treino + 7 de teste, aceitar × recusar
python nucleo/reg10k.py aprendizado --sementes 3 --politica comodos:sala,cozinha   # E15: a sua escolha de aceite
```

Para trocar a versão do núcleo, rode `cd nucleo && git fetch --tags && git checkout <tag>`, depois
`cd ..`, `git add nucleo` e um commit. Dados de artigo só são gerados com o núcleo numa tag
(o manifesto registra o commit).

Exercícios da versão: E13 (parâmetros por cômodo), E14 e E15 (o gêmeo que aprende e o titular que decide), no roteiro dos alunos do núcleo (`nucleo/docs/roteiro-alunos.md`).

Na v3dt.1, o gêmeo remoto aprende um perfil agregado por cômodo e hora (sem dado por ocupante, 30 dias) e sugere T_apagamento por faixa horária. Nada vale sem o aceite do titular no app (invariante OR-17). Resultado de 10 sementes: com o aceite, o tempo no escuro com alguém acordado cai 78%, e a luz acesa sem ninguém sobe 64% (`docs/ambiente-simulacao-v3dt.md`, §15).

Resultados de simulação, não de medição.

Licenças: código MIT (`LICENSE`); dados e documentos CC BY 4.0 (`LICENSE-dados.md`).
