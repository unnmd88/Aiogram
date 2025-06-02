from abc import abstractmethod
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Traffic lights helper')


class MessageParser:
    def __init__(self, message: str = ''):
        self._msg = message

    @abstractmethod
    def parse(self, *args, **kwargs):
        """ Реализация парса сообщения """

class TextParser:
    def __init__(self, text: str):
        self._src_text = text
        self._args = text.split()
        self._parser = argparse.ArgumentParser(description='Traffic lights helper')
