import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import (
Message,
CallbackQuery,
InlineKeyboardMarkup,
InlineKeyboardButton,
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

MIN_PLAYERS = 6
WAIT_TIME = 30

lobbies = {}

@dp.message(Command("start"))
async def start_cmd(message: Message):
await message.answer(
"Привет! Чтобы играть в мафию, сначала напиши боту /start, затем заходи в группу."
)

@dp.message(Command("mafia"))
async def create_game(message: Message):
if message.chat.type == ChatType.PRIVATE:
return

```
chat_id = message.chat.id

if chat_id in lobbies:
    await message.answer("Игра уже создается.")
    return

lobbies[chat_id] = {
    "players": {},
    "started": False
}

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Присоединиться",
                callback_data=f"join:{chat_id}"
            )
        ]
    ]
)

await message.answer(
    f"🎭 Лобби создано\n\n"
    f"Минимум игроков: {MIN_PLAYERS}\n"
    f"Старт через: {WAIT_TIME} сек",
    reply_markup=kb
)

asyncio.create_task(start_timer(chat_id))
```

async def start_timer(chat_id):
await asyncio.sleep(WAIT_TIME)

```
if chat_id not in lobbies:
    return

players = lobbies[chat_id]["players"]

if len(players) < MIN_PLAYERS:
    await bot.send_message(
        chat_id,
        f"❌ Недостаточно игроков.\n"
        f"Нужно минимум {MIN_PLAYERS}.\n"
        f"Сейчас: {len(players)}"
    )
    del lobbies[chat_id]
    return

await bot.send_message(
    chat_id,
    f"🎭 Игра началась!\n"
    f"Игроков: {len(players)}"
)

roles = ["Мафия", "Доктор", "Комиссар"]
while len(roles) < len(players):
    roles.append("Мирный")

import random
random.shuffle(roles)

for (user_id, username), role in zip(players.items(), roles):
    try:
        await bot.send_message(
            user_id,
            f"Ваша роль: {role}"
        )
    except:
        pass
```

@dp.callback_query(F.data.startswith("join:"))
async def join_game(callback: CallbackQuery):
chat_id = int(callback.data.split(":")[1])

```
if chat_id not in lobbies:
    await callback.answer("Лобби не найдено")
    return

user = callback.from_user

lobbies[chat_id]["players"][user.id] = (
    user.username or user.full_name
)

await callback.answer("Вы присоединились")
```

async def main():
await dp.start_polling(bot)

if **name** == "**main**":
asyncio.run(main())
