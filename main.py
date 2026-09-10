import os import asyncio import html import logging
from aiogram import Bot, Dispatcher, F from aiogram.filters import CommandStart from aiogram.types import Message, CallbackQuery from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = os.environ["BOT_TOKEN"] GROUP_ID = int(os.environ["GROUP_ID"])
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN) dp = Dispatcher()
def get_keyboard(): return InlineKeyboardMarkup( inline_keyboard=[ [ InlineKeyboardButton( text="✉️ Отправить анонимно", callback_data="anonymous" ) ] ] )
@dp.message(CommandStart()) async def start(message: Message): await message.answer( "👋 Привет!\n\n" "Отправь мне сообщение, и я опубликую его в группе анонимно.\n" "Твоё имя участникам группы показано не будет.", reply_markup=get_keyboard() )
@dp.callback_query(F.data == "anonymous") async def anonymous(callback: CallbackQuery): await callback.message.answer( "✍️ Отправь мне сообщение." ) await callback.answer()
@dp.message() async def receive(message: Message): if message.chat.type != "private": return
if message.text:
    text = html.escape(message.text)

    await bot.send_message(
        GROUP_ID,
        "📩 <b>Анонимное сообщение</b>\n\n" + text,
        parse_mode="HTML"
    )

elif message.photo:
    caption = html.escape(message.caption or "")

    await bot.send_photo(
        GROUP_ID,
        message.photo[-1].file_id,
        caption="📩 <b>Анонимное сообщение</b>\n\n" + caption,
        parse_mode="HTML"
    )

elif message.video:
    caption = html.escape(message.caption or "")

    await bot.send_video(
        GROUP_ID,
        message.video.file_id,
        caption="📩 <b>Анонимное сообщение</b>\n\n" + caption,
        parse_mode="HTML"
    )

elif message.voice:
    await bot.send_voice(
        GROUP_ID,
        message.voice.file_id,
        caption="📩 Анонимное голосовое"
    )

elif message.document:
    await bot.send_document(
        GROUP_ID,
        message.document.file_id,
        caption="📩 Анонимный документ"
    )

elif message.sticker:
    await bot.send_sticker(
        GROUP_ID,
        message.sticker.file_id
    )

else:
    await message.answer(
        "❌ Этот тип сообщения пока не поддерживается."
    )
    return

await message.answer(
    "✅ Сообщение отправлено анонимно."
)
async def main(): print("🤖 Бот запущен!") await dp.start_polling(bot)
if name == "main": asyncio.run(main())
