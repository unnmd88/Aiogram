from functools import cached_property

import aiohttp


class DriversStorage:
    """
    Синглтон для хранения драйверов различных сетевых запросов,
    таких как aiohttp.ClientSession, SnmpEngine и т.д.
    """

    _instance = None
    _attempts_create_instance = 0

    def __new__(cls, *args, **kwargs):
        cls._attempts_create_instance += 1
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_count_attempts_create_instance(cls):
        return cls._attempts_create_instance

    def __init__(self):
        self._aiohttp_client_session = None
        self._snmp_engine = None
        self._storage = {}

    def load_aiohttp_session(self, session: aiohttp.ClientSession):
        self._aiohttp_client_session = session
        self._storage['aiohttp_session'] = session

    def load_snmp_engine(self, engine):
        self._aiohttp_client_session = engine
        self._storage['snmp_engine'] = engine

    @property
    def aiohttp_client_session(self) -> aiohttp.ClientSession:
        return self._aiohttp_client_session

    @property
    def snmp_engine(self):
        return self._aiohttp_client_session

    @property
    def drivers_as_dict(self):
        return self._storage


drivers_storage = DriversStorage()


if __name__ == '__main__':
    i = [DriversStorage() for _ in range(10)]
    print(i)
    print(len(i))