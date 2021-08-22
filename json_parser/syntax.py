# Json Grammar:
#
# <start>      ::= <dict>
#                | <array>
#                | <empty>
#
# <dict>       ::= <Ocurly> <kv_exprs> <Ecurly>
#
# <kv_exprs>   ::= <kv_expr> <Comma> <kv_exprs>
#                | <kv_expr>
#                | <empty>
#
# <kv_expr>    ::= <Quote> <word> <Quote> <Colon> <dict>
#                | <Quote> <word> <Quote> <Colon> <array>
#                | <Quote> <word> <Quote> <Colon> <word>
#                | <Quote> <word> <Quote> <Colon> <Quote> <word> <Quote>
#
# <array>      ::= <Osquare> <arr_exprs> <Esquare>
#
# <arr_exprs>  ::= <arr_expr> <Comma> <arr_exprs>
#                | <arr_expr>
#                | <empty>
#
# <arr_expr>   ::= <dict>
#                | <array>
#                | <word>
#                | <Quote> <word> <Quote>


class Syntaxer:
    def __init__(self, lexer):
        self._lexer = lexer
        self._object = None

    def __str__(self):
        return str(self._object)

    def run(self):
        symbol = self._lexer.check_next_n(1)
        if symbol.token == 'Ocurly':
            self._object = self._dict()
        elif symbol.token == 'Osquare':
            self._object = self._array()
        elif not symbol:
            return None
        else:
            raise Exception("Syntax Error!")
        return self._object

    def _dict(self):
        d = {}
        assert(self._lexer.next().token == 'Ocurly')
        kv_exprs = self._kv_exprs()
        for k, v in kv_exprs:
            d[k]=v
        assert(self._lexer.next().token == 'Ecurly')
        return d

    def _kv_exprs(self):
        kv_exprs = []
        symbol = self._lexer.check_next_n(1)
        if symbol.token == "Quote":
            k, v = self._kv_expr()
            kv_exprs.append((k, v))

            tmp = self._lexer.check_next_n(1)
            if tmp.token == "Comma":
                assert(self._lexer.next().token == "Comma")
                kv_exprs.extend(self._kv_exprs())
            elif tmp.token != "Ecurly":
                raise Exception("Syntax Error!")
        elif symbol.token == "Ecurly":
            self._empty()
        else:
            raise Exception("Syntax Error!")
        return kv_exprs

    def _kv_expr(self):
        k = None
        v = None

        assert(self._lexer.next().token == 'Quote')
        word = self._lexer.next()
        assert(word.token == "Word")
        k = word.src
        assert(self._lexer.next().token == 'Quote')
        assert(self._lexer.next().token == 'Colon')

        symbol = self._lexer.check_next_n(1)
        if symbol.token == "Ocurly":
            v = self._dict()
        elif symbol.token == "Osquare":
            v = self._array()
        elif symbol.token == "Word":
            tmp = self.lexer.next()
            assert(tmp.token == "Word")
            v = tmp.src
        elif symbol.token == "Quote":
            assert(self._lexer.next().token == 'Quote')
            tmp = self._lexer.next()
            assert(tmp.token == "Word")
            v = tmp.src
            assert(self._lexer.next().token == 'Quote')
        else:
            raise Exception("Syntax Error!")

        return k, v

    def _empty(self):
        return None

    def _array(self):
        assert(self._lexer.next().token == 'Osquare')
        a = self._arr_exprs()
        assert(self._lexer.next().token == 'Esquare')
        return a

    def _arr_exprs(self):
        arr_exprs=[]
        symbol = self._lexer.check_next_n(1)
        if symbol:
            arr_exprs.append(self._arr_expr())

            tmp = self._lexer.check_next_n(1)
            if tmp.token == "Comma":
                assert(self._lexer.next().token == "Comma")
                arr_exprs.extend(self._arr_exprs())
            elif tmp.token != "Esquare":
                raise Exception("Syntax Error!")
        else:
            self._empty()
        return arr_exprs

    def _arr_expr(self):
        v = None
        symbol = self._lexer.check_next_n(1)
        if symbol.token == "Ocurly":
            v = self._dict()
        elif symbol.token == "Qsquare":
            v = self._array()
        elif symbol.token == "Word":
            tmp = self._lexer.next()
            assert(tmp.token == "Word")
            v = tmp.src
        elif symbol.token == "Quote":
            assert(self._lexer.next().token == 'Quote')
            tmp = self._lexer.next()
            assert(tmp.token == "Word")
            v = tmp.src
            assert(self._lexer.next().token == 'Quote')
        return v
