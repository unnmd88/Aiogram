
from enum import Enum


class KeysAndFlags(Enum):
    JSON = {
        '-j', '-json', 'j', '-j'
    }
    TEXT = 'text'

    FLAG_GET_STATE = '?'
    FLAG_GET_CONFIG = 'конфиг'


class AvailabelsControllers(Enum):
    PEEK = 'Peek'
    SWARCO = 'Swarco'
    POTOK_S = 'Поток (S)'
    POTOK_P = 'Поток (P)'


class JsonResponceBody(Enum):

    REQ_ERRORS = 'request_errors'
    HOST_ID = 'host_id'
    PROTOCOL = 'protocol'
    VALID_DATA_REQUEST = 'valid_data_request'
    TYPE_CONTROLLER = 'type_controller'
    ADDRESS = 'address'
    REQUEST_EXEC_TIME = 'request_execution_time'
    REQ_ENTITY = 'request_entity'
    RESP_ENTITY = 'responce_entity'
    RAW_DATA = 'raw_data'
    SSH = 'ssh'
    FTP = 'ftp'
    START_TIME = 'start_time'
