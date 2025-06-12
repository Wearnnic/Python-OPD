import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

logging.basicConfig(level=logging.INFO)

API_TOKEN = '8187319698:AAFBwQbTitqZAztaOsHsqn5XIJl-z6J_qcE'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)

class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_race_type = State()

@router.message(Command("start", "help"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏃‍♂️ Добро пожаловать на марафон! 🏃‍♀️\n"
        "Для регистрации введите ваше ФИО:"
    )
    await state.set_state(RegistrationStates.waiting_for_name)

@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("❗ ФИО не может быть пустым. Пожалуйста, введите ваше ФИО:")
        return
    await state.update_data(name=name)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="🏅 5 км"),
                types.KeyboardButton(text="🥇 10 км"),
            ],
            [
                types.KeyboardButton(text="🎽 Полумарафон"),
                types.KeyboardButton(text="🏆 Марафон"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите тип забега:", reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_race_type)

@router.message(RegistrationStates.waiting_for_race_type)
async def process_race_type(message: types.Message, state: FSMContext):
    race_type = message.text
    valid_races = ["🏅 5 км", "🥇 10 км", "🎽 Полумарафон", "🏆 Марафон"]
    if race_type not in valid_races:
        await message.answer("❗ Пожалуйста, выберите тип забега из предложенных вариантов.")
        return
    data = await state.get_data()
    name = data.get("name")

    # Сохраняем регистрацию в файл
    with open("registrations.txt", "a", encoding="utf-8") as f:
        f.write(f"{name} - {race_type}\n")

    await message.answer(
        f"✅ Спасибо за регистрацию!\n\n"
        f"ФИО: {name}\n"
        f"Тип забега: {race_type}",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
