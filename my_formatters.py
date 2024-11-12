import json
import logging
from typing import Type

from constants import KeysAndFlags, AvailabelsControllers

from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag, Italic, Underline
)

logger = logging.getLogger(__name__)


class Peek:

    def parse_get_state(self, ipAddr, data_host):
        # stream_info = data_host.get('responce_entity').get('raw_data').get('current_states').get('basic').get('stream_info')
        basic = data_host.get('responce_entity').get('raw_data').get('current_states').get('basic')
        stream_info = basic.get('stream_info')
        if stream_info is None:
            raise ValueError

        logger.debug(data_host)
        logger.debug(stream_info)
        streams = []
        # Формируются данные о Потоках
        for xp, data in stream_info.items():
            logger.debug(xp)
            logger.debug(data)
            xp_ = as_list(
                as_marked_section(
                    Bold(f'Поток {xp}:'),
                    as_key_value(' current_mode', data.get('current_mode')),
                    as_key_value(' current_stage', data.get('current_stage')),
                    as_key_value(' current_state', data.get('current_state')),
                    marker=''
                ),
            )
            streams.append(xp_)

        streams = as_list(
            *streams,
            sep=f'\n{50 * "-"}\n'
        )
        # Формируются полные данные об объетке
        basic_ = as_list(
            as_list(
                as_marked_section(
                    Bold(f'Номер СО: {data_host.get("host_id")}\nip: {ipAddr}'),
                    as_key_value('План', basic.get('current_plan')),
                    as_key_value('Параметр плана', basic.get('current_parameter_plan')),
                    as_key_value('Ошибки', basic.get('current_errors')),
                    as_key_value('Количество потоков', basic.get('streams')),
                    as_key_value('Время ДК', basic.get('current_time')),
                    marker=" ",
                ),
                as_marked_section(
                    Italic(Underline(Bold('\n--stream info--'))),
                    as_list(streams),
                    marker=''
                ),
                as_marked_section(
                    as_key_value('\nТип ДК', data_host.get('type_controller')),
                    as_key_value('Адрес ДК', data_host.get('address')),
                    as_key_value('Протокол получения данных', data_host.get('protocol')),
                    as_key_value('Время запроса', data_host.get('request_time')),
                ),
            ),
            sep='\n\n',
        )
        return basic_


class Swarco:
    pass


class UndefindTypeController:
    pass

class CommonTypeController:
    pass


class BaseFormatter:

    def __init__(self, responce_format: KeysAndFlags = None):
        self.responce_format = responce_format

    def _create_obj(self, type_controller: str) -> Peek | Swarco | UndefindTypeController:

        matches = {
            AvailabelsControllers.PEEK.value: Peek,
            AvailabelsControllers.SWARCO.value: Swarco
        }
        logger.debug(matches)
        if type_controller not in matches:
            return UndefindTypeController()

        return matches.get(type_controller)()

    def define_format_responce(self, data: list[str]) -> KeysAndFlags:

        if data[-1] in KeysAndFlags.JSON.value:
            return KeysAndFlags.JSON
        else:
            return KeysAndFlags.TEXT

    def text_format_current_state(self, raw_data: str):

        content = []
        for ipAddr, data_host in json.loads(raw_data).items():
            logger.debug(data_host)
            obj = self._create_obj(data_host.get('type_controller'))
            logger.debug(f'obj: {obj}')

            if data_host.get('request_errors') or isinstance(obj, UndefindTypeController):
                content.append(self.text_format_current_state_base_data_only(ipAddr, data_host))
            else:
                content.append(obj.parse_get_state(ipAddr, data_host))

        return as_list(*content, HashTag(f"Режим"), sep="\n\n")

    def text_format_current_state_base_data_only(self, ipAddr, data_host):

        basic_ = as_list(
            as_marked_section(
                Bold(f'Номер СО: {data_host.get("host_id") or "Не определён"}\nip: {ipAddr}'),
                as_key_value('Ошибки', data_host.get('request_errors')),
                as_key_value('Тип ДК', data_host.get('type_controller')),
                as_key_value('Адрес ДК', data_host.get('address')),
                as_key_value('Протокол получения данных', data_host.get('protocol')),
                as_key_value('Время запроса', data_host.get('request_time')),
                marker=" ",
            ),
            sep='\n\n',
        )
        return basic_

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


def current_state_formatter( raw_data: dict | str, resp_format: str):

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