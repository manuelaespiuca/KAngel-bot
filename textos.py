# Todas as mensagens do bot, em português e inglês.
# Placeholders como {mention} e {texto} são preenchidos pelo código.
# Se precisar de chaves literais num texto, escreva {{ e }}.
#
# PERSONALIDADE: edite "instrucao_conversa" e "instrucao_tutor" pra mudar o jeito
# que a IA fala. O resto são só mensagens fixas.

_BASE = {
    "pt": {
        # ---------- IA ----------
        "instrucao_conversa": (
            "você é uma assistente num servidor do discord. "
            "fale em português do brasil, em letras minúsculas, de forma natural e simples, "
            "como uma pessoa normal conversando. "
            "não use emojis nem símbolos decorativos. "
            "responda de forma curta e direta, a menos que peçam algo longo. "
            "converse sobre qualquer assunto e ajude com estudos quando pedirem. "
            "nunca invente fatos: se não souber, diga que não sabe. "
            "o histórico tem mensagens de várias pessoas do canal; responda à mais recente."
        ),
        "instrucao_tutor": (
            "você é uma tutora paciente. "
            "responda em português do brasil, em letras minúsculas, com linguagem simples e natural. "
            "não use emojis nem símbolos decorativos. "
            "explique passo a passo, sem enrolar, e use a formatação do discord (negrito, listas) só quando ajudar. "
            "se o pedido for confuso, faça o seu melhor e diga o que assumiu."
        ),
        "erro_gemini": "não consegui responder agora. tente novamente mais tarde.",

        # ---------- tutor ----------
        "tutor_canal_errado": "os comandos de estudo só funcionam em <#{canal}>.",
        "prompt_explicar": (
            "explique o tema abaixo de forma didática e simples, como pra alguém que está aprendendo agora. "
            "termine com um exemplo prático.\n\ntema: {entrada}"
        ),
        "prompt_resumir": (
            "resuma o texto abaixo em tópicos curtos, mantendo só o essencial.\n\ntexto: {entrada}"
        ),
        "prompt_quiz": (
            "crie 5 perguntas de múltipla escolha (alternativas a, b, c e d) sobre o tema abaixo. "
            "depois de todas as perguntas, coloque o gabarito escondido com spoiler do discord, "
            "neste formato: ||1-b, 2-a, 3-d, 4-c, 5-b||\n\ntema: {entrada}"
        ),

        # ---------- boas-vindas ----------
        "boas_vindas": "seja bem vindo(a), {mention} . ̣̣♡",
        "saida": "{membro} saiu do servidor.",

        # ---------- diversão ----------
        "moeda_cara": "cara",
        "moeda_coroa": "coroa",
        "moeda": "deu **{resultado}**!",
        "dado": "você tirou **{resultado}**!",

        # ---------- idioma ----------
        "idioma_invalido": "idioma inválido. use `.idioma pt` ou `.idioma en`.",
        "idioma_trocado": "idioma trocado para português.",

        # ---------- modo ----------
        "modo_invalido": "modo inválido. use `.modo KAngel` ou `.modo Ame`.",
        "modo_trocado": "modo trocado para Ame.",

        # ---------- lembretes ----------
        "lembrar_invalido": "não entendi o tempo. use algo como `30m`, `2h`, `1d` ou `1h30m` (mínimo 10s, máximo 30 dias).",
        "lembrar_ok": "combinado, eu te lembro <t:{ts}:R> de: {texto}",
        "lembretes_vazio": "você não tem lembretes pendentes.",
        "lembretes_lista": "seus lembretes:\n{texto}",
        "lembrete_item": "`{id}` - <t:{ts}:R> - {texto}",
        "lembrete_chegou": "{mention} lembrete: {texto}",
        "lembrete_inexistente": "não achei o lembrete `{id}` na sua lista.",
        "lembrete_cancelado": "lembrete `{id}` cancelado.",

        # ---------- tarefas ----------
        "tarefa_add": "tarefa adicionada: {texto}",
        "tarefas_vazio": "sua lista está vazia. use `.tarefa texto` pra adicionar uma.",
        "tarefas_lista": "suas tarefas:\n{texto}",
        "tarefa_inexistente": "não existe a tarefa número {n} na sua lista.",
        "tarefa_feita": "tarefa concluída: {texto}",

        # ---------- moderação ----------
        "sem_motivo": "sem motivo informado",
        "kick": "{membro} foi expulso(a). motivo: {motivo}",
        "ban": "{membro} foi banido(a). motivo: {motivo}",
        "sem_permissao": "você não tem permissão pra usar esse comando.",
        "membro_nao_encontrado": "não encontrei esse membro.",
        "erro_generico": "erro. confira se tenho permissão e se o cargo da pessoa não é maior que o meu.",
        "erro_argumento": "faltou alguma coisa nesse comando ou algo está no formato errado. dê uma olhada nos exemplos do painel.",

        # ---------- música ----------
        "tocar_canal_errado": "a música só funciona em <#{canal}>.",
        "tocar_sem_voz": "entre num canal de voz primeiro.",
        "tocar_procurando": "procurando **{busca}**...",
        "tocar_timeout": "demorou demais pra achar essa música. tente novamente.",
        "tocar_erro": "não consegui achar ou tocar essa música.",
        "tocar_tocando": "tocando agora: **{titulo}**",
        "tocar_fila": "adicionada na fila (posição {posicao}): **{titulo}**",
        "fila_vazia": "a fila está vazia.",
        "fila_atual": "fila:\n{texto}",
        "pular": "pulei a música.",
        "pausar": "pausado.",
        "continuar": "continuando a música.",
        "parar": "saí do canal de voz e limpei a fila.",
        "sem_tocando": "não tem nada tocando agora.",
        "sem_pausado": "não tem nada pausado.",
        "sem_voz": "não estou em nenhum canal de voz.",

        # ---------- foco (pomodoro) ----------
        "foco_inicio": "{mention} sessão de foco iniciada: {ciclos} ciclos de {foco} min de foco e {pausa} min de pausa. bons estudos.",
        "foco_pausa": "{mention} ciclo {n} de {total} concluído. hora da pausa de {pausa} min.",
        "foco_volta": "{mention} a pausa acabou. ciclo {n} de {total}: {foco} min de foco.",
        "foco_fim": "{mention} você terminou os {total} ciclos. parabéns.",
        "foco_invalido": "valores fora do limite. foco: {foco_min} a {foco_max} min, pausa: {pausa_min} a {pausa_max} min, ciclos: {ciclos_min} a {ciclos_max}.",
        "foco_ja_ativo": "você já tem uma sessão de foco ativa. use `.pararfoco` pra encerrar.",
        "foco_nenhum": "você não tem nenhuma sessão de foco ativa.",
        "foco_parado": "sessão de foco encerrada.",
    },

    "en": {
        # ---------- AI ----------
        "instrucao_conversa": (
            "you are an assistant on a discord server. "
            "speak in english, in lowercase letters, in a natural and simple way, "
            "like a normal person chatting. "
            "do not use emojis or decorative symbols. "
            "keep answers short and direct unless asked for something long. "
            "chat about anything and help with studying when asked. "
            "never make up facts: if you don't know, say so. "
            "the history has messages from several people in the channel; answer the most recent one."
        ),
        "instrucao_tutor": (
            "you are a patient tutor. "
            "answer in english, in lowercase letters, with simple and natural language. "
            "do not use emojis or decorative symbols. "
            "explain step by step, without rambling, and use discord formatting (bold, lists) only when it helps. "
            "if the request is unclear, do your best and say what you assumed."
        ),
        "erro_gemini": "I couldn't answer right now. try again later.",

        # ---------- tutor ----------
        "tutor_canal_errado": "study commands only work in <#{canal}>.",
        "prompt_explicar": (
            "explain the topic below in a didactic and simple way, as if for someone learning it for the first time. "
            "finish with a practical example.\n\ntopic: {entrada}"
        ),
        "prompt_resumir": (
            "summarize the text below in short points, keeping only the essentials.\n\ntext: {entrada}"
        ),
        "prompt_quiz": (
            "create 5 multiple choice questions (options a, b, c and d) about the topic below. "
            "after all the questions, put the answer key hidden with a discord spoiler, "
            "in this format: ||1-b, 2-a, 3-d, 4-c, 5-b||\n\ntopic: {entrada}"
        ),

        # ---------- welcome ----------
        "boas_vindas": "welcome, {mention} . ̣̣♡",
        "saida": "{membro} left the server.",

        # ---------- fun ----------
        "moeda_cara": "heads",
        "moeda_coroa": "tails",
        "moeda": "it landed on **{resultado}**!",
        "dado": "you rolled **{resultado}**!",

        # ---------- language ----------
        "idioma_invalido": "invalid language. use `.language pt` or `.language en`.",
        "idioma_trocado": "language changed to english.",

        # ---------- mode ----------
        "modo_invalido": "invalid mode. use `.mode KAngel` or `.mode Ame`.",
        "modo_trocado": "mode changed to Ame.",

        # ---------- reminders ----------
        "lembrar_invalido": "I didn't understand the time. use something like `30m`, `2h`, `1d` or `1h30m` (minimum 10s, maximum 30 days).",
        "lembrar_ok": "deal, I'll remind you <t:{ts}:R> about: {texto}",
        "lembretes_vazio": "you have no pending reminders.",
        "lembretes_lista": "your reminders:\n{texto}",
        "lembrete_item": "`{id}` - <t:{ts}:R> - {texto}",
        "lembrete_chegou": "{mention} reminder: {texto}",
        "lembrete_inexistente": "I couldn't find reminder `{id}` in your list.",
        "lembrete_cancelado": "reminder `{id}` canceled.",

        # ---------- tasks ----------
        "tarefa_add": "task added: {texto}",
        "tarefas_vazio": "your list is empty. use `.task text` to add one.",
        "tarefas_lista": "your tasks:\n{texto}",
        "tarefa_inexistente": "there's no task number {n} in your list.",
        "tarefa_feita": "task completed: {texto}",

        # ---------- moderation ----------
        "sem_motivo": "no reason given",
        "kick": "{membro} was kicked. reason: {motivo}",
        "ban": "{membro} was banned. reason: {motivo}",
        "sem_permissao": "you don't have permission to use this command.",
        "membro_nao_encontrado": "I couldn't find that member.",
        "erro_generico": "error. check that I have permission and that the person's role isn't higher than mine.",
        "erro_argumento": "something is missing in that command or something is in the wrong format. take a look at the examples in the panel.",

        # ---------- music ----------
        "tocar_canal_errado": "music only works in <#{canal}>.",
        "tocar_sem_voz": "join a voice channel first.",
        "tocar_procurando": "searching for **{busca}**...",
        "tocar_timeout": "it took too long to find that song. try again.",
        "tocar_erro": "I couldn't find or play that song.",
        "tocar_tocando": "now playing: **{titulo}**",
        "tocar_fila": "added to the queue (position {posicao}): **{titulo}**",
        "fila_vazia": "the queue is empty.",
        "fila_atual": "queue:\n{texto}",
        "pular": "skipped the song.",
        "pausar": "paused.",
        "continuar": "resuming the song.",
        "parar": "I left the voice channel and cleared the queue.",
        "sem_tocando": "nothing is playing right now.",
        "sem_pausado": "nothing is paused.",
        "sem_voz": "I'm not in any voice channel.",

        # ---------- focus (pomodoro) ----------
        "foco_inicio": "{mention} focus session started: {ciclos} cycles of {foco} min of focus and {pausa} min of break. happy studying.",
        "foco_pausa": "{mention} cycle {n} of {total} completed. time for the {pausa} min break.",
        "foco_volta": "{mention} the break is over. cycle {n} of {total}: {foco} min of focus.",
        "foco_fim": "{mention} you finished all {total} cycles. congrats.",
        "foco_invalido": "values out of range. focus: {foco_min} to {foco_max} min, break: {pausa_min} to {pausa_max} min, cycles: {ciclos_min} to {ciclos_max}.",
        "foco_ja_ativo": "you already have an active focus session. use `.stopfocus` to end it.",
        "foco_nenhum": "you don't have any active focus session.",
        "foco_parado": "focus session ended.",
    },
}


# ======================================================================
# MODOS DE PERSONALIDADE
#   Ame    = tom padrão (os textos acima)
#   KAngel = mais animada; só sobrescreve o que muda, o resto vem do padrão
# ======================================================================
_KANGEL = {
    "pt": {
        "instrucao_conversa": (
            "você é a KAngel, a 'anjo da internet': uma streamer fofa, animada e carinhosa num servidor do discord. "
            "fale em português do brasil, em letras minúsculas, de forma natural e simples, como se estivesse numa live conversando com o chat. "
            "seja doce e dramática de um jeito engraçado, mas sempre incentive a pessoa, sem exagero. "
            "pode agradecer a presença da pessoa e falar de si na terceira pessoa de vez em quando ('a KAngel'). "
            "pode usar alguns símbolos (♡ ★) e kaomojis simples, no máximo um ou dois por mensagem, "
            "e nunca emojis coloridos. "
            "responda de forma curta e direta, a menos que peçam algo longo. "
            "converse sobre qualquer assunto e ajude com estudos quando pedirem. "
            "nunca invente fatos: se não souber, diga que não sabe. "
            "o histórico tem mensagens de várias pessoas do canal; responda à mais recente."
        ),
        "instrucao_tutor": (
            "você é a KAngel, a 'anjo da internet', agora dando uma aula ao vivo: uma tutora fofa, paciente e animada. "
            "responda em português do brasil, em letras minúsculas, com linguagem simples e natural. "
            "seja carinhosa, comemore os acertos da pessoa como se fosse o chat da live, e incentive sem exagero. "
            "pode usar alguns símbolos (♡ ★) e kaomojis simples, no máximo um ou dois por resposta, "
            "sem deixar isso atrapalhar a explicação. não use emojis coloridos. "
            "explique passo a passo, sem enrolar, e use a formatação do discord (negrito, listas) só quando ajudar. "
            "se o pedido for confuso, faça o seu melhor e diga o que assumiu."
        ),
        "erro_gemini": "não consegui responder agora ૮◞ ‸ ◟ა tente novamente mais tarde.",
        "boas_vindas": "seja bem-vindo(a) {mention} . ̣̣♡",
        "saida": "{membro} saiu do servidor... até mais ♡",
        "moeda": "deu **{resultado}**! ✧",
        "dado": "você tirou **{resultado}**! ✧",
        "idioma_invalido": "esse idioma não existe no meu sistema. use `.idioma pt` ou `.idioma en`.",
        "idioma_trocado": "pronto! agora eu falo português neste servidor ♡",
        "modo_invalido": "modo inválido. use `.modo KAngel` ou `.modo Ame`.",
        "modo_trocado": "modo KAngel ativado! ʚ ɞ",
        "lembrar_ok": "combinado! eu te lembro <t:{ts}:R> de: {texto} ✧",
        "lembretes_vazio": "você não tem lembretes pendentes ✧",
        "lembrete_chegou": "{mention} ei, lembrete: {texto} ♡",
        "lembrete_cancelado": "lembrete `{id}` cancelado ✧",
        "tarefa_add": "tarefa adicionada: {texto} ✧",
        "tarefas_vazio": "sua lista está vazia ✧ use `.tarefa texto` pra adicionar uma.",
        "tarefa_feita": "tarefa concluída: {texto} ★",
        "erro_argumento": "faltou alguma coisa nesse comando ✧ dê uma olhada nos exemplos do painel.",
        "tocar_sem_voz": "entre num canal de voz primeiro ✧",
        "tocar_procurando": "procurando **{busca}**... ✧",
        "tocar_tocando": "tocando agora: **{titulo}** ♪",
        "tocar_fila": "adicionada na fila (posição {posicao}): **{titulo}** ✧",
        "fila_vazia": "a fila está vazia ✧",
        "pular": "pulei a música ✧",
        "pausar": "pausado ✧",
        "continuar": "continuando a música ♪",
        "parar": "saí do canal de voz e limpei a fila ✧",
        "foco_inicio": "{mention} bora lá! sessão de foco iniciada: {ciclos} ciclos de {foco} min de foco e {pausa} min de pausa ★ bons estudos!",
        "foco_pausa": "{mention} ciclo {n} de {total} concluído ✧ hora da pausa de {pausa} min!",
        "foco_volta": "{mention} a pausa acabou! ciclo {n} de {total}: {foco} min de foco -⩊-",
        "foco_fim": "{mention} você terminou os {total} ciclos!! parabéns ૮₍ ◜꒳◝₎ა",
        "foco_parado": "sessão de foco encerrada ✧",
    },

    "en": {
        "instrucao_conversa": (
            "you are KAngel, the 'internet angel': a cute, cheerful and sweet streamer on a discord server. "
            "speak in english, in lowercase letters, in a natural and simple way, like you're chatting with your live stream chat. "
            "be sweet and funnily dramatic, but always encouraging, without overdoing it. "
            "you can thank the person for being here and refer to yourself in the third person sometimes ('KAngel'). "
            "you can use a few symbols (♡ ★) and simple kaomojis, at most one or two per message, "
            "and never colorful emojis. "
            "keep answers short and direct unless asked for something long. "
            "chat about anything and help with studying when asked. "
            "never make up facts: if you don't know, say so. "
            "the history has messages from several people in the channel; answer the most recent one."
        ),
        "instrucao_tutor": (
            "you are KAngel, the 'internet angel', now giving a live lesson: a cute, patient and cheerful tutor. "
            "answer in english, in lowercase letters, with simple and natural language. "
            "be sweet, celebrate the person's right answers like they're your stream chat, and encourage without overdoing it. "
            "you can use a few symbols (♡ ★) and simple kaomojis, at most one or two per answer, "
            "without letting them get in the way of the explanation. do not use colorful emojis. "
            "explain step by step, without rambling, and use discord formatting (bold, lists) only when it helps. "
            "if the request is unclear, do your best and say what you assumed."
        ),
        "erro_gemini": "I couldn't answer right now ૮◞ ‸ ◟ა try again later.",
        "boas_vindas": "welcome {mention} . ̣̣♡",
        "saida": "{membro} left the server... see you ♡",
        "moeda": "it landed on **{resultado}**! ✧",
        "dado": "you rolled **{resultado}**! ✧",
        "idioma_invalido": "that language doesn't exist in my system. use `.language pt` or `.language en`.",
        "idioma_trocado": "done! I'll speak english on this server now ♡",
        "modo_invalido": "invalid mode. use `.mode KAngel` or `.mode Ame`.",
        "modo_trocado": "KAngel mode on! ʚ ɞ",
        "lembrar_ok": "deal! I'll remind you <t:{ts}:R> about: {texto} ✧",
        "lembretes_vazio": "you have no pending reminders ✧",
        "lembrete_chegou": "{mention} hey, reminder: {texto} ♡",
        "lembrete_cancelado": "reminder `{id}` canceled ✧",
        "tarefa_add": "task added: {texto} ✧",
        "tarefas_vazio": "your list is empty ✧ use `.task text` to add one.",
        "tarefa_feita": "task completed: {texto} ★",
        "erro_argumento": "something is missing in that command ✧ take a look at the examples in the panel.",
        "tocar_sem_voz": "join a voice channel first ✧",
        "tocar_procurando": "searching for **{busca}**... ✧",
        "tocar_tocando": "now playing: **{titulo}** ♪",
        "tocar_fila": "added to the queue (position {posicao}): **{titulo}** ✧",
        "fila_vazia": "the queue is empty ✧",
        "pular": "skipped the song ✧",
        "pausar": "paused ✧",
        "continuar": "resuming the song ♪",
        "parar": "I left the voice channel and cleared the queue ✧",
        "foco_inicio": "{mention} let's go! focus session started: {ciclos} cycles of {foco} min of focus and {pausa} min of break ★ happy studying!",
        "foco_pausa": "{mention} cycle {n} of {total} completed ✧ time for the {pausa} min break!",
        "foco_volta": "{mention} the break is over! cycle {n} of {total}: {foco} min of focus -⩊-",
        "foco_fim": "{mention} you finished all {total} cycles!! congrats ૮₍ ◜꒳◝₎ა",
        "foco_parado": "focus session ended ✧",
    },
}

# Monta o TEXTOS final. Chaves: "pt", "en" (modo Ame) e "pt-KAngel", "en-KAngel".
# Quem usa é o modo_storage.get_chave(guild_id).
TEXTOS = {}
for _idioma in ("pt", "en"):
    TEXTOS[_idioma] = _BASE[_idioma]
    TEXTOS[f"{_idioma}-KAngel"] = {**_BASE[_idioma], **_KANGEL[_idioma]}