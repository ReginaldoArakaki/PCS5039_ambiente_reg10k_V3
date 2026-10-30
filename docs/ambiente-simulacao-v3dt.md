# Ambiente de simulação Reg10k — V3: Casa B (7 cômodos) e aprendizado do gêmeo

**Versão do documento:** v04 | **Data:** 29/10/2026 | **Situação:** entregue: v3dt (§11 e §12) e v3dt.1 (§14 a §18)
**Responsável:** Reginaldo Arakaki (EPUSP)
**Disciplina:** PCS5039 — Engenharia de Software Orientada a IoT (EPUSP)
**Linha de pesquisa:** Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP
**Base:** núcleo `nucleo-v1.3`; V2 (`v2dta`) e V1 (`v1dt.1`); plano das versões paralelas v06 (§4, V3; DQ-PV-01); plano do ambiente v02 (§2.1: "Casa B e aprendizado do gêmeo — modelo comportamental; sugestões com aceite"; DI-09: sem hora do dia até aqui); v0dt (DT-03 e E10: aprendizado mínimo como exercício); V1 Business Drivers v02 (§ privacidade: presença é dado pessoal comportamental); V2/V3 v05 (§2.8: dado comportamental, detalhe retido 30 dias; RN-DT-07: preferência versionada)

| Versão | Data | Mudança |
|---|---|---|
| v01 | 29/10/2026 | Plano para aprovação, com a rodada de dúvidas (§10) |
| v02 | 29/10/2026 | Propostas DQ3-01 a DQ3-10 aceitas; entrega da v3dt (§11) e comparação V0–V3 no mesmo núcleo (§12) |
| v03 | 29/10/2026 | Entrega da v3dt.1 (§14 a §18): núcleo `nucleo-v1.4`, cenários S01–S05, protocolo de 21 dias com 10 sementes, achados RS-10 a RS-13, ajustes ◆ |
| v04 | 29/10/2026 | RS-11 (§16): política seletiva medida (sala, cozinha, quarto 3), substituindo a estimativa |

---

## 1. Objetivo e divisão proposta

A trilha previa para a V3 duas coisas ao mesmo tempo: uma casa maior (Casa B, 7 cômodos) e o aprendizado do gêmeo (modelo de comportamento e sugestões com aceite). São **duas variáveis**. Pelo princípio P1 (uma variável por vez), a proposta (DQ3-01) é dividir:

| Entrega | Muda | Moradores | Para quê |
|---|---|---|---|
| **v3dt** | Só o porte: Casa B | Morador e Rex, como V0–V2 | Fechar a série de portes (1, 2, 4 e 7 cômodos) com as mesmas famílias G*, comparável com V0–V2 |
| **v3dt.1** | Só o aprendizado do gêmeo | A família da v1dt.1 | Modelo de comportamento por cômodo e hora, sugestões ao titular, aplicação só depois do aceite |

As duas ficam no repositório novo `PCS5039_ambiente_reg10k_V3`.

## 2. v3dt: a Casa B

Proposta (DQ3-02): **Casa A + área de serviço + dois quartos**, sem corredor. A Casa A fica igual (como a V2 estendeu a V1), e os cômodos novos aumentam a profundidade da casa: quarto 3 fica a duas passagens internas da sala.

```
 y=7,5 ┌───────── 3,5 ──────┬──────────── 5,0 ───────────┬──────── 3,5 ────────┐
       │ Quarto 3           │ Quarto (suíte)             │ Banheiro            │
       │                PORTA-06 (SA-07)       PORTA-03 (SA-04)                 │
 y=4,0 ├────────────────────┼───▌PORTA-02 (SA-03)▐───────┼─────────────────────┼──────── 2,5 ──────┐
       │ Quarto 2       PORTA-05 (SA-06)  Sala (5 × 4)   VAO-01 (SA-02) Cozinha │ Área de serviço   │
       │                    │                            │          PORTA-04 (SA-05)                  │
 y=0   └────────────────────┴──▌PORTA-01 (SA-01)▐────────┴─────────────────────┴───────────────────┘
      x=0                x=3,5                         x=8,5                 x=12                x=14,5
```

| Item | Proposta |
|---|---|
| Cômodos (7) | Sala, cozinha, quarto (suíte), banheiro (os 4 da Casa A, deslocados 3,5 m para a direita), quarto 2, quarto 3, área de serviço |
| Passagens novas | PORTA-04 cozinha ↔ área de serviço; PORTA-05 sala ↔ quarto 2; PORTA-06 quarto ↔ quarto 3 |
| Parâmetros | Banheiro com T_apagamento de 5 min (como na V2); os demais, 60 s |
| Cenários | As famílias G* (F1–F9) geradas para a Casa B, mais 4 próprios: C01 travessia até o quarto 3 (duas passagens internas), C02 área de serviço com a máquina de lavar (pessoa parada vários minutos), C03 três quartos ocupados à noite, C04 desconexão com a casa toda ocupada |
| Comparação | V0–V3 com 1, 2, 4 e 7 cômodos, no mesmo núcleo, com o comparador normalizado por cômodo |

## 3. v3dt.1: o aprendizado do gêmeo

### 3.1 O que muda no modelo

| Item | Proposta | Base |
|---|---|---|
| **Hora do dia** | O roteiro passa a ter `hora_inicio` (por exemplo, 06:00) e um relógio de parede. Até aqui não havia hora do dia (DI-09) | DQ3-03 |
| **Quem aprende** | O **gêmeo remoto** (DTReg10k-R, na plataforma), a partir das evidências e estados que já recebe. O hub não aprende; só aplica o que o titular aceitou | DQ3-04 |
| **O que aprende** | Perfil de ocupação por **cômodo e faixa de 1 h**: fração do tempo ocupado, movimento e permanência parada. Nada por pessoa (os sensores não identificam, RN09) | DQ3-05; privacidade (V1) |
| **O que sugere** | T_apagamento por cômodo e faixa horária: por exemplo, curto no quarto à noite (quem dorme quer escuro, RN-V1-05) e longo na sala à tarde (quem lê parado). Cada sugestão traz a evidência e o efeito esperado | DQ3-05 |
| **Aceite** | Sugestão só vale depois do aceite do titular no app (ação nova `APP_ACEITAR` ou `APP_RECUSAR`); o aceite cria uma versão de configuração, pendente até o hub confirmar (RN-DT-07) | DQ3-07 |
| **Hub** | A configuração passa a aceitar T_apagamento por faixa horária, e o controlador usa o valor da faixa corrente | DQ3-07 |
| **Retenção** | O modelo guarda só o perfil agregado, com janela de 30 dias (V2/V3 §2.8) | DQ3-08 |
| **Invariante nova OR-17** | Nenhum parâmetro aprendido é aplicado sem aceite; recusa é registrada e respeitada; o modelo não guarda nada por ocupante | DQ3-07, DQ3-08 |

### 3.2 Como simular semanas

Medição em 29/10/2026: 1 hora simulada com duas pessoas leva 1,2 s e gera cerca de 12 mil eventos. Três semanas num só registro chegariam a uns 6 milhões de eventos em memória. Proposta (DQ3-06):

- **Rotina gerada dia a dia:** um gerador de rotina cria cada dia da família (acordar, sair, voltar, jantar, ler, dormir), com variação por semente. Por exemplo, o idoso lê na sala à tarde, e a criança dorme cedo.
- **O gêmeo carrega o modelo de um dia para o outro**, como faria a plataforma. Cada dia é uma execução separada, e a memória fica limitada a um dia.
- **Protocolo:** 14 dias de treino, sugestão e aceite simulado, e 7 dias de teste. Cerca de 10 min por semente e controlador; 10 sementes no lugar de 30.

### 3.3 Medidas

Antes × depois do aceite, por cômodo e faixa: escuro com ocupante acordado, luz com todos dormindo, desperdício, número de sugestões, aceites e recusas. É o experimento do artigo sobre o gêmeo: **o que o gêmeo aprende melhora a casa, e a que custo de privacidade?**

## 4. Regressão

| O quê | Garantia |
|---|---|
| Conjunto de regressão do núcleo | Assinaturas iguais às da `nucleo-v1.3` |
| V0, V1 e V2 | Ficam no seu núcleo até subirem; hora do dia e aprendizado são desligados por padrão (sem `hora_inicio`, nada muda) |
| Esperados existentes | Intocados |

## 5. Dentro × fora

| Dentro | Fora | Entra em |
|---|---|---|
| Casa B; hora do dia; perfil por cômodo e hora; sugestões com aceite; OR-17 | Luz natural (sensor de luminosidade) | A decidir |
| | Aprendizado por pessoa (identificação) | Fora do escopo (RN09) |
| | Várias residências e aprendizado entre casas | V4 |

## 6. Rastreabilidade e documentos da plataforma

O aprendizado com sugestão e aceite não está escrito na V1 nem na V2/V3: só a privacidade do dado comportamental (V1) e a preferência versionada (RN-DT-07). A v3dt.1 vai gerar:

- uma **pendência PD para a V1**: processo "sugerir ajuste com aceite do titular", com regra de minimização;
- os **refinamentos RS na V2/V3**, que vira a v06: requisito funcional de sugestão (SYN ou ACO), INV de aceite e classe `Sugestao` no modelo de informação.

## 7. Diferenças didáticas e exercício

- O aluno vê o gêmeo deixar de só espelhar e passar a **propor**, com o titular no controle.
- **E15 (novo).** Com a rotina de 14 dias, analisar o perfil aprendido, decidir quais sugestões aceitar e medir o efeito nos 7 dias de teste; discutir privacidade (o que o perfil revela da rotina da família). Pesos: análise 40%, decisão e medição 40%, discussão de privacidade 20%.

## 8. Critérios de pronto

| ID | Critério |
|---|---|
| CP-V3-01 | v3dt: famílias G* da Casa B aprovadas com a referência; comparação V0–V3 no mesmo núcleo |
| CP-V3-02 | v3dt.1: sem aceite, nada muda (assinaturas iguais); com aceite, a configuração por faixa é aplicada e a OR-17 é respeitada |
| CP-V3-03 | v3dt.1: 10 sementes de 21 dias, com o efeito antes × depois medido por cômodo e faixa |
| CP-V3-04 | Testes que fazem a OR-17 falhar quando deve (parâmetro aplicado sem aceite; dado por ocupante no modelo) |

## 9. Repositório

`PCS5039_ambiente_reg10k_V3` ainda não existe. Esta sessão não cria repositórios: crie-o vazio e público na conta **ReginaldoArakaki**, como a V0, a V1 e a V2. Com ele criado, eu o adiciono à sessão e publico a v3dt.

## 10. Rodada de dúvidas

| ID | Pergunta | Opções | Proposta |
|---|---|---|---|
| **DQ3-01** (bloqueante) | Dividir a V3? | (a) v3dt = Casa B, depois v3dt.1 = aprendizado; (b) as duas juntas | **(a)**: uma variável por vez; a Casa B fecha a série de portes comparável |
| **DQ3-02** (bloqueante) | Planta da Casa B | (a) Casa A + área de serviço + quarto 2 + quarto 3, sem corredor (§2); (b) com corredor; (c) outra sua | **(a)**: mantém a Casa A e aprofunda a casa (quarto 3 a duas passagens) |
| DQ3-03 | Hora do dia | Relógio de parede com `hora_inicio` no roteiro; ou continuar sem | Relógio, só quando o roteiro pedir (desligado por padrão) |
| DQ3-04 | Quem aprende | Gêmeo remoto (plataforma); hub; controlador | Gêmeo remoto: tem o histórico; o hub só aplica o aceito |
| DQ3-05 | O que aprende e sugere | Perfil por cômodo e hora → T_apagamento por faixa; ou mais (horário de acender) | T_apagamento por cômodo e faixa; acender por horário fica fora (não há luz natural) |
| DQ3-06 | Como simular semanas | Dia a dia com modelo persistente; ou um registro só | Dia a dia: 14 de treino + 7 de teste, 10 sementes |
| DQ3-07 | Aceite no app | Ações `APP_ACEITAR` / `APP_RECUSAR` por sugestão; ou aceite automático | Ações explícitas, que viram versão de configuração (RN-DT-07); OR-17 |
| DQ3-08 | Privacidade do modelo | Só agregado por cômodo e hora, 30 dias; ou guardar eventos | Só agregado, 30 dias (V2/V3 §2.8); a OR-17 verifica |
| DQ3-09 | Moradores | v3dt com morador e Rex; v3dt.1 com a família | Assim: a v3dt fica comparável com V0–V2, e a rotina da família dá o que aprender |
| DQ3-10 | Documentos da plataforma | PD para a V1 e V2/V3 v06 na v3dt.1; ou depois | Na v3dt.1, junto com a entrega |

