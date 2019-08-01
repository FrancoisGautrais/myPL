#!/usr/bin/python3
from ..symbollexer import SymbolLexer


class StringIOWrapper:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.len = len(text)
        self.char = ""

    def read(self, n):
        if self.index >= self.len: return ""
        self.char = self.text[self.index]
        self.index += 1
        return self.char




class Lexer:
    TOK_UNKNOWN = -1
    TOK_END = 0
    TOK_PLUS=1
    TOK_MINUS=2
    TOK_STAR=3
    TOK_SLASH=4
    TOK_ANTI_SLASH=5
    TOK_HOOK_OPEN=6
    TOK_HOOK_CLOSE=7
    TOK_PAR_OPEN=8
    TOK_PAR_CLOSE=9
    TOK_ACC_OPEN=10
    TOK_ACC_CLOSE=11
    TOK_PIPE=12
    TOK_INTERROGATION=13
    TOK_DOT=14
    TOK_VIRGULE=15
    TOK_POINT_VIRGULE=16
    TOK_ALPHA=17
    TOK_DIGIT=18
    TOK_STRING=19

    TOKEN_LIST = ["END", "PLUS", "MINUS", "STAR", "SLASH", "ANTI_SLASH", "HOOK_OPEN", "HOOK_CLOSE",
                  "PAR_OPEN", "PAR_CLOSE", "ACC_OPEN", "ACC_CLOSE", "PIPE", "INTEROGATION", "DOT",
                  "VIRGULE", "POINT_VIRGULE", "ALPHA", "DIGIT", "STRING"]
    SEPARATOR = " \t\n\r"


    OPERATION = {
        '+' : TOK_PLUS,
        '-' : TOK_MINUS,
        '*' : TOK_STAR,
        '/' : TOK_SLASH,
        '\\' : TOK_ANTI_SLASH,
        '[' : TOK_HOOK_OPEN,
        ']' : TOK_HOOK_CLOSE,
        '(' : TOK_PAR_OPEN,
        ')' : TOK_PAR_CLOSE,
        '{' : TOK_ACC_OPEN,
        '}' : TOK_ACC_CLOSE,
        '|' : TOK_PIPE,
        '.' : TOK_DOT,
        '?' : TOK_INTERROGATION,
        ',' : TOK_VIRGULE,
        ';' : TOK_POINT_VIRGULE
    }

    def __init__(self, fd):
        self.fd = fd
        self.token = Lexer.OPERATION
        self.char = ""
        self.data = None
        self.current = ""
        self._nc()
        self.isFinished = False
        self.symbols = SymbolLexer(Lexer.OPERATION.keys())

    def _nc(self):
        self.char = self.fd.read(1)
        return self.char

    def _setToken(self, tok, string, data=None):
        self.token = tok
        if tok == Lexer.TOK_END:
            self.isFinished = True
        self.data = data if data != None else string
        self.current = string
        return self.token

    def _trim(self):
        while (self.char in Lexer.SEPARATOR) and self.char != "": self._nc()

    def _string(self):
        string = ""
        self._nc()
        while (self.char != "\"" or (len(string) > 0 and string[-1] == "\\")) and self.char != "":
            string += self.char
            self._nc()
        if self.char != "\"":
            raise Exception("Erreur _string: chaine non terminée")
        self._nc()
        return self._setToken(Lexer.TOK_STRING, string, string)


    def next(self):
        self.current = ""
        self._trim()
        if self.char == "":
            x = self._setToken(Lexer.TOK_END, None, None)
            self._nc()
            return x

        ret = self.symbols.readNext(self.char, self)
        if ret:
            return self._setToken(Lexer.OPERATION[ret], ret)

        if self.char == "\"":
            return self._string()

        if self.char.isdigit():
            x=self._setToken(Lexer.TOK_DIGIT, self.char)
            self._nc()
            return x

        if self.char.isalpha():
            x=self._setToken(Lexer.TOK_ALPHA, self.char)
            self._nc()
            return x





    @staticmethod
    def tokstr(tok):
        if tok == None:
            return "UNKNOWN"
        if tok >= 0 and tok < len(Lexer.TOKEN_LIST):
            return Lexer.TOKEN_LIST[tok]
        return "UNKNOWN"

    def read(self, n=1):
        return self._nc()


