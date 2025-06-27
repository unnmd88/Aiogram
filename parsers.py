from abc import abstractmethod
from collections import deque
from collections.abc import Sequence
from enum import StrEnum
from typing import Type

import nltk

from messages import (
    EntitySymbols,
    ErrorMessages
)

nltk.download('punkt_tab')



class Entities(StrEnum):
    get_states = '?'



def get_tokens(text: str, type_container: Type[Sequence[str]] = tuple) -> Sequence[str]:
    if not isinstance(type_container, list):
        return type_container(t for t in text.split())
    return text.split()


class BaseMessage:

    _entity_index: int = 0
    _max_args: int = 10
    _args_slice = slice(1, None)


    def __init__(self, message):
        self._message = message
        self._tokens = get_tokens(self._message)
        self._args = self.get_args()
        self._errors = deque(maxlen=8)

    def __eq__(self, other):
        if isinstance(other, BaseMessage):
            return self._message == other.message
        return NotImplemented

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'message={self._message!r} '
            f'tokens={self._tokens!r} '
            f'errors={self._errors!r} '
            f'entity={self.entity!r} '
            f'args={self.args})'
        )

    @property
    def message(self):
        return self._message

    @property
    def tokens(self):
        return self._tokens

    @property
    def entity(self):
        if len(self._tokens) > 1:
            return self._tokens[self._entity_index]

    @property
    def args(self):
        return self._args

    def get_args(self) -> Sequence[str]:
        try:
            return self._tokens[self._args_slice]
        except IndexError:
            return []

    @property
    def is_valid(self):
        return bool(self._errors)

    def validate_and_put_error_if_has(self) -> bool:
        self._errors.clear()
        if len(self._tokens) < 2:
            self._errors.append('Некорректное сообщение')
            return self.is_valid

        if len(self._args) == 0:
            self._errors.append(f'Не предоставлены аргументы для команды')
        elif len(self._args) > self._max_args:
            self._errors.append(f'Неверное количество аргументов: {len(self._args)}')
        try:
            Entities(self.entity)
        except ValueError:
            self._errors.append(f'Недопустимый тип команды: {self.entity}')
        return self.is_valid



# class MessageParser:
#
#     entity_symbol: str
#
#     def __init__(self, message: Message):
#         self._message = message
#         self._errors = deque(maxlen=8)
#         self.validate()
#
#     def __repr__(self):
#         return (
#             f'self._message: {self._message.message}\n'
#             f'self._errors: {self._errors}\n'
#             f'self._tokens: {self._message.tokens}'
#         )
#
#     @property
#     def message(self) -> Message:
#         return self._message
#
#     @property
#     def entity(self):
#         return self._message.entity
#
#     @property
#     def errors(self):
#         return self._errors
#
#     def validate(self) -> bool:
#         try:
#             if not self._message.is_valid():
#                 raise ValueError
#             EntitySymbols(self.entity)
#         except ValueError:
#             self.put_error(ErrorMessages.bad_entity)
#         return False if self._errors else True
#
#     def put_error(self, msg: str | Exception):
#         self._errors.append(str(msg))
#
#     def is_valid(self) -> bool:
#         return bool(self._errors)
#
#
# class GetStateMessageParser(MessageParser):
#
#     entity_symbol = '?'
#
#     def get_hosts(self) -> Sequence[str]:
#         return self.message.args


if __name__ == '__main__':
    print(nltk.word_tokenize(''))
    print('?1251144'.split())
    get_states = BaseMessage('? 12511 44')
    get_states.validate_and_put_error_if_has()

    print(get_states)
    # print(type(get_states.tokens))



