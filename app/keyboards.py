from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Регистрация'), KeyboardButton(text='Погода')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Поддержка')]
], resize_keyboard=True, input_field_placeholder='Please select the menu item...')


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Send phone number', request_contact=True)]], resize_keyboard=True)
get_local = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Send your GEO', request_location=True)]], resize_keyboard=True)

