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
# #class -> (prim* | '[' range+ ']') [selector]
# #selector -> '?' | '{' NUMBER [ ',' NUMBER]'}' | '*' | '+'
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
        root=Graph()
        if self.tok==Lexer.TOK_POINT_VIRGULE: return None
        self._expr(root)
        while self.tok!=Lexer.TOK_POINT_VIRGULE:
            self._expr(root)
        return root

    def _expr(self, root):
        return self._class(root)

    def _class(self, upRoot):
        out=None
        root=Graph()
        if self.tok in Regex.PRIM_PREMIER:
            while self.tok in Regex.PRIM_PREMIER:
                self._prim(root)

        elif self.tok==Lexer.TOK_HOOK_OPEN:
            self._next()
            while self.tok!=Lexer.TOK_HOOK_CLOSE:
                self._range(root)
            self._next()

        else:
            raise Exception("Expected Class or char")
        upRoot.append(root)

    def _range(self, root, node):
        first=self._char(root)
        next=Node()
        if self.tok == Lexer.TOK_MINUS:
            if not first.isAlfaNum():
                raise Exception("Alphanumeric char expected before '-")
            self._next()
            second=self._char(root)
            if not  not first.isAlfaNum():
                raise Exception("Alphanumeric char expected after '-")
            for x in range(ord(first), ord(second)+1):
                node.connect(chr(x), next)
            return
        return

    def _prim(self, root):
        if self.tok==Lexer.TOK_ANTI_SLASH:
            self._next()
            root.append(self.data)
            self._next()
            return

        if self.tok==Lexer.TOK_STRING:
            for x in self.data:
                root.append(x)
            self._next()
            return

        if self.tok==Lexer.TOK_PAR_OPEN:
            self._next()
            self._expr(root)
            if self.tok!=Lexer.TOK_PAR_CLOSE: raise Exception("']' not found in class")
            self._next()
            return

        self._char(root)
        return

    CHAR_PREMIER=[Lexer.TOK_DOT, Lexer.TOK_DIGIT, Lexer.TOK_ALPHA]
    PRIM_PREMIER=[Lexer.TOK_DOT, Lexer.TOK_DIGIT, Lexer.TOK_ALPHA, Lexer.TOK_PAR_OPEN]
    SLECETOR_PREMIER=[Lexer.TOK_INTERROGATION, Lexer.TOK_ACC_OPEN, Lexer.TOK_STAR, Lexer.TOK_PLUS]

    def _char(self, root):
        x=None
        if self.tok==Lexer.TOK_DOT:
            x=None
        elif self.tok in [Lexer.TOK_DIGIT, Lexer.TOK_ALPHA]:
            x=self.data
        root.append(x)
        self._next()
        return x

    @staticmethod
    def compile(string):
        if  not (';' in string):
            string=string+';'
        parser=Regex(StringIOWrapper(string))
        return  parser.parse()