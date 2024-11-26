from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from constants import ButtonsMainMenu


text_on_buttons_main = [
    ButtonsMainMenu.FEATURES.value, ButtonsMainMenu.MONITORING.value,
    ButtonsMainMenu.MANAGEMENT.value, ButtonsMainMenu.DOWNLOAD_COFIG.value
]


def create_buttons_main_menu(content: list) -> ReplyKeyboardBuilder:
    menu = ReplyKeyboardBuilder()
    for btn in content:
        menu.add(KeyboardButton(text=btn.capitalize()))
    menu.adjust(1, 3)
    return menu


main_menu = create_buttons_main_menu(text_on_buttons_main)
