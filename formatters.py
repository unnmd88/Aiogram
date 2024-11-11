import enum
import json
from enum import Enum
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

class KeysAndFlags(Enum):
    JSON = {
        '-j', '-json', 'j', '-j'
    }
    TEXT = 'text'


class TextFormatter:

    @staticmethod
    def define_resonse_format(flag):

        return KeysAndFlags.JSON if flag in KeysAndFlags.JSON.value else KeysAndFlags.TEXT

    def current_state_formatter(self, raw_data: dict | str, resp_format: str):
        try:
            if resp_format == KeysAndFlags.JSON:
                return f'```\n{raw_data}\n```', 'MarkdownV2'

            # to_dict = json.loads(raw_data)
            print(raw_data)
            print(type(raw_data))

            # ms = [
            #     as_marked_section(
            #         Bold(f'ip: {k}'),
            #         as_key_value('Номер СО', v.get('host_id')),
            #         as_key_value('Протокол', v.get('protocol')),
            #         marker=" ",
            #     ) for k, v in to_dict.items()
            # ]

            content = as_list(*raw_data, sep="\n\n")

            print(content)

            return content, False

        except Exception as err:
            print(err)

