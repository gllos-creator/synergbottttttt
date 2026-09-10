import os import html import asyncio import logging
from aiogram import Bot, Dispatcher, F from aiogram.filters import CommandStart from aiogram.types import Message, CallbackQuery from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = os.getenv("BOT_TOKEN") GROUP_ID = int(os.getenv("GROUP_ID"))
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN) dp = Dispatcher()
Связывает сообщение в группе с пользователем,
который отправил его боту
users = {}
def menu(): return InlineKeyboardMarkup( inline_keyboard=[ [ InlineKeyboardButton( text="✉️ Отправить анонимно", callback_data="send_anonymous" ) ] ] )
@dp.message(CommandStart()) async def start(message: Message): await message.answer( "👋 Привет!\n\n" "Отправь мне сообщение, и я опубликую его в группе " "анонимно.\n\n" "Твоё имя и профиль участникам группы показаны не будут.", reply_markup=menu() )
@dp.callback_query(F.data == "send_anonymous") async def anonymous_button(callback: CallbackQuery): await callback.message.answer( "✍️ Просто отправь мне сообщение.\n\n" "Можно отправить текст, фото, видео, голосовое " "или документ." ) await callback.answer()
@dp.message() async def receive_message(message: Message):
# Работаем только с личными сообщениями боту
if message.chat.type != "private":
    return

sent = None

# ТЕКСТ
if message.text:

    text = html.escape(message.text)

    sent = await bot.send_message(
        GROUP_ID,
        f"📩 <b>Анонимное сообщение</b>\n\n{text}",
        parse_mode="HTML"
    )

# ФОТО
elif message.photo:

    caption = html.escape(message.caption or "")

    text = "📩 <b>Анонимное сообщение</b>"

    if caption:
        text += f"\n\n{caption}"

    sent = await bot.send_photo(
        GROUP_ID,
        message.photo[-1].file_id,
        caption=text,
        parse_mode="HTML"
    )

# ВИДЕО
elif message.video:

    caption = html.escape(message.caption or "")

    text = "📩 <b>Анонимное сообщение</b>"

    if caption:
        text += f"\n\n{caption}"

    sent = await bot.send_video(
        GROUP_ID,
        message.video.file_id,
        caption=text,
        parse_mode="HTML"
    )

# ГОЛОСОВОЕ
elif message.voice:

    sent = await bot.send_voice(
        GROUP_ID,
        message.voice.file_id,
        caption="📩 Анонимное голосовое"
    )

# ДОКУМЕНТ
elif message.document:

    sent = await bot.send_document(
        GROUP_ID,
        message.document.file_id,
        caption="📩 Анонимный документ"
    )

# СТИКЕР
elif message.sticker:

    sent = await bot.send_sticker(
        GROUP_ID,
        message.sticker.file_id
    )

else:

    await message.answer(
        "❌ Этот тип сообщения пока не поддерживается."
    )

    return

# Запоминаем отправителя
users[sent.message_id] = message.from_user.id

await message.answer(
    "✅ Сообщение отправлено анонимно."
)
async def main():
print("🤖 Бот запущен!")

await dp.start_polling(bot)
if name == "main": asyncio.run(main())
