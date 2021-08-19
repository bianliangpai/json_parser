import re


token_map = {'{' : 'OCurly',
             '}' : 'ECurly',
             '[' : 'OSQUARE',
             ']' : 'ESQUARE',
             '\"': 'QUOTE',
             ':' : 'COLON',
             ',' : 'COLMA',
             '[a-zA-Z][a-zA-Z0-9]*': 'WORD'}


class Symbol:
    def __init__(self, token, src):
        self.token = token
        self.src = src

class Lexer:
    def __init__(self, src=''):
        self._src = src
        self._tokens = []
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
            elif ch in '{}[]\":,':
                self._tokens.append(Symbol(token_map[ch], ch))
            elif re.search(re.compile('[a-zA-Z]'), ch):
                tmp = ch
                while i < len(self._src) and re.search(re.compile('[a-zA-Z0-9]'), self._src[i]):
                    tmp += self._src[i]
                    i += 1
                self._tokens.append(Symbol("WORD", tmp))
                continue
            else:
                raise Exception("Unrecongnized input: {}".format(self._src[i]))
            i += 1

    def next():
        pass