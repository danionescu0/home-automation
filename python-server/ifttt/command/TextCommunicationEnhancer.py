import re

from typeguard import typechecked

from ifttt.parser.Tokenizer import Tokenizer


class TextCommunicationEnhancer:
    __clusters = [
            'A\[(\w+)\]',
            'S\[(\w+)\]',
            'TIME',
        ]
    @typechecked()
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.__tokenizer = tokenizer

    @typechecked()
    def enhance(self, text: str) -> str:
        for cluster in self.__clusters:
            p = re.compile(cluster)
            for found in p.finditer(text):
                text = self.__replace(text, found.group())

        return text

    def __replace(self, original, text_to_be_replaced):
        token = self.__tokenizer.tokenize(text_to_be_replaced)[0]

        return original.replace(text_to_be_replaced, str(token.get_value()))