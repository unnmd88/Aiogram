from enum import StrEnum


class EntitySymbols(StrEnum):
    get_state = '?'


class ReplyMessages(StrEnum):
    state_entity = (
        f'Текущий статус дк. В начале сообщения должен быть '
        f'индикатор "?" и далее номера/ip объектов через пробел.\n'
        f'Пример сообщения для получения статуса для СО 11:\n'
        f'? 11\n'
        f'Пример сообщения для получения статуса нескольких СО:\n'
        f'? 11 155 3412\n'
        f'----------------------------------------------------'
    )


class ErrorMessages(StrEnum):
    bad_entity = (
        f'Неверный тип запроса. Используйте следующие типы:\n'
        f'< {EntitySymbols.get_state} >\n'
        f'{ReplyMessages.state_entity}'
    )