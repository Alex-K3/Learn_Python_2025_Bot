from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ChatMemberUpdated
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, KICKED, or_f
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboards import main_reply, get_number, get_local
import app.database.users as db_user
import app.weather as wt
from config import logger


router = Router()


class Registry(StatesGroup):
    first_name = State()
    last_name = State()
    birthday = State()
    city = State()
    phone = State()
    email = State()


class Weather(StatesGroup):
    local = State()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await db_user.set_user(message.from_user.id, message.from_user.username, status='Active')
    await message.answer("Чтобы бот работал корректно, предлагаем вам пройти регистрацию /registry или часть функционала будет недоступна")


@router.message(or_f(Command('registry'), F.text == "Регистрация"))
async def command_registry_handler(message: Message, state: FSMContext):
    await message.answer('Какое у вас имя?')
    await state.set_state(Registry.first_name)


@router.message(Registry.first_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer('Какая у вас фамилия?')
    await state.set_state(Registry.last_name)


@router.message(Registry.last_name)
async def register_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Укажите дату вашего рождения в формате ДД.ММ.ГГГГ: ')
    await state.set_state(Registry.birthday)


@router.message(Registry.birthday)
async def register_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer('Укажите ваш город проживания: ')
    await state.set_state(Registry.city)


@router.message(Registry.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Поделитесь вашим номером телефона, кнопкой ниже', reply_markup=get_number)
    await state.set_state(Registry.phone)


@router.message(Registry.phone, F.contact)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Введите ваш email', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registry.email)


@router.message(Registry.email)
async def register_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()

    await db_user.update_user(message.from_user.id, data["first_name"], data["last_name"], data["birthday"], data["city"], data["phone"], data["email"])
    await message.answer(
        "Регистрация успешно пройдена.\n"
        "Ваши данные:\n"
        f"Имя - {data['first_name']}\n"
        f"Фамилия - {data['last_name']}\n"
        f"Дата рождения - {data['birthday']}\n"
        f"Город проживания - {data['city']}\n"
        f"Номер телефона - {data['phone']}\n"
        f"И ваша электронная почта - {data['email']}\n"
        "успешно сохранены"
    )
    await state.clear()


@router.message(or_f(Command('help'), F.text == "Помощь"))
async def command_help_handler(message: Message):
    await message.answer("Help yourself", reply_markup=main_reply)


@router.message(or_f(Command('support'), F.text == "Поддержка"))
# @router.message(F.text == "Поддержка")
async def command_support_handler(message: Message):
    await message.answer("Developer and author bot: @Aleeex_K. If your have question, please send message author.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(or_f(Command('weather'), F.text == "Погода"))
async def command_weather_handler(message: Message, state: FSMContext):
    await state.set_state(Weather.local)
    await message.answer("Share your geo, please", reply_markup=get_local)


@router.message(Weather.local)
async def weather_local(message: Message, state: FSMContext):
    await state.update_data(local_lat=message.location.latitude)
    await state.update_data(local_lon=message.location.longitude)
    data = await state.get_data()
    await message.answer(wt.main_bot(data["local_lat"], data["local_lon"]), reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    await db_user.set_user(event.from_user.id, event.from_user.username, status='Inactive')
    logger.info(f'Пользователь {event.from_user.id} заблокировал бота')


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )
