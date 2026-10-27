<a id="topo"></a>

<p align="center">
  <img src="https://i.imgur.com/ruJ7tB0.png" alt="KAngel Bot" width="600">
</p>

# KAngel Bot ʚ ɞ

🇺🇸 [Read in English](README-en.md)

Bot de Discord escrito em Python com [discord.py](https://discordpy.readthedocs.io/) que organiza os estudos, toca música e cuida do servidor. Ele conversa por IA (Gemini), tem pomodoro, lembretes, tarefas, tutor, música com fila, moderação e boas-vindas, suporta dois idiomas (português e inglês) e duas personalidades (Ame e KAngel), escolhidos por servidor.

```
while attention.exists():
    perform()
```

| Informações | Detalhes |
|---|---|
| **Prefixo** | `.` (configurável no `.env`) |
| **Área** | estudos, música, diversão e moderação |
| **IA** | Gemini (`gemini-3.6-flash`, via `google-genai`) |
| **Idiomas** | português e inglês, por servidor |
| **Personalidades** | `Ame` (padrão) e `KAngel`, por servidor |
| **Destaques** | tutor com IA, pomodoro, lembretes persistentes, música com fila (yt-dlp + FFmpeg) |

## Funcionalidades

### Conversa com IA (Gemini)
- Ao mencionar o bot (`@bot`), ele responde direto com o Gemini
- Também é possível continuar a conversa respondendo (reply) uma mensagem do bot, sem precisar mencionar de novo
- Usa as últimas 5 mensagens do canal como contexto (mensagens sem texto, como imagens e gifs, são ignoradas)
- Responde no idioma e na personalidade escolhidos pro servidor, através de uma instrução de sistema (editável em `textos.py`): letras minúsculas, resposta curta e direta, e sem inventar fatos
- Conversa sobre qualquer assunto e ajuda com estudos quando pedem
- Respostas grandes são divididas em várias mensagens pra caber no limite do Discord, e nenhuma resposta menciona ninguém
- Mensagens de comando (`.`), mensagens de outros bots e DMs nunca disparam o Gemini
- Se o Gemini estiver sobrecarregado (erro 5xx), o bot tenta de novo até 3 vezes, com limite de tempo por chamada
- Se o Gemini falhar, o bot avisa que deu erro em vez de ficar em silêncio

### Tutor (estudos com IA)
| Comando | Descrição |
|---|---|
| `.explicar tema` / `.explain` | explicação didática, com um exemplo prático |
| `.resumir texto` / `.summarize` | resumo em tópicos curtos |
| `.quiz tema` | 5 perguntas de múltipla escolha (a a d), com o gabarito escondido em spoiler |

Se `CANAL_ESTUDOS_ID` estiver configurado, esses comandos só funcionam nesse canal. Com `0`, funcionam em qualquer canal.

### Foco (pomodoro)
| Comando | Descrição |
|---|---|
| `.foco 25 5 4` / `.focus` | inicia uma sessão: minutos de foco, minutos de pausa e número de ciclos (esses são os valores padrão) |
| `.pararfoco` / `.stopfocus` | encerra sua sessão |

- O bot avisa no canal, mencionando você, quando cada pausa, cada volta ao foco e a sessão inteira terminam
- Só uma sessão ativa por pessoa
- Limites (em `config.py`): foco de 1 a 120 min, pausa de 1 a 60 min, ciclos de 1 a 12
- As sessões ficam só na memória: se o bot reiniciar, elas se perdem

### Lembretes
| Comando | Descrição |
|---|---|
| `.lembrar 2h prova` / `.remind` | cria um lembrete (aceita `30m`, `2h`, `1d`, `1h30m`) |
| `.lembretes` / `.reminders` | mostra seus lembretes pendentes |
| `.cancelarlembrete 3` / `.unremind` | cancela um lembrete pelo número |

- Tempo mínimo de 10 segundos e máximo de 30 dias; o texto tem no máximo 500 caracteres
- Ficam salvos em `lembretes.json`, então sobrevivem a reinícios do bot
- O aviso chega no mesmo canal onde o lembrete foi criado; se o canal não existir mais, vai pra DM
- O bot confere os lembretes a cada 10 segundos

### Tarefas
| Comando | Descrição |
|---|---|
| `.tarefa texto` / `.task` | adiciona uma tarefa na sua lista (até 200 caracteres) |
| `.tarefas` / `.tasks` | mostra sua lista, numerada |
| `.feito 2` / `.done` | marca como concluída pelo número (ela sai da lista) |

A lista é pessoal e fica salva em `tarefas.json`.

### Música
O `.tocar` só funciona no canal de texto configurado em `CANAL_MUSICA_ID` (com `0`, funciona em qualquer canal), e você precisa estar num canal de voz.

| Comando | Descrição |
|---|---|
| `.tocar` / `.play` | busca e toca uma música (nome ou link); entra na fila se já tiver algo tocando |
| `.fila` / `.queue` | mostra a fila de músicas |
| `.pular` / `.skip` | pula pra próxima música |
| `.pausar` / `.pause` | pausa a música atual |
| `.continuar` / `.resume` | retoma de onde parou |
| `.parar` / `.stop` | desconecta do canal de voz e limpa a fila |

O bot entra no canal de voz em que você estiver ao usar `.tocar` (ou muda pro seu, se já estiver em outro). Texto vira busca no YouTube e links vão direto pro `yt-dlp`; o áudio é tocado com `FFmpeg`. A busca tem limite de 20 segundos. Quando uma música termina, a próxima da fila começa automaticamente. Cada servidor tem a própria fila, que fica só na memória e se perde se o bot reiniciar.

### Diversão
| Comando | Descrição |
|---|---|
| `.moeda` / `.coin` | sorteia cara ou coroa |
| `.dado` / `.dice` | sorteia um número de 1 a 6 |

### Moderação
| Comando | Descrição |
|---|---|
| `.kick @pessoa motivo` | expulsa um membro (exige permissão `kick_members`) |
| `.ban @pessoa motivo` | bane um membro (exige permissão `ban_members`) |

O motivo é opcional. Quem não tiver permissão recebe um aviso, e o bot também precisa ter as permissões e um cargo acima da pessoa.

### Boas-vindas e saída
- Quando alguém entra no servidor, o bot manda um embed com gif e a mensagem de boas-vindas no canal configurado
- Quando alguém sai, o bot avisa em outro canal configurado
- Quem sai por causa de `.kick` ou `.ban` não gera a mensagem de saída (esses comandos já têm a própria mensagem)
- As duas mensagens seguem o idioma e a personalidade escolhidos pro servidor
- Quem entra recebe automaticamente o cargo de membro (`CARGO_MEMBRO_ID` no `.env`); se o servidor usa a triagem de membros, o cargo é dado depois que a pessoa aceita as regras. Bots não recebem o cargo
- Pra isso funcionar, o cargo do bot precisa estar acima do cargo de membro e ter a permissão **Gerenciar cargos**
- Se um canal ou o cargo não for encontrado, o bot avisa no console

### Painel
`.painel` / `.panel` envia e fixa um embed com todos os comandos do bot, no idioma do servidor (só administradores).

## Idiomas (pt/en)
- `.idioma pt` / `.idioma en` (ou `.language`) troca o idioma das respostas naquele servidor
- A escolha é por servidor, salva em `idiomas.json`, e sobrevive a reinícios do bot
- Padrão: português
- Os nomes dos comandos existem nos dois idiomas ao mesmo tempo (ex: `.tocar` e `.play`, `.foco` e `.focus`), independente do idioma escolhido
- A maioria das frases fica em `textos.py` (as do painel ficam em `painel.py`), escritas nos dois idiomas

## Modos (personalidade)
- `.modo Ame` / `.modo KAngel` (ou `.mode`) troca a personalidade do bot naquele servidor
- **Ame** é o tom padrão: simples e direto, sem emojis nem símbolos decorativos
- **KAngel** é mais animada e carinhosa, com jeito de streamer: incentiva a pessoa e usa alguns símbolos (♡ ★) e kaomojis simples, sem exagero
- O modo muda as respostas da IA (conversa e tutor) e também as mensagens fixas do bot (boas-vindas, saída, diversão, lembretes etc.), nos dois idiomas
- A escolha é por servidor, salva em `modos.json`, e sobrevive a reinícios do bot
- Idioma e modo se combinam: são 4 variações no total (`pt`, `en`, `pt-KAngel`, `en-KAngel`)

## Comandos por prefixo e `/`
Os comandos funcionam dos dois jeitos: digitando o prefixo direto ou usando `/` com o menu guiado do Discord, os dois sempre disponíveis, sem precisar escolher.

- Os comandos de música e diversão existem no `/` com os dois nomes (`/tocar` e `/play`, `/moeda` e `/coin`...)
- Nos demais, o `/` usa o nome em português (ex: `/foco`, `/lembrar`, `/modo`)
- O `.painel` funciona só com o prefixo
- Os comandos só funcionam dentro de servidores, não em DM

## Estrutura do projeto

```
.
├── main.py                      # configura o bot e carrega as cogs automaticamente
├── config.py                    # lê o .env: token, chave, prefixo, IDs de canal e de cargo, modelo do Gemini, limites do pomodoro, opções do yt-dlp e do FFmpeg
├── textos.py                    # frases e instruções da IA (pt e en, modos Ame e KAngel)
├── armazenamento.py             # carrega e salva os arquivos .json
├── idioma_storage.py            # guarda o idioma escolhido por cada servidor
├── modo_storage.py              # guarda o modo (Ame/KAngel) escolhido por cada servidor
├── requirements.txt
├── .env                         # token do Discord e chave do Gemini
├── idiomas.json                 # gerado automaticamente
├── modos.json                   # gerado automaticamente
├── lembretes.json               # gerado automaticamente
├── tarefas.json                 # gerado automaticamente
└── cogs/
    ├── ia.py                    # conversa com o Gemini
    ├── tutor.py                 # .explicar, .resumir, .quiz
    ├── pomodoro.py              # .foco, .pararfoco
    ├── lembretes.py             # .lembrar, .lembretes, .cancelarlembrete
    ├── tarefas.py               # .tarefa, .tarefas, .feito
    ├── musica.py                # .tocar, .fila, .pular, .pausar, .continuar, .parar
    ├── diversao.py              # .moeda, .dado
    ├── moderacao.py             # .kick, .ban
    ├── boasvindas.py            # entrada (boas-vindas + cargo automático) e saída
    ├── idioma.py                # .idioma
    ├── modo.py                  # .modo
    └── painel.py                # .painel
```

O `main.py` carrega sozinho todo arquivo `.py` da pasta `cogs/` (menos os que começam com `_`). Pra desativar uma parte, basta tirar o arquivo da pasta ou renomeá-lo com `_` na frente.

## Bibliotecas usadas

- [`discord.py[voice]`](https://pypi.org/project/discord.py/): biblioteca principal, com suporte a voz
- [`google-genai`](https://pypi.org/project/google-genai/): integração com o Gemini
- [`yt-dlp`](https://pypi.org/project/yt-dlp/): busca e extração de áudio do YouTube
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): leitura das variáveis de ambiente
- **FFmpeg** (programa externo, precisa estar instalado e no PATH do sistema)

## Licença

Copyright (c) 2026 KAngel Bot. Todos os direitos reservados.

Este software e todo o seu código-fonte, estrutura, lógica e documentação são protegidos por direitos autorais.

É estritamente PROIBIDO, sem autorização prévia e expressa por escrito do titular dos direitos:

- Copiar, reproduzir ou duplicar qualquer parte deste projeto;
- Modificar, adaptar ou criar obras derivadas;
- Distribuir, publicar, sublicenciar ou vender cópias;
- Utilizar o código, no todo ou em parte, em projetos próprios ou de terceiros;
- Realizar engenharia reversa ou descompilar o software.

O acesso a este repositório é fornecido exclusivamente para fins de visualização. Qualquer outro uso depende de autorização prévia do titular dos direitos.

---

<p align="center">
  <a href="#topo">↑ voltar ao topo</a>
</p>
