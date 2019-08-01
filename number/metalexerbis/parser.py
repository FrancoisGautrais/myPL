#!/usr/bin/python3

from .lexer import Lexer
from .lexer import StringIOWrapper

from .operation import *


#
#
#
#
#
#
#
#
# expr -> class
# class -> (prim* | '[' range+ ']') [selector]
# selector -> '?' | '{' NUMBER [ ',' NUMBER]'}' | '*' | '+'
# range -> char [ '-' char ]
# prim ->  ['\'] CHAR |  STRING |  '(' class ')'
# char -> '.' | ALPHA | NUMERIC


class Regex:
    def __init__(self, fd):
        self.lex = Lexer(fd)
        self.tok = Lexer.TOK_UNKNOWN
        self.data = None

    def _next(self):
        self.tok = self.lex.next()
        self.data = self.lex.data
        #print("Token", Lexer.tokstr(self.tok), " '" + str(self.data) + "'")
        return self.tok

    def parse(self):
        self._next()
        return self._main()

    def _main(self):
        if self.tok==Lexer.TOK_POINT_VIRGULE: return None
        first=self._expr()
        curr=first
        while self.tok!=Lexer.TOK_POINT_VIRGULE:
            tmp=self._expr()
            curr.addNextToEnd(tmp)
            curr=tmp
        return first

    def _expr(self):
        return self._class()

    def _class(self):
        out=None
        if self.tok in Regex.PRIM_PREMIER:
            curr=self._prim()
            first=curr
            while self.tok in Regex.PRIM_PREMIER:
                tmp  = self._prim()
                curr.addNextToEnd(tmp)
                curr=tmp
            out=first

        elif self.tok==Lexer.TOK_HOOK_OPEN:
            self._next()
            ranges=Class()
            ranges.addRange(self._range().setParent(ranges))
            while self.tok!=Lexer.TOK_HOOK_CLOSE:
                ranges.addRange(self._range().setParent(ranges))
            self._next()
            out=ranges
        else:
            raise Exception("Expected Class or char")
        sel=self._selector()
        if sel==None: return out
        return sel.setStart(out)

    def _selector(self):
        if self.tok == Lexer.TOK_INTERROGATION:
            self._next()
            return FacultativeSelector()
        if self.tok == Lexer.TOK_STAR:
            self._next()
            return StarSelector()
        if self.tok == Lexer.TOK_PLUS:
            self._next()
            return PlusSelector()
        if self.tok == Lexer.TOK_ACC_OPEN:
            out=None
            self._next()
            n=self._number()
            if self.tok == Lexer.TOK_VIRGULE:
                self._next()
                m=self._number()
                out=NumberRangeSelector(n,m)
            else:
                out=NumberSelector(n)

            if self.tok != Lexer.TOK_ACC_CLOSE:
                raise Exception("expected '}' to end number selector")
            self._next()
            return out
        return None

    def _number(self):
        acc=""
        while self.tok==Lexer.TOK_DIGIT:
            acc+=self.data
            self._next()
        return int(acc)

    def _range(self):
        first=self._char()
        if self.tok == Lexer.TOK_MINUS:
            if not type(first)==Char or not first.isAlfaNum():
                raise Exception("Alphanumeric char expected before '-")
            self._next()
            second=self._char()
            if not type(second)==Char or not first.isAlfaNum():
                raise Exception("Alphanumeric char expected after '-")
            return Range(first, second)
        return first


    def _prim(self):
        if self.tok==Lexer.TOK_ANTI_SLASH:
            self._next()
            d=Char(self.data)
            self._next()
            return d

        if self.tok==Lexer.TOK_STRING:
            x=String(self.data)
            self._next()
            return x

        if self.tok==Lexer.TOK_PAR_OPEN:
            self._next()
            x=self._expr()
            if self.tok!=Lexer.TOK_PAR_CLOSE: raise Exception("']' not found in class")
            self._next()
            return Parentheses(x)

        d=self._char()
        return d

    CHAR_PREMIER=[Lexer.TOK_DOT, Lexer.TOK_DIGIT, Lexer.TOK_ALPHA]
    PRIM_PREMIER=[Lexer.TOK_DOT, Lexer.TOK_DIGIT, Lexer.TOK_ALPHA, Lexer.TOK_PAR_OPEN]
    SLECETOR_PREMIER=[Lexer.TOK_INTERROGATION, Lexer.TOK_ACC_OPEN, Lexer.TOK_STAR, Lexer.TOK_PLUS]

    def _char(self):
        d=None
        if self.tok==Lexer.TOK_DOT:
            d=Dot()
        elif self.tok in [Lexer.TOK_DIGIT, Lexer.TOK_ALPHA]:
            d=Char(self.data)
        self._next()
        return d

    @staticmethod
    def compile(string):
        if  not (';' in string):
            string=string+';'
        parser=Regex(StringIOWrapper(string))
        return  parser.parse()