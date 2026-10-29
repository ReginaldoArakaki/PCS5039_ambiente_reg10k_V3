# Ambiente de simulação Reg10k — V3: Casa B (7 cômodos) e aprendizado do gêmeo

**Versão do documento:** v01 | **Data:** 29/10/2026 | **Situação:** plano para aprovação
**Responsável:** Reginaldo Arakaki (EPUSP)
**Disciplina:** PCS5039 — Engenharia de Software Orientada a IoT (EPUSP)
**Linha de pesquisa:** Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP
**Base:** núcleo `nucleo-v1.3`; V2 (`v2dta`) e V1 (`v1dt.1`); plano das versões paralelas v06 (§4, V3; DQ-PV-01); plano do ambiente v02 (§2.1: "Casa B e aprendizado do gêmeo — modelo comportamental; sugestões com aceite"; DI-09: sem hora do dia até aqui); v0dt (DT-03 e E10: aprendizado mínimo como exercício); V1 Business Drivers v02 (§ privacidade: presença é dado pessoal comportamental); V2/V3 v05 (§2.8: dado comportamental, detalhe retido 30 dias; RN-DT-07: preferência versionada)

| Versão | Data | Mudança |
|---|---|---|
| v01 | 29/10/2026 | Plano para aprovação, com a rodada de dúvidas (§10) |

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

Sem objeção, as propostas valem.

**Duração de referência:** v3dt, 1 dia; v3dt.1, 2 a 3 dias (núcleo `nucleo-v1.4` para o relógio e o aprendizado).
