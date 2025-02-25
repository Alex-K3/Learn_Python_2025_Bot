from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboards import main_reply, get_number, get_local
import app.database.requests as rq
import app.weather as wt

router = Router()


class Registry(StatesGroup):
    name = State()
    age = State()
    number = State()


class Weather(StatesGroup):
    local = State()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer("Hello! What you're gonna do?", reply_markup=main_reply)


@router.message(Command('help'))
async def command_help_handler(message: Message):
    await message.answer("Help yourself", reply_markup=main_reply)


@router.message(Command('support'))
async def command_support_handler(message: Message):
    await message.answer("Developer and author bot: @Aleeex_K. If your have question, please send message author.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('weather'))
async def command_weather_handler(message: Message, state: FSMContext):
    await state.set_state(Weather.local)
    await message.answer("Share your geo, please", reply_markup=get_local)


@router.message(Weather.local)
async def weather_local(message: Message, state: FSMContext):
    await state.update_data(local_lat=message.location.latitude)
    await state.update_data(local_lon=message.location.longitude)
    data = await state.get_data()
    await message.answer(wt.main(data["local_lat"], data["local_lon"]), reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command('registry'))
async def command_registry_handler(message: Message, state: FSMContext):
    await state.set_state(Registry.name)
    await message.answer('What`s your name?')


@router.message(Registry.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registry.age)
    await message.answer('How old you are?')


@router.message(Registry.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Registry.number)
    await message.answer('Enter your phone number', reply_markup=get_number)


@router.message(Registry.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    try:
        age = int(data["age"])
    except ValueError:
        await message.answer("Возраст должен быть числом. Попробуйте снова.")
        return

    await rq.update_user(message.from_user.id, data["name"], age, data["number"])
    await message.answer(f'Your name: {data["name"]}\nYour age: {data["age"]}\nYour number: {data["number"]}',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(F.text == "Помощь")
async def button_help_handler(message: Message):
    await command_help_handler(message)


@router.message(F.text == "Поддержка")
async def button_support_handler(message: Message):
    await command_support_handler(message)


@router.message(F.text == "Погода")
async def button_weather_handler(message: Message, state: FSMContext):
    await command_weather_handler(message, state)


@router.message(F.text == "Регистрация")
async def button_registry_handler(message: Message, state: FSMContext):
    await command_registry_handler(message, state)


@router.message()
async def echo_handler(message: Message) -> None:
    await message.send_copy(chat_id=message.chat.id)
