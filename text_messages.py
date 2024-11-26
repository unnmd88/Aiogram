from enum import Enum
from typing import Any

from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag, Italic, Underline, Text
)

from keyboards.main_keyboard import text_on_buttons_main
from constants import ButtonsMainMenu

new_line = '\n'
available_options = as_list(
    Underline(Bold('Функционал, доступный на данный момент')),
    '1. Получить состояние ДК',
    '2. Загрузка конфига Swarco',
)

monitoring_text = as_list(
    Underline(Bold('----Мониторинг----')),
    f"Для получения состояния ДК необходимо отправить сообщение боту "
    f"в формате:"
    f"\n<номер СО или ip> <?>. Номер СО должен соответствовать номеру объекта из Дира."
    f"\nВажно: номера СО/ip, а также знак ? в конце должны быть разделены пробелом. ",
    Italic('Примеры.'),
    f"Запрос состояния по номеру объекта для СО 11:"
    f"\n11 ?"
    f"\nЗапрос состояния по для нашего лабовского Пика ip 10.45.154.19:"
    f"\n10.45.154.19 ?"
    f"\nДоступа возможность получения состояния нескольких ДК в одном запросе:"
    f"\n11 2390 2412 ?"
    f"\nТакже возможно комбинировать ip/номер CO в одном запросе. Пример:"
    f"\n11 10.45.154.19 2390 ?",
    f"\n"
    f"Для ДК Peek реализовано получение расширенной информации о состоянии "
    f"\n Формат сообщения(добавляется еще один ? знак):"
    f"\n<номер СО или ip> <??>",
    Italic('Примеры.'),
    f"По номеру:"
    f"\n2390 ??"
    f"\nПо ip адресу:"
    f"\n10.45.54.19 ??"
    f"\nВ данный момент для доступна возможность запроса для одного ДК за раз"
)

management_text = (
    f"В данный момент не реализовано"
)

start_command_text = (
    f"Ознакомиться с функционалом можно нажав необходимую кнопку, "
    f"либо отправить одно из сообщений: "
    f"{new_line}"
    f"{new_line.join([txt.capitalize() for txt in text_on_buttons_main])}"
)

download_config_text = as_list(
    Underline(Bold('----Загрузка конфига----')),
    f"Для загрузки конфига необходимо отправить сообщение боту "
    f"в формате:"
    f"\n<номер СО или ip> <конфиг>. Номер СО должен соответствовать номеру объекта из Дира."
    f"\nВажно: номера СО/ip, а также знак ? в конце должны быть разделены пробелом. ",
    Italic('Примеры.'),
    f"По номеру:"
    f"\n11 конфиг"
    f"\nПо ip адресу:"
    f"\n10.45.154.16 конфиг"
    f"\nВ данный момент для доступна возможность запроса для одного ДК за раз"
)


class AvailableTexts(Enum):
    available_texts = {
        '/start': start_command_text,
        ButtonsMainMenu.FEATURES.value: available_options,
        ButtonsMainMenu.MONITORING.value: monitoring_text,
        ButtonsMainMenu.MANAGEMENT.value: management_text,
        ButtonsMainMenu.DOWNLOAD_COFIG.value: download_config_text,
    }


def get_text(word: str) -> Any:
    if not word:
        return '...'
    return AvailableTexts.available_texts.value.get(word.lower(), '...')
