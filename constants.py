
from enum import Enum


class KeysAndFlags(Enum):
    JSON = {
        '-j', '-json', 'j', '-j'
    }
    TEXT = 'text'

    FLAG_GET_STATE = '?'
    FLAG_GET_STATES = '??'
    FLAG_GET_CONFIG = 'конфиг'


class AvailabelsControllers(Enum):
    PEEK = 'Peek'
    SWARCO = 'Swarco'
    POTOK_S = 'Поток (S)'
    POTOK_P = 'Поток (P)'


class JsonResponceBody(Enum):
    """
    Класс с перечислениями полей json responce
    """

    REQ_ERRORS = 'request_errors'
    HOST_ID = 'host_id'
    SCN = 'scn'
    IP_ADDRESS = 'ip_adress'
    PROTOCOL = 'protocol'
    VALID_DATA_REQUEST = 'valid_data_request'
    TYPE_CONTROLLER = 'type_controller'
    ADDRESS = 'address'
    INPUTS = 'inputs'
    USER_PARAMETERS = 'user_parameters'
    NUMBER = 'number'
    TYPE = 'type'
    REQUEST_EXEC_TIME = 'request_execution_time'
    REQ_ENTITY = 'request_entity'
    RESP_ENTITY = 'responce_entity'
    RAW_DATA = 'raw_data'
    DOWNLOAD_DATA = 'download_data'
    PATH_TO_ARHIVE = 'path_to_archive'
    PATH_TO_URL = 'url_to_archive'
    SSH = 'ssh'
    FTP = 'ftp'
    START_TIME = 'start_time'
    MODEL_OBJ = 'obj'
    HAS_IN_DB = 'has_in_db'
    TIME_REQ_CONTROLLER = 'request_time'


class ButtonsMainMenu(Enum):

    FEATURES = 'возможности'
    MONITORING = 'мониторинг'
    MANAGEMENT = 'управление'
    DOWNLOAD_COFIG = 'загрузка конфига'
