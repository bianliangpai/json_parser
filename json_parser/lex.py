import re
from json_parser.definition import keyword_token_map, Symbol


class Lexer:
    def __init__(self, src=''):
        self._src = src
        self._tokens = []
        self._token_index = -1
        self._parse()

    def __str__(self):
        result = '{ '
        for token in self._tokens:
            result += "{} -> {}, ".format(token.token, token.src)
        result += ' }'
        return result

    def _parse(self):
        i = 0
        while i < len(self._src):
            ch = self._src[i]
            if ch == ' ' or ch == '\n' or ch == '\t':
                pass
            elif ch in keyword_token_map.keys():
                self._tokens.append(Symbol(keyword_token_map[ch], ch))
            elif re.search(re.compile('[a-zA-Z]'), ch):
                tmp = ''
                while i < len(self._src) and re.search(re.compile('[a-zA-Z0-9]'), self._src[i]):
                    tmp += self._src[i]
                    i += 1
                self._tokens.append(Symbol("Word", tmp))
                continue
            else:
                raise Exception("Unrecongnized input: {}".format(self._src[i]))
            i += 1

    def check_next_n(self, n):
        tmp = self._token_index + n
        if tmp >= len(self._tokens):
            return None
        return self._tokens[tmp]

    def next(self):
        self._token_index += 1
        if self._token_index >= len(self._tokens):
            return None
        return self._tokens[self._token_index]