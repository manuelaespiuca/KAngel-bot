<a id="top"></a>

<p align="center">
  <img src="https://i.imgur.com/ruJ7tB0.png" alt="KAngel Bot" width="600">
</p>

# KAngel Bot ʚ ɞ

🇧🇷 [Leia em português](README.md)

A Discord bot written in Python with [discord.py](https://discordpy.readthedocs.io/) that helps you study, plays music and takes care of your server. It chats using AI (Gemini) and has a pomodoro timer, reminders, tasks, a study tutor, a music queue, moderation and welcome messages. It supports two languages (Portuguese and English) and two personalities (Ame and KAngel), both chosen per server.

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
| **Highlights** | AI tutor, pomodoro, persistent reminders, music queue (yt-dlp + FFmpeg) |

## Features

### AI chat (Gemini)
- When you mention the bot (`@bot`), it replies directly using Gemini
- You can also keep the conversation going by replying to one of the bot's messages, without mentioning it again
- Uses the last 5 messages in the channel as context (messages without text, such as images and gifs, are ignored)
- Replies in the language and personality chosen for the server, through a system instruction (editable in `textos.py`): lowercase letters, short and direct answers, and no made-up facts
- Chats about anything and helps with studying when asked
- Long replies are split into several messages to fit Discord's limit, and no reply mentions anyone
- Command messages (`.`), messages from other bots and DMs never trigger Gemini
- If Gemini is overloaded (5xx error), the bot retries up to 3 times, with a time limit per call
- If Gemini fails, the bot says there was an error instead of staying silent

### Tutor (AI study help)
| Command | Description |
|---|---|
| `.explicar topic` / `.explain` | clear explanation with a practical example |
| `.resumir text` / `.summarize` | summary in short bullet points |
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
- Sessions live only in memory: if the bot restarts, they are lost

### Reminders
| Command | Description |
|---|---|
| `.lembrar 2h exam` / `.remind` | creates a reminder (accepts `30m`, `2h`, `1d`, `1h30m`) |
| `.lembretes` / `.reminders` | shows your pending reminders |
| `.cancelarlembrete 3` / `.unremind` | cancels a reminder by its number |

- Minimum time is 10 seconds and maximum is 30 days; the text can have up to 500 characters
- They are saved in `lembretes.json`, so they survive bot restarts
- The alert arrives in the same channel where the reminder was created; if the channel no longer exists, it goes to your DMs
- The bot checks reminders every 10 seconds

### Tasks
| Command | Description |
|---|---|
| `.tarefa text` / `.task` | adds a task to your list (up to 200 characters) |
| `.tarefas` / `.tasks` | shows your numbered list |
| `.feito 2` / `.done` | marks a task as done by its number (it leaves the list) |

The list is personal and saved in `tarefas.json`.

### Music
`.tocar` only works in the text channel set in `CANAL_MUSICA_ID` (with `0`, it works in any channel), and you need to be in a voice channel.

| Command | Description |
|---|---|
| `.tocar` / `.play` | searches for and plays a song (name or link); joins the queue if something is already playing |
| `.fila` / `.queue` | shows the song queue |
| `.pular` / `.skip` | skips to the next song |
| `.pausar` / `.pause` | pauses the current song |
| `.continuar` / `.resume` | resumes from where it stopped |
| `.parar` / `.stop` | leaves the voice channel and clears the queue |

The bot joins the voice channel you are in when you use `.tocar` (or moves to yours if it is in another one). Text becomes a YouTube search and links go straight to `yt-dlp`; the audio is played with `FFmpeg`. The search has a 20-second limit. When a song ends, the next one in the queue starts automatically. Each server has its own queue, which lives only in memory and is lost if the bot restarts.

### Fun
| Command | Description |
|---|---|
| `.moeda` / `.coin` | flips a coin |
| `.dado` / `.dice` | rolls a number from 1 to 6 |

### Moderation
| Command | Description |
|---|---|
| `.kick @person reason` | kicks a member (requires the `kick_members` permission) |
| `.ban @person reason` | bans a member (requires the `ban_members` permission) |

The reason is optional. People without permission get a warning, and the bot also needs the right permissions and a role above the target.

### Welcome and goodbye
- When someone joins the server, the bot sends an embed with a gif and a welcome message in the configured channel
- When someone leaves, the bot announces it in another configured channel
- Members who leave because of `.kick` or `.ban` don't trigger the goodbye message (those commands already have their own message)
- Both messages follow the language and personality chosen for the server
- New members automatically get the member role (`CARGO_MEMBRO_ID` in `.env`); if the server uses membership screening, the role is given after the person accepts the rules. Bots don't get the role
- For this to work, the bot's role must be above the member role and have the **Manage Roles** permission
- If a channel or the role is not found, the bot warns in the console

### Panel
`.painel` / `.panel` sends and pins an embed with all the bot's commands, in the server's language (administrators only).

## Languages (pt/en)
- `.idioma pt` / `.idioma en` (or `.language`) changes the language of the replies on that server
- The choice is per server, saved in `idiomas.json`, and survives bot restarts
- Default: Portuguese
- Command names exist in both languages at the same time (e.g. `.tocar` and `.play`, `.foco` and `.focus`), regardless of the chosen language
- Most phrases live in `textos.py` (the panel ones are in `painel.py`), written in both languages

## Modes (personality)
- `.modo Ame` / `.modo KAngel` (or `.mode`) changes the bot's personality on that server
- **Ame** is the default tone: simple and direct, without emojis or decorative symbols
- **KAngel** is more cheerful and caring, with a streamer vibe: it encourages the person and uses a few symbols (♡ ★) and simple kaomojis, without overdoing it
- The mode changes the AI replies (chat and tutor) and also the bot's fixed messages (welcome, goodbye, fun, reminders, etc.), in both languages
- The choice is per server, saved in `modos.json`, and survives bot restarts
- Language and mode combine: there are 4 variations in total (`pt`, `en`, `pt-KAngel`, `en-KAngel`)

## Prefix and `/` commands
Commands work both ways: typing the prefix directly or using `/` with Discord's guided menu. Both are always available, with no need to choose.

- Music and fun commands exist in `/` with both names (`/tocar` and `/play`, `/moeda` and `/coin`...)
- For the others, `/` uses the Portuguese name (e.g. `/foco`, `/lembrar`, `/modo`)
- `.painel` only works with the prefix
- Commands only work inside servers, not in DMs

## How to use

This project is not a hosted bot: everyone runs their own copy, with their own Discord bot and their own Gemini API key. That way, nobody uses anyone else's key. The bot is only online while the program is running.

### Requirements

- [Python](https://www.python.org/downloads/) 3.10 or newer
- [FFmpeg](https://ffmpeg.org/download.html) installed and in your PATH (required for music)
  - Windows: `winget install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux (Debian/Ubuntu): `sudo apt install ffmpeg`
- A Discord account and a Google account (for the Gemini key)

### 1. Download the project

```bash
git clone https://github.com/manuelaespiuca/KAngel-bot.git
cd KAngel-bot
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your bot on Discord

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab and copy the **token** (click *Reset Token* if you need to generate one).
3. Still on the **Bot** tab, enable both *Privileged Gateway Intents*:
   - **Server Members Intent** (welcome and goodbye messages)
   - **Message Content Intent** (AI chat and prefix commands)

### 4. Get your Gemini API key

Create a free key at [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Set up the `.env`

Copy the example file (it must stay in the same folder as `main.py`):

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in at least:

```
DISCORD_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
```

#### Optional variables

| Variable | What it does |
|---|---|
| `MODELO_GEMINI` | Gemini model used by the AI (default: `gemini-3.6-flash`) |
| `PREFIXO` | prefix for text commands (default: `.`) |
| `CANAL_MUSICA_ID` | channel where `.tocar` works (`0` = any channel) |
| `CANAL_ESTUDOS_ID` | channel for the tutor commands (`0` = any channel) |
| `CANAL_BOAS_VINDAS_ID` | channel for welcome messages (`0` = disabled) |
| `CANAL_SAIDA_ID` | channel for goodbye messages (`0` = disabled) |
| `CARGO_MEMBRO_ID` | role automatically given to new members (`0` = disabled) |
| `GIF_BOAS_VINDAS_URL` | link to a gif for the welcome message |

**How to get an ID:** in Discord, turn on *Developer Mode* under Settings → Advanced. Then right-click a channel or role and choose **Copy ID**.

### 6. Invite the bot to your server

In the Developer Portal, go to **OAuth2 → URL Generator**:

1. Under *Scopes*, check `bot` and `applications.commands`.
2. Under *Bot Permissions*, check: **Send Messages**, **Embed Links**, **Read Message History**, **Manage Messages** (to pin the panel), **Kick Members**, **Ban Members**, **Manage Roles**, **Connect** and **Speak**.
3. Copy the generated link, open it in your browser and choose your server.

After inviting, move the bot's role **above** the member role (Server Settings → Roles), otherwise it can't give the role or moderate.

### 7. Run the bot

```bash
python main.py
```

If everything is right, you will see `bot online como ... | N cogs carregados` in the terminal. Slash commands (`/`) can take a few minutes to show up in Discord.

The files `idiomas.json`, `modos.json`, `lembretes.json` and `tarefas.json` are created automatically as you use the bot.

### Common problems

- **"a variável ... não está definida"** (variable not set): the `.env` is missing or incomplete. Check step 5.
- **"token do Discord inválido"** (invalid token): copy the token again from the Developer Portal.
- **Intents error**: enable both *Privileged Gateway Intents* (step 3).
- **Music doesn't play**: check that FFmpeg is installed (`ffmpeg -version` in the terminal) and that you are in a voice channel.
- **The AI doesn't reply**: check your Gemini key and whether the model in `MODELO_GEMINI` is available for your account.
- **The bot doesn't give roles or kick anyone**: the bot's role must be above the others and have the required permissions.

## Project structure

```
.
├── main.py                      # sets up the bot and loads the cogs automatically
├── config.py                    # reads the .env: token, key, prefix, channel and role IDs, Gemini model, pomodoro limits, yt-dlp and FFmpeg options
├── textos.py                    # phrases and AI instructions (pt and en, Ame and KAngel modes)
├── armazenamento.py             # loads and saves the .json files
├── idioma_storage.py            # stores the language chosen by each server
├── modo_storage.py              # stores the mode (Ame/KAngel) chosen by each server
├── requirements.txt
├── LICENSE                      # MIT license
├── .gitignore                   # files Git ignores (.env and bot data)
├── .env.example                 # template for the .env (copy to .env and fill in)
├── .env                         # created by you
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

`main.py` automatically loads every `.py` file in the `cogs/` folder (except those starting with `_`). To disable a feature, just remove the file from the folder or rename it with a `_` in front.

## Libraries used

- [`discord.py[voice]`](https://pypi.org/project/discord.py/): main library, with voice support
- [`google-genai`](https://pypi.org/project/google-genai/): Gemini integration
- [`yt-dlp`](https://pypi.org/project/yt-dlp/): searching and extracting audio from YouTube
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): reading environment variables
- **FFmpeg** (external program, must be installed and in the system PATH)

## License

Distributed under the [MIT](LICENSE) license. You can use, copy, modify and distribute this project, as long as you keep the copyright notice and the license.

Copyright (c) 2026 Manuela Espiúca.

---

<p align="center">
  <a href="#top">↑ back to top</a>
</p>