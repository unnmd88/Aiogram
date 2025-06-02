from contextlib import nullcontext as does_not_raise
import pytest

from parsers import (
    get_tokens,
    Message, GetStateMessageParser
)


@pytest.mark.parametrize(
    'message, expected',
    [
        ('? 11', ('?', '11')),
        ('? 11 3320 1251', ('?', '11', '3320', '1251')),
    ]
)
def test_get_tokens(message, expected):
    assert get_tokens(message) == expected


@pytest.fixture
def good_messages():
    return  [
        ('? 11', Message('? 11')),
        ('? 11 3320 1515', Message('? 11 3320 1515')),
    ]

@pytest.fixture
def bad_messages():
    return  ['?11,']


class TestMessage:

    def test_eq(self, good_messages):
        for msg, obj in good_messages:
            assert Message(msg).message == obj.message

    def test_entity(self, good_messages):
        for msg, obj in good_messages:
            assert Message(msg).entity == obj.entity
            assert Message(msg).entity == get_tokens(msg)[0]

    @pytest.mark.parametrize(
        "msg, expected",
        [
            ('? 1251 144,', True),
            ('?1251144,', False),
            ('?,', False),
            ('?', False),
        ],
    )
    def test_is_valid(self, msg, expected):
        assert Message(msg).is_valid() == expected

    @pytest.mark.parametrize(
        "msg, expected",
        [
            ('? 1251 144', ('?', '1251', '144')),
            ('? 1 2 5', ('?', '1', '2', '5')),
        ],
    )
    def test_tokens(self, msg, expected):
        assert Message(msg).tokens == expected


@pytest.mark.parametrize(
    "instance, expected",
    [
        (GetStateMessageParser(Message('? 1251 144')), True),
        (GetStateMessageParser(Message('?1251144,')), False),
    ],
)
class TestMessageParser:

    def test_validate(self, instance: GetStateMessageParser, expected):
        assert instance.validate() == expected