Sem objeção, as propostas valem. **Aceitas em 29/10/2026.**

**Duração de referência:** v3dt, 1 dia; v3dt.1, 2 a 3 dias (núcleo `nucleo-v1.4` para o relógio e o aprendizado).

## 11. Entrega da v3dt

| Item | Situação |
|---|---|
| Planta | `ambiente/casa-b.json`: 7 cômodos e 7 passagens (SA-01 a SA-07), como no §2. Ids de cômodo `quartodois`, `quartotres` e `servico`, porque o esquema só aceita letras |
| Cenários G* | 56, gerados pelo núcleo: F1=7, F2=7, F3=6, F4=7, F5=1, F6=7, F7=7, F8=7, F9=7 |
| Cenários próprios | C01 travessia até o quarto 3 (F1); C02 área de serviço com a máquina (F2); C03 dois quartos ocupados longe um do outro (F8); C04 desconexão com a casa ocupada nas pontas (F5). As asserções de entrada usam janela relativa (`apos`) |
| Referência | Aprovada em todos os 60 cenários; invariantes respeitadas; execuções determinísticas |
| Regressão | 120 assinaturas em `dados/assinaturas-V3.json` |
| Dados | `dados/experimentos-V3-20261029.csv`: 3.600 execuções (60 cenários, referência e grupo_exemplo, 30 sementes), com manifesto |
| Página | 7 cômodos na animação, no gêmeo e na tabela por cômodo; verificada no navegador, sem erros |

**Desvio do plano.** O C03 previa "três quartos ocupados à noite", mas a v3dt tem só o morador e o Rex (DQ3-09). Ficou "dois quartos ocupados, longe um do outro". Os três quartos com a família entram na v3dt.1.

**Correção durante a entrega.** Na primeira rodada, a zona cega Z1 da sala não foi deslocada com a casa e ficou na frente da porta externa. A referência passou mesmo assim, porque acende pelo SA; o grupo_exemplo, que só acende pelo SP, caiu a 0% na F1, com atraso de 5 s. Com a Z1 no lugar (x de 7,5 a 8,5, junto ao vão para a cozinha, como na Casa A), os dados foram refeitos; o CSV acima é o corrigido. Lição para o roteiro: ao deslocar uma planta, deslocar também as zonas cegas, que ficam em coordenadas absolutas.

## 12. Comparação V0–V3 no mesmo núcleo (CP-V3-01)

As quatro versões rodaram no `nucleo-v1.3` (7077d3c), com 30 sementes. V0 e V2 subiram para esse núcleo nos ajustes **v0dtc** e **v2dtb**, que acrescentam as famílias F8 e F9; a regressão manteve todas as assinaturas anteriores (V0: 76 iguais; V2: 58 iguais). Dados: V0 `experimentos-V0-20261029-v13.csv`, V1 `experimentos-V1-20261029-v1dt1.csv`, V2 `experimentos-V2-20261029-v13.csv`, V3 `experimentos-V3-20261029.csv`.

Requisitos atendidos (% das execuções), só cenários G*:

| Família | Controlador | V0 (1) | V1 (2) | V2 (4) | V3 (7) |
|---|---|---|---|---|---|
| F1 entrada e saída | referência | 100 | 100 | 100 | 100 |
| | grupo_exemplo | 100 | 65 | 43 | 29 |
| F2 parado | referência | 100 | 100 | 100 | 100 |
| | grupo_exemplo | 100 | 50 | 25 | 29 |
| F3 passagem interna | referência | — | 100 | 100 | 100 |
| | grupo_exemplo | — | 100 | 67 | 50 |
| F9 dormindo | referência | 100 | 100 | 100 | 100 |
| | grupo_exemplo | 100 | 50 | 25 | 29 |
| F4–F8 | ambos | 100 | 100 | 100 | 100 |

Medidas por cômodo (referência):

| Medida | V0 | V1 | V2 | V3 |
|---|---|---|---|---|
| Desperdício por cômodo, F1 (s) | 60,7 | 58,1 | 59,1 | 35,2 |
| Ocupação desconhecida por cômodo, F2 (s) | 5,1 | 20,6 | 79,8 | 73,2 |
| Espelho fiel, F7 (%) | 98,3 | 80,0 | 66,1 | 69,7 |
| Gêmeo não atual por cômodo, F5 (s) | 601,2 | 601,2 | 601,2 | 601,2 |

Leitura:

- **A referência não perde requisito com o porte**: 100% em todas as famílias, de 1 a 7 cômodos.
- **O grupo_exemplo piora com as passagens internas.** Ele só acende pelo SP. Nos cômodos que se alcançam por passagem interna, o atraso da PIR estoura o limite de 1 s. De 1 para 4 cômodos a queda é de 100 para 25–43%. Na Casa B fica entre 29 e 50%, porque a profundidade nova (quarto 3 a duas passagens) repete o mesmo efeito em mais cômodos, sem um mecanismo novo.
- **O desperdício por cômodo cai na Casa B** (35 s contra cerca de 60 s). Isso é efeito da normalização, não ganho do controlador: o desperdício total quase não cresce de V2 para V3 (236 → 246 s), porque cada cenário G* usa só o cômodo-alvo e o caminho até ele, e a divisão é por 7. Para comparar portes, use a medida por cômodo **ocupado** (a fazer no comparador).
- **O espelho fica entre 66 e 70% a partir de 4 cômodos**: o que pesa é a composição dos episódios (cômodos sem evidência, em que o gêmeo não afirma), não o número de cômodos.
- **A desconexão custa o mesmo por cômodo** (601 s): cada cômodo fica desatualizado durante a queda, e a reconciliação não cresce com o porte (100 ms).

Resultados de simulação, não de medição (P7).

## 13. Próximos passos da v3dt (feitos)

1. Tags `v3dt`, `v0dtc` e `v2dtb`: criadas em 29/10/2026.
2. v3dt.1: entregue (§14).

## 14. Entrega da v3dt.1

| Item | Situação |
|---|---|
| Núcleo `nucleo-v1.4` (commit `e7f8123`) | Relógio de parede (`hora_inicio`); faixas de T_apagamento no hub (`FAIXA_APLICADA`); sugestões e aceite na plataforma (`APP_ACEITAR`, `APP_RECUSAR`, versão de configuração com as sugestões de origem); modelo agregado do DTReg10k-R (`plataforma/aprendizado.py`); ação `LER` (◆, §17); **OR-17**; rotina diária e protocolo de semanas (`experimentos/rotina.py`, `experimentos/aprendizado.py`, `reg10k.py aprendizado`, opção `--politica` para o E15); schemas, página (hora do dia, sugestões no cartão do cenário), modelo (RN-V3-01 a RN-V3-03), UML (`classes-v3dt1`, `sequencia-S02`, casos de uso), E15, guia v07 |
| Regressão | As 92 assinaturas do núcleo e as 120 da v3dt ficam iguais (CP-V3-02: sem aceite, nada muda). 279 testes, em Python 3.9 e 3.12, dos quais 20 novos; quatro deles fazem a OR-17 falhar quando deve (CP-V3-04) |
| Ambiente | `casa-b-familia`: a Casa B com morador, moradora, criança, idoso e o Rex. Quarto do casal, quarto 2 da criança, quarto 3 do idoso |
| Cenários do catálogo | S01 leitura na sala sem faixa; S02 sugestão aceita (sala das 20h às 23h com 5 min); S03 sugestão recusada; S04 quarto à noite com a faixa curta já aceita; S05 aceite com o canal fora (a versão espera a reconexão). Todos aprovados com a referência; catálogo sem problemas; página verificada no navegador, inclusive em iframe |
| Rotina | `experimentos/rotina-familia.json`: das 17h à 1h, com variação por semente e passos eventuais. O idoso lê na sala; a criança brinca no quarto 2 e dorme por volta das 20h50; o casal janta, vê TV na sala e dorme por volta das 22h30; a moradora lê no quarto antes de dormir; o Rex dorme na área de serviço |
| Protocolo (CP-V3-03) | 10 sementes × (14 dias de treino + 7 de teste em dois braços) = 280 dias simulados, 68 min em 2 processos. Invariantes respeitadas em **todos** os dias. Dados em `dados/aprendizado-V3-20261029*` com manifesto (núcleo `e7f8123`, versão `0f1bd45`) |

## 15. Resultados do protocolo

**O que o gêmeo sugeriu.** As 10 sementes chegaram às mesmas quatro sugestões, ao fim de 14 dias:

| Cômodo | Faixa | T_apagamento | Evidência (semente 0) | Leitura |
|---|---|---|---|---|
| Sala | 17h–23h | 300 s | reação logo depois de quase todo apagamento com alguém dentro | O idoso lê à tarde; a família vê TV à noite |
| Cozinha | 19h–21h | 300 s | idem | Jantar: gente sentada e acordada |
| Quarto (casal) | 22h–23h | 300 s | 334 reações em 348 apagamentos | A moradora lê na cama antes de dormir |
| Quarto 3 (idoso) | 21h–22h | 30 s | 14 apagamentos, 14 imóveis, nenhuma reação | O idoso dorme por volta das 21h35 |

**Efeito do aceite**, por dia de teste. Os braços têm as mesmas rotinas e sementes, e a diferença tem IC 95% sobre as 10 sementes. Simulação, não medição:

| Medida (casa inteira) | Recusar (controle) | Aceitar tudo | Diferença |
|---|---|---|---|
| Escuro com alguém acordado | 1.732 s | 376 s | −1.355 ± 54 s (−78%) |
| Apagamentos com alguém acordado | 228 | 47 | −181 ± 7 (−79%) |
| Aceso sem ninguém | 2.067 s | 3.398 s | +1.331 ± 71 s (+64%) |
| Aceso com todos dormindo | 188 s | 352 s | +165 ± 65 s (+88%) |

| Cômodo | O que melhora | O que custa |
|---|---|---|
| Sala | escuro com alguém acordado 1.445 → 316 s; apagamentos 191 → 41 | aceso sem ninguém 272 → 1.142 s |
| Cozinha | escuro 108 → 17 s | aceso sem ninguém 96 → 424 s |
| Quarto (casal) | escuro 176 → 40 s (quem lê) | aceso com todos dormindo 69 → 263 s; aceso sem ninguém 421 → 554 s |
| Quarto 3 | aceso com todos dormindo 64 → 34 s | — |

## 16. Leitura e achados

- **O aprendizado resolve o dilema da E14 em parte.** O dilema era quem lê × quem dorme, sem hora do dia. Com hora do dia e perfil por cômodo, o gêmeo separa os dois casos onde eles acontecem em horas diferentes: sala à tarde e à noite, contra o quarto 3 às 21h.
- **RS-11. Onde os dois casos se misturam na mesma hora, a sugestão cobra caro.** No quarto do casal às 22h, a moradora lê e o marido já dorme. O gêmeo vê reação ao escuro e sugere 5 min, bom para ela e ruim quando os dois adormecem: +195 s aceso com todos dormindo, por noite. É a decisão que o E15 entrega ao titular. Aceitar só as faixas da sala, da cozinha e do quarto 3 (`--politica comodos:sala,cozinha,quartotres`, arquivos `dados/aprendizado-V3-20261029-escolhida*`) foi medido com o mesmo protocolo e as mesmas 10 sementes. Mantém 90% do ganho no escuro: −1.222 ± 40 s por dia (−71%), contra −1.355 ± 54 s aceitando tudo; a estimativa pela soma dos cômodos (1.219 s) se confirmou. Apagamentos com alguém acordado caem 164 ± 5 por dia (−72%). O custo com quem dorme desaparece e vira ganho: −29 ± 8 s aceso com todos dormindo (−16%), contra +165 ± 65 s aceitando tudo. O tempo aceso sem ninguém sobe +1.199 ± 70 s (+58%), pouco abaixo dos +1.331 s. As invariantes valem em todos os dias simulados.
- **O custo do T longo é o desperdício.** Desperdício quer dizer luz acesa depois que o cômodo esvazia: +1.331 s por dia, quase todo na sala. O plano previa a troca; a medida a torna explícita para o artigo.
- **RS-10. O sinal de "alguém dentro" exige movimento depois da passagem.** A criança entra no quarto 2 e deita em seguida. O único movimento visto acontece até 10 s depois da passagem, e o modelo o trata como "passou e saiu". Por isso o quarto 2 nunca recebeu a faixa curta, embora a criança durma lá todas as noites. Sem identificar ninguém, o gêmeo não distingue "entrou e deitou" de "passou". É uma limitação honesta do modelo, que vai para a discussão do E15 e para o refinamento RS-10 na V2/V3 v06.
- **A sugestão converge e é estável.** Em 10 de 10 sementes, as mesmas faixas. A variação da rotina (±10 a ±30 min) não mudou o que o gêmeo aprende com 14 dias e o mínimo de 5 dias de evidência por hora.
- **RS-12. O aceite precisa do caminho da versão de configuração.** O S05 mostra que o aceite com o canal fora fica PENDENTE e só vale na reconexão. A OR-12 (decisões locais iguais com e sem rede) não se aplica a um aceite, que muda a casa de propósito, como comando e preferência.
- **RS-13. Privacidade.** O perfil guardado (`dados/aprendizado-*-sugestoes.json`) tem só cômodo, hora e contagens. Mesmo assim revela a rotina da casa: a que horas o idoso dorme, quem lê no quarto às 22h. Na V2/V3 v06, ele vira a classe de dado "comportamental agregado", ainda pessoal.

## 17. Ajustes feitos na construção (◆)

| Item | Ajuste | Motivo |
|---|---|---|
| ◆ Ação `LER` | Nova ação de ocupante: parado e acordado, acena de 3 a 10 s depois que a luz do cômodo apaga | Sem reação ao escuro, não haveria o que o gêmeo aprender sobre quem lê. O `PARADO` não reage, e mudar o `PARADO` mudaria os cenários antigos |
| ◆ Janela do dia | Das 17h à 1h (8 h), e não 24 h | Custo: 29 s por dia simulado com 5 ocupantes e 7 cômodos. É o trecho em que ler e dormir acontecem |
| ◆ Braços pareados | Treino uma vez; teste em dois braços (aceitar × recusar) nos mesmos dias e sementes | A comparação antes × depois de um braço só mistura o efeito do aceite com a variação da rotina |
| ◆ Política de aceite | Opção `--politica` (todas, longas, curtas, por cômodo) | E15.2: o aluno decide como titular |
| ◆ OR-12 e aceite | `APP_ACEITAR` entra em `tem_app` | O aceite muda decisões locais de propósito (§16, RS-12) |
| ◆ S04 | Começa às 22h50, não às 22h40 | A faixa das 23h precisava entrar antes de a moradora dormir |
| ◆ C03 da v3dt | Continua com dois quartos | Ver §11 |

## 18. Critérios de pronto

| ID | Situação |
|---|---|
| CP-V3-01 | ✔ Comparação V0–V3 no `nucleo-v1.3` (§12) |
| CP-V3-02 | ✔ Sem aceite, nada muda: 92 + 120 assinaturas iguais; com aceite, as faixas valem (S02, S04, S05) e a OR-17 é respeitada |
| CP-V3-03 | ✔ 10 sementes de 21 dias, com o efeito por cômodo e faixa (§15; planilha `aprendizado-V3-v3dt1.xlsx`) |
| CP-V3-04 | ✔ Testes da OR-17: aplicar sem aceite, versão sem aceite, sugestão recusada numa versão, dado por ocupante |

**Documentos da plataforma:** V2/V3 v06 (RF-ACO-09, Sugestao, PerfilOcupacao, FaixaHoraria, INV-17, OC-17, §3.6.4) e PD10 para a V1, conforme o §6.
