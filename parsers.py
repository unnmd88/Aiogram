from collections import deque
from collections.abc import Sequence
from typing import Type

import nltk

from messages import (
    EntitySymbols,
    ErrorMessages
)

nltk.download('punkt_tab')


def get_tokens(text: str, type_container: Type[Sequence[str]] = tuple) -> Sequence[str]:
    if not isinstance(type_container, list):
        return type_container(t for t in text.split())
    return text.split()


class Message:
    def __init__(self, message):
        self._message = message
        self._tokens = get_tokens(self._message)

    def __eq__(self, other):
        if isinstance(other, Message):
            return self._message == other.message
        return NotImplemented

    def __len__(self):
        return len(self._tokens)

    @property
    def message(self):
        return self._message

    def is_valid(self):
        return len(self._tokens) > 2

    @property
    def tokens(self):
        return self._tokens

    @property
    def entity(self):
        try:
            return self._tokens[0]
        except IndexError:
            return None

    @property
    def args(self):
        return self._tokens[1:]


class MessageParser:

    entity_symbol: str

    def __init__(self, message: Message):
        self._message = message
        self._errors = deque(maxlen=8)
        self.validate()

    def __repr__(self):
        return (
            f'self._message: {self._message.message}\n'
            f'self._errors: {self._errors}\n'
            f'self._tokens: {self._message.tokens}'
        )

    @property
    def message(self) -> Message:
        return self._message

    @property
    def entity(self):
        return self._message.entity

    @property
    def errors(self):
        return self._errors

    def validate(self) -> bool:
        try:
            if not self._message.is_valid():
                raise ValueError
            EntitySymbols(self.entity)
        except ValueError:
            self.put_error(ErrorMessages.bad_entity)
        return bool(self._errors)

    def put_error(self, msg: str | Exception):
        self._errors.append(str(msg))


class GetStateMessageParser(MessageParser):

    entity_symbol = '?'

    def get_hosts(self) -> Sequence[str]:
        return self.message.args


if __name__ == '__main__':
    print(nltk.word_tokenize(''))
    parser = GetStateMessageParser(message=Message('?1251144'))
    print(parser)
    print(type(parser.message.tokens))



