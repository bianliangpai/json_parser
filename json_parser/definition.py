keyword_token_map = {'{' : 'Ocurly',
                     '}' : 'Ecurly',
                     '[' : 'Osquare',
                     ']' : 'Esquare',
                     '\"': 'Quote',
                     ':' : 'Colon',
                     ',' : 'Comma',}


class Symbol:
    def __init__(self, token, src):
        self.token = token
        self.src = src