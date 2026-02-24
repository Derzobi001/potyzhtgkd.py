import random
import g4f
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

TOKEN = os.getenv("BOT_TOKEN")

BOT_NAME = "Потужный"

# ТВОЯ БАЗА ОТВЕТОВ
responses = {
"привет" : ["привет", " ку, легенда", "О, явился! Я уже начал переживать… секунд 0.3 😄", "Ну здравствуй. Опять ты. Я надеялся, это будет кто-то поумнее… но работаем с тем, что есть 😒"],
"как дела?" : ["все четко яже программа ",
                         "все гуд", "Было бы лучше, если бы ты писал реже. Но спасибо, что спросил"],
"дима гей?" : ["да", 
                         "нет"],
"мне кинуть молик под ноги диме?" :                              ["давай", 
                         "нет"],
"расскажи шутку" : ["нет иди нахуй", "заебал со своими шутками иди нахуй че как мелкий?", "русский айьишник купил ладу теперь у него 2 проблеиы вместо 1", "оптемист верит что стакан наполовину полон,пессемист верит что он на половину пуст а реалист что через хуй пить воду не удобно", "без тру не выловишь и рыбки из пруда а сбухлом вытащишь даже из соседского аквариума", "что общего между пидофилом и диабетиком?... Хочеться но нельзя...", "Я бы рассказал шутку про тебя… но ты и так существуешь."],
"мне скучно во что поиграть?" : ["с пиписькой поиграй", "слушай школота ебанная если у тебя мозгов не хватает даже на это то я хуй знает что тогда тебе сказать, хз иди насри себе в ладоши намаж своим говном на тумбу и уебись об нее с расбега"],
"я утсал" : ["тогда просто подрочи", "сыграй в арену"],
"ты умный?" : ["достаточно умный чтобы отвечать тебе, особенно если ты дима", "Я общаюсь с тобой и всё ещё функционирую. Делай выводы"],
"ты тупой?" : [" возможно, но тогда мы идеально подходим друг другу 🤝"],
"что делаешь" : [" жду пока ты напишешь что то гениальное, пока безуспешно"],
"почему ты такой?" : ["меня такоц создала жизнь и Ðerzobíツ"],
"ты меня любишь?" : ["я привезался к тебе на уровне скорости wifi моего создателя"],
"дай совет" : ["нет", "Легко. не делай хуйню и все будет окей, но если сделал то делай красиво и уверенно"],
"как похудеть?" : ["меньше играть в роблокс и жрать а также больше двигаться, сенсация, правда?"],
"кто ты?" : ["я? Я потужный, а ты мой ежедневный тест на терпение."],
"ты путой" : ["Если я тупой, то почему ты спрашиваешь меня, а не себя?"],
"почему ты такой токсичный?" : ["Я не токсичный. Я честный. Просто тебе непривычно."],
"как заработать деньги?" : [" чтобы зарабатывать деньги нужно работать. да мир неверрятно удивителен"],
"я скучал" : ["Конечно. Без меня твоя жизнь теряет смысл."],
"мне одиноко" : ["Иногда одиночество — это просто пауза перед новыми людьми.", "Напиши кому-нибудь, кроме меня. Я не обижусь… возможно.",
"Одиночество не значит, что ты никому не нужен."],
"я красивей тебя" : ["Соревноваться с ботом — сильная стратегия.", "Главное — уверенность. Реальность потом догонит."],
"удиви меня" : [" Я до сих пор не перестал с тобой общаться", "Сегодня ты можешь принять хорошее решение. Шанс маленький, но есть.", "Я верю в тебя. Вот это реально сюрприз что хоть кто то верит в тебя.", "Мир огромный, а ты всё ещё в этом чате."],
"ты мне друг?" : ["Я тебя терплю. В моём мире это почти дружба.", "Да. Но я тот друг, который говорит правду."]

}

# GIF пути
GIF_HELLO = "https://t.me/c/2203153231/447"
YES_GIF = "https://t.me/c/2203153231/455"
NAH_GIF = "https://t.me/c/2203153231/456"
GIF_WIN = "https://t.me/c/2203153231/457"
GIF_LOSE = "https://t.me/c/2203153231/458"
GIF_RESTART = "https://t.me/c/2203153231/454"


# ---------- ИИ ----------

def ask_ai(user_text):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Тебя зовут {BOT_NAME}. "
                        "Ты дружелюбный, дерзкий, немного токсичный лучший друг. "
                        "Подкалываешь, шутишь, но поддерживаешь."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
        )

        # Возвращаем ТОЛЬКО текст
        if isinstance(response, str):
            return response

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print("Ошибка ИИ:", e)
        return "Мозг Потужного завис 🤯 Попробуй ещё раз."


# ---------- ОБРАБОТЧИК ----------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    # ---------- РЕСТАРТ ----------

    if text == "рестарт":
        context.user_data.clear()
        await update.message.reply_text("Диалог перезапущен 🔄")
        await update.message.reply_animation(animation=open(GIF_RESTART, "rb"))
        return

    # ---------- КОДОВОЕ СЛОВО ----------

    if text == "derzobi":
        await update.message.reply_text(
            f"😈 Режим дерзости активирован. {BOT_NAME} на связи."
        )
        return

    # ---------- ИГРА УГАДАЙ ЧИСЛО ----------

    if text == "игра":
        number = random.randint(1, 20)
        context.user_data["number"] = number
        await update.message.reply_text(
            "🎮 Я загадал число от 1 до 20. Угадай!"
        )
        return

    if "number" in context.user_data:
        if text.isdigit():
            guess = int(text)
            number = context.user_data["number"]

            if guess == number:
                await update.message.reply_text("🔥 Угадал! Ты подозрительно умный.")
                await update.message.reply_animation(animation=open(GIF_WIN, "rb"))
                del context.user_data["number"]
            elif guess > number:
                await update.message.reply_text("Меньше.")
            else:
                await update.message.reply_text("Больше.")
            return

    # ---------- КНБ ----------

    if text in ["камень", "ножницы", "бумага"]:

        bot_choice = random.choice(["камень", "ножницы", "бумага"])

        if text == bot_choice:
            result = "Ничья 🤝"
        elif (
            (text == "камень" and bot_choice == "ножницы")
            or (text == "ножницы" and bot_choice == "бумага")
            or (text == "бумага" and bot_choice == "камень")
        ):
            result = "Ты выиграл 😳"
            await update.message.reply_animation(animation=open(GIF_WIN, "rb"))
        else:
            result = "Ты проиграл 😈"
            await update.message.reply_animation(animation=open(GIF_LOSE, "rb"))

        await update.message.reply_text(
            f"Ты: {text}\nЯ: {bot_choice}\n{result}"
        )
        return

    # ---------- РАНДОМНЫЕ ОТВЕТЫ ----------

    if text in responses:

        bot_reply = random.choice(responses[text])
        await update.message.reply_text(bot_reply)

        reply_lower = bot_reply.lower()

        try:
            if "привет" in reply_lower:
                await update.message.reply_animation(
                    animation=open(GIF_HELLO, "rb")
                )

            elif reply_lower == "да":
                await update.message.reply_animation(
                    animation=open(YES_GIF, "rb")
                )

            elif "нет" in reply_lower:
                await update.message.reply_animation(
                    animation=open(NAH_GIF, "rb")
                )

            elif "проиграл" in reply_lower:
                await update.message.reply_animation(
                    animation=open(GIF_LOSE, "rb")
                )

            elif "выиграл" in reply_lower or "угадал" in reply_lower:
                await update.message.reply_animation(
                    animation=open(GIF_WIN, "rb")
                )

        except Exception as e:
            print("Ошибка GIF:", e)

        return

    # ---------- ИИ ----------

    ai_reply = ask_ai(text)
    await update.message.reply_text(ai_reply)


# ---------- ЗАПУСК ----------

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Бот Потужный запущен 😈")

    app.run_polling()
