CSV dos experimentos com o manifesto ao lado, e assinaturas de regressão (`assinaturas-<versão>.json`).

## v3dt.1: protocolo do aprendizado do gêmeo

| Arquivo | Conteúdo |
|---|---|
| `aprendizado-V3-20261029.csv` | Uma linha por semente, braço (treino, aceitar, recusar), dia, cômodo e hora, com escuro com alguém acordado, aceso com todos dormindo, aceso sem ninguém e apagamentos com alguém acordado |
| `aprendizado-V3-20261029-dias.csv` | Um dia por linha: invariantes, versão da configuração e métricas do oráculo |
| `aprendizado-V3-20261029-resumo.csv` | Média por dia de teste, por cômodo e hora, nos dois braços |
| `aprendizado-V3-20261029-sugestoes.json` | Por semente: as sugestões, as aceitas e o perfil guardado pelo gêmeo (só cômodo, hora e contagens) |
| `aprendizado-V3-20261029.manifesto.json` | Commits do núcleo e da versão, protocolo, hash das entradas |
| `aprendizado-V3-20261029-escolhida*` | O mesmo protocolo com a política de aceite `comodos:sala,cozinha,quartotres` |

Resultados de simulação, não de medição (P7).
