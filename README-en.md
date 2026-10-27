<a id="top"></a>

<p align="center">
  <img src="https://i.imgur.com/ruJ7tB0.png" alt="KAngel Bot" width="600">
</p>

# KAngel Bot ʚ ɞ

🇧🇷 [Ler em português](README.md)

A Discord bot written in Python with [discord.py](https://discordpy.readthedocs.io/) that organizes your studies, plays music and looks after the server. It chats through AI (Gemini), and has a pomodoro timer, reminders, tasks, a tutor, music with a queue, moderation and welcome messages. It supports two languages (Portuguese and English) and two personalities (Ame and KAngel), chosen per server.

```
while attention.exists():
    perform()
```

| Info | Details |
|---|---|
| **Prefix** | `.` (configurable in `.env`) |
| **Focus** | studying, music, fun and moderation |
| **AI** | Gemini (`gemini-3.6-flash`, via `google-genai`) |
| **Languages** | Portuguese and English, per server |
| **Personalities** | `Ame` (default) and `KAngel`, per server |
| **Highlights** | AI tutor, pomodoro, persistent reminders, music with a queue (yt-dlp + FFmpeg) |

## Features

### AI Chat (Gemini)
- When you mention the bot (`@bot`), it replies directly using Gemini
- You can also keep the conversation going by replying to one of the bot's messages, with no need to mention it again
- Uses the last 5 messages in the channel as context (messages without text, such as images and gifs, are ignored)
- Replies in the language and personality chosen for the server, through a system instruction (editable in `textos.py`): lowercase letters, short and direct answers, and no made-up facts
- Chats about any topic and helps with studying when asked
- Long replies are split into several messages to fit Discord's limit, and no reply mentions anyone
- Command messages (`.`), messages from other bots and DMs never trigger Gemini
- If Gemini is overloaded (5xx error), the bot retries up to 3 times, with a time limit per call
- If Gemini fails, the bot says there was an error instead of staying silent

### Tutor (studying with AI)
| Command | Description |
|---|---|
| `.explicar topic` / `.explain` | a clear, didactic explanation with a practical example |
| `.resumir text` / `.summarize` | a summary in short bullet points |
| `.quiz topic` | 5 multiple-choice questions (a to d), with the answer key hidden in a spoiler |

If `CANAL_ESTUDOS_ID` is set, these commands only work in that channel. With `0`, they work in any channel.

### Focus (pomodoro)
| Command | Description |
|---|---|
| `.foco 25 5 4` / `.focus` | starts a session: focus minutes, break minutes and number of cycles (these are the default values) |
| `.pararfoco` / `.stopfocus` | ends your session |

- The bot pings you in the channel when each break, each return to focus and the whole session end
- Only one active session per person
- Limits (in `config.py`): focus from 1 to 120 min, break from 1 to 60 min, cycles from 1 to 12
- Sessions are kept in memory only: if the bot restarts, they are lost

### Reminders
| Command | Description |
|---|---|
| `.lembrar 2h exam` / `.remind` | creates a reminder (accepts `30m`, `2h`, `1d`, `1h30m`) |
| `.lembretes` / `.reminders` | shows your pending reminders |
| `.cancelarlembrete 3` / `.unremind` | cancels a reminder by its number |

- Minimum time of 10 seconds and maximum of 30 days; the text can be at most 500 characters
- They are saved in `lembretes.json`, so they survive bot restarts
- The alert arrives in the same channel where the reminder was created; if the channel no longer exists, it goes to your DMs
- The bot checks reminders every 10 seconds

### Tasks
| Command | Description |
|---|---|
| `.tarefa text` / `.task` | adds a task to your list (up to 200 characters) |
| `.tarefas` / `.tasks` | shows your numbered list |
| `.feito 2` / `.done` | marks a task as completed by its number (it leaves the list) |

The list is personal and is saved in `tarefas.json`.

### Music
`.tocar` only works in the text channel set in `CANAL_MUSICA_ID` (with `0`, it works in any channel), and you need to be in a voice channel.

| Command | Description |
|---|---|
| `.tocar` / `.play` | searches for and plays a song (name or link); it joins the queue if something is already playing |
| `.fila` / `.queue` | shows the music queue |
| `.pular` / `.skip` | skips to the next song |
| `.pausar` / `.pause` | pauses the current song |
| `.continuar` / `.resume` | resumes from where it stopped |
| `.parar` / `.stop` | disconnects from the voice channel and clears the queue |

The bot joins the voice channel you are in when you use `.tocar` (or moves to yours if it is in another one). Text becomes a YouTube search and links go straight to `yt-dlp`; the audio is played with `FFmpeg`. The search has a 20-second limit. When a song ends, the next one in the queue starts automatically. Each server has its own queue, which is kept in memory only and is lost if the bot restarts.

### Fun
| Command | Description |
|---|---|
| `.moeda` / `.coin` | flips a coin: heads or tails |
| `.dado` / `.dice` | rolls a number from 1 to 6 |

### Moderation
| Command | Description |
|---|---|
| `.kick @person reason` | kicks a member (requires the `kick_members` permission) |
| `.ban @person reason` | bans a member (requires the `ban_members` permission) |

The reason is optional. Anyone without permission gets a warning, and the bot also needs the permissions and a role above the target person.

### Welcome and goodbye
- When someone joins the server, the bot sends an embed with a gif and the welcome message in the configured channel
- When someone leaves, the bot announces it in another configured channel
- People who leave because of `.kick` or `.ban` don't trigger the goodbye message (those commands already have their own message)
- Both messages follow the language and personality chosen for the server
- New members automatically receive the member role (`CARGO_MEMBRO_ID` in `.env`); if the server uses membership screening, the role is given after the person accepts the rules. Bots don't receive the role
- For this to work, the bot's role must be above the member role and have the **Manage Roles** permission
- If a channel or the role is not found, the bot warns in the console

### Panel
`.painel` / `.panel` sends and pins an embed with all of the bot's commands, in the server's language (administrators only).

## Languages (pt/en)
- `.idioma pt` / `.idioma en` (or `.language`) changes the language of the replies on that server
- The choice is per server, saved in `idiomas.json`, and survives bot restarts
- Default: Portuguese
- Command names exist in both languages at the same time (e.g. `.tocar` and `.play`, `.foco` and `.focus`), regardless of the chosen language
- Most phrases live in `textos.py` (the panel's live in `painel.py`), written in both languages

## Modes (personality)
- `.modo Ame` / `.modo KAngel` (or `.mode`) changes the bot's personality on that server
- **Ame** is the default tone: simple and direct, with no emojis or decorative symbols
- **KAngel** is more cheerful and affectionate, with a streamer vibe: it encourages the person and uses a few symbols (♡ ★) and simple kaomojis, without overdoing it
- The mode changes the AI's replies (chat and tutor) and also the bot's fixed messages (welcome, goodbye, fun, reminders, etc.), in both languages
- The choice is per server, saved in `modos.json`, and survives bot restarts
- Language and mode combine: there are 4 variations in total (`pt`, `en`, `pt-KAngel`, `en-KAngel`)

## Prefix and `/` commands
Commands work both ways: typing the prefix directly or using `/` with Discord's guided menu, both always available, with no need to choose.

- The music and fun commands exist in `/` with both names (`/tocar` and `/play`, `/moeda` and `/coin`...)
- For the others, `/` uses the Portuguese name (e.g. `/foco`, `/lembrar`, `/modo`)
- `.painel` only works with the prefix
- Commands only work inside servers, not in DMs

## Project structure

```
.
├── main.py                      # sets up the bot and loads the cogs automatically
├── config.py                    # reads .env: token, key, prefix, channel and role IDs, Gemini model, pomodoro limits, yt-dlp and FFmpeg options
├── textos.py                    # phrases and AI instructions (pt and en, Ame and KAngel modes)
├── armazenamento.py             # loads and saves the .json files
├── idioma_storage.py            # stores the language chosen by each server
├── modo_storage.py              # stores the mode (Ame/KAngel) chosen by each server
├── requirements.txt
├── .env                         # Discord token and Gemini key
├── idiomas.json                 # generated automatically
├── modos.json                   # generated automatically
├── lembretes.json               # generated automatically
├── tarefas.json                 # generated automatically
└── cogs/
    ├── ia.py                    # chat with Gemini
    ├── tutor.py                 # .explicar, .resumir, .quiz
    ├── pomodoro.py              # .foco, .pararfoco
    ├── lembretes.py             # .lembrar, .lembretes, .cancelarlembrete
    ├── tarefas.py               # .tarefa, .tarefas, .feito
    ├── musica.py                # .tocar, .fila, .pular, .pausar, .continuar, .parar
    ├── diversao.py              # .moeda, .dado
    ├── moderacao.py             # .kick, .ban
    ├── boasvindas.py            # join (welcome + automatic role) and leave
    ├── idioma.py                # .idioma
    ├── modo.py                  # .modo
    └── painel.py                # .painel
```

`main.py` automatically loads every `.py` file in the `cogs/` folder (except those starting with `_`). To disable a part, just remove the file from the folder or rename it with a `_` in front.

## Libraries used

- [`discord.py[voice]`](https://pypi.org/project/discord.py/): main library, with voice support
- [`google-genai`](https://pypi.org/project/google-genai/): Gemini integration
- [`yt-dlp`](https://pypi.org/project/yt-dlp/): searching and extracting audio from YouTube
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): reading environment variables
- **FFmpeg** (external program, must be installed and on the system PATH)

## License

Copyright (c) 2026 KAngel Bot. All rights reserved.

This software and all of its source code, structure, logic and documentation are protected by copyright.

It is strictly PROHIBITED, without prior and express written authorization from the rights holder, to:

- Copy, reproduce or duplicate any part of this project;
- Modify, adapt or create derivative works;
- Distribute, publish, sublicense or sell copies;
- Use the code, in whole or in part, in your own or third-party projects;
- Reverse engineer or decompile the software.

Access to this repository is provided exclusively for viewing purposes. Any other use requires prior authorization from the rights holder.

---

<p align="center">
  <a href="#top">↑ back to top</a>
</p>