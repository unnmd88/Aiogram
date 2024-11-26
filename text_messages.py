from enum import Enum


from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag, Italic, Underline, Text
)

from keyboards.main_keyboard import text_on_buttons_main
from constants import ButtonsMainMenu


new_line = '\n'
help = as_list(
    Underline(Bold('Функционал, доступный на данный момент')),
    Italic('1. Получить состояние ДК.'),
    f"Для получения состояния ДК необходимо отправить сообщение боту "
    f"в формате:"
    f"\n<номер СО или ip> <?>. Номер СО должен соответствовать номеру из Дира"
    f"\nВажно: номера СО/ip, а также знак ? в конце должны быть разделены пробелом. "
    f"Пример запроса состояния по номеру для СО 11:"
    f"\n11 ?"
    f"\nПример запроса состояния по  ip 10.45.154.19:"
    f"\n10.45.154.19 ?"
    f"\nДоступные опции:"
    f"\n * несколько СО в одном запросе. Пример:"
    f"\n11 2390 2412 ?"
    f"\n * комбинировать ip/номер CO в одном запросе. Пример:"
    f"\n11 10.45.154.19 2390 ?",
    Italic('2. Получить состояние ДК с расширенными параметрами.'),
    f"В данный момент реализовано только для ДК Peek."
    f"\n Формат сообщения(добавляется еще один ? знак):"
    f"\n<номер СО или ip> <??>"
    f"\nПример по номеру:"
    f"\n413-P ??"
    f"\nПример по ip:"
    f"\n10.45.54.19 ??"
    f"\nДоступные опции:"
    f"\n * Один запрос для одного ДК"
)

available_options = (
    f"Тестовое сообщение возможностей"
)

start_command_text = (
    f"Ознакомиться с функционалом можно нажав необходимую кнопку, " 
    f"либо отправить одно из сообщений: "
    f"{new_line}"
    f"{new_line.join([txt.capitalize() for txt in text_on_buttons_main])}"
)


class AvailableTexts(Enum):
    available_texts = {
        '/start': start_command_text,
        ButtonsMainMenu.FEATURES.value: available_options
    }


def get_text(word: str) -> str:
    return AvailableTexts.available_texts.value.get(word.lower(), '...')



