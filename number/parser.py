#!/usr/bin/python3

from .lexer import Lexer

from .operation import *
from .builtin import *

#
# bloc -> '{' instlist '}' | inst
# instlist -> inst [ ';' inst ]*
# inst -> 'return' expr | 'include' expr | expr ';'
# expr -> def | for | while | if | expraff
# def -> 'def' [IDENT] '(' [IDENT [, IDENT]*] ')' ['='] expr | expr
# for -> 'for' '(' [expr] ; [expr]; [expr] ')' bloc
# while -> 'wille' '(' expr ')' bloc
# if -> 'if' '(' expr ')' bloc [ 'elif' '(' expr ')' bloc ]* ['else' bloc]
# expraff -> IDENT (['+'|'-'|'*'|'/'|'%'|'&'|'|'|'&&'|'||']'=') expr | IDENT ('++' | '--') | exprand
# expror -> exprand '||' expror | exprand
# exprand -> exprbor '&&' exprand | exprbor
# exprbor -> exprband '|' expbror | exprband
# exprband -> exprnot '&' expbrand | exprnot
# exprnot -> '!' exprnot | exprcmp
# exprcmp -> expradd ('<'|'<='|'>'|'>='|'=='|'!=') exprcmp | expradd
# expradd -> exprmul '-' expradd |  exprmul '+' expradd | exprmul
# exprmul -> prim '*' exprmul |  prim '/' exprmul | prim
# prim -> object [call]  int | float | bool | '(' expr ')'
# call ->  '(' [expr [ ',' expr ]*] ')'
# object -> ident [  '.' ident  |  '[' expr ']' ]*
# array -> '[' [expr [ ',' expr]* ] ']'
# ident -> IDENT

class Parser:
    def __init__(self, fd):
        self.lex = Lexer(fd)
        self.tok = Lexer.TOK_UNKNOWN
        self.data = None
        self.context = None

    def _next(self):
        self.tok = self.lex.next()
        self.data = self.lex.data
        #print("Token", Lexer.tokstr(self.tok), " '" + str(self.data) + "'")
        return self.tok

    def parse(self, context):
        self.context=context
        self._next()
        return self._main()


    def parseInterractif(self):
        self._next()
        return self._main()

    def _main(self):
        ret=None
        ret=self._instList()
        ret.enclose=False
        return ret

    def _block(self):
        if self.tok != Lexer.TOK_AO:
            return Bloc(self._inst())
        self._next()
        bloc = self._instList()

        if self.tok != Lexer.TOK_AF and self.tok != Lexer.TOK_END:
            raise Exception("'}' manquant en fin de bloc : "+Lexer.tokstr(self.tok))
        self._next()
        return bloc

    def _instList(self):
        if self.tok==Lexer.TOK_AF: return Bloc(Nop())
        bloc = Bloc(self._inst())
        while self.tok != Lexer.TOK_END and self.tok!=Lexer.TOK_AF:
            if self.tok==Lexer.TOK_AF:
                self._next()
                return bloc
            op=self._inst()
            if type(op)!=Nop:
                bloc.addInst(op)
            if self.tok==Lexer.TOK_PVIRGULE: self._next()

        return bloc

    def _inst(self):
        if self.tok==Lexer.TOK_KEYWORD:
            if self.data == "return": return self._return()
            if self.data == "include": return self._include()
        return self._expr()

    def _include(self):
        self._next()
        return self.context.parseSourceFile(self._expr().eval(self.context.stack))

    def _return(self):
        if self.tok!=Lexer.TOK_KEYWORD or self.data!="return":
            raise Exception("Return must begin by 'return")
        self._next()
        return Return(self._expr())

    def _expr(self):
        if self.tok==Lexer.TOK_KEYWORD:
            if self.data=="def": return self._def()
            if self.data=="while": return self._while()
            if self.data=="for": return self._for()
            if self.data=="if": return self._if()
        return self._exprAff()

    def _def(self):
        if self.tok != Lexer.KEYWORDS and self.data != "def":
            raise Exception("Definition msut begin by 'def'")
        self._next()
        first=None
        if self.tok != Lexer.TOK_PO: first = self._ident()

        if self.tok == Lexer.TOK_PO:
            args = []
            self._next()

            if self.tok == Lexer.TOK_PF:
                self._next()
                return Definition(first, self._block(), args)

            if self.tok != Lexer.TOK_IDENT: raise Exception("A Expected ident for var args : " + Lexer.tokstr(self.tok))
            args.append(self.data)
            self._next()

            while self.tok != Lexer.TOK_PF:
                if self.tok != Lexer.TOK_VIRGULE:
                    raise Exception("Expected ',' in fct def : " + Lexer.tokstr(self.tok))
                self._next()

                if self.tok != Lexer.TOK_IDENT: raise Exception(
                    "B Expected ident for var args : " + Lexer.tokstr(self.tok))
                args.append(self.data)
                self._next()
            self._next()
            if self.tok == Lexer.TOK_AFF:
                self._next()
            return Definition(first, self._block(), args)

    def _for(self):
        if self.tok!=Lexer.TOK_KEYWORD or self.data!="for":
            raise Exception("For msut begin by 'for'")
        self._next()
        ret=For()

        if self.tok != Lexer.TOK_PO: raise Exception("Erreur '(' manquant apres for")
        self._next()

        if self.tok != Lexer.TOK_PVIRGULE:
            ret.aff=self._exprAff()
            if self.tok != Lexer.TOK_PVIRGULE: raise Exception("Need ';' afet for affectation")
        self._next()

        if self.tok != Lexer.TOK_PVIRGULE:
            ret.cond=self._expr()
            if self.tok != Lexer.TOK_PVIRGULE: raise Exception("Need ';' afet for condition")
        self._next()

        if self.tok != Lexer.TOK_PF:
            ret.inc=self._expr()
            if self.tok != Lexer.TOK_PF: raise Exception("Need ')' afet for incrementation")
        self._next()
        ret.bloc=self._block()
        ret.bloc.enclose=False
        return ret

    def _while(self):
        if self.tok!=Lexer.TOK_KEYWORD or self.data!="while":
            raise Exception("While msut begin by 'while'")
        self._next()

        if self.tok != Lexer.TOK_PO: raise Exception("Erreur '(' manquant apres while")
        self._next()
        cond = self._expr()
        if self.tok != Lexer.TOK_PF: raise Exception("Erreur ')' manquant apres la condition while")
        self._next()
        bloc=self._block()
        return While(cond, bloc)

    def _if(self):
        if self.tok!=Lexer.TOK_KEYWORD or self.data!="if":
            raise Exception("For msut begin by 'if'")
        self._next()

        if self.tok!=Lexer.TOK_PO: raise Exception("Erreur '(' manquant apres if")
        self._next()
        cond=self._expr()
        if self.tok!=Lexer.TOK_PF: raise Exception("Erreur ')' manquant apres la condition if")
        self._next()

        blocThen=self._block()

        retIf=IfThenElse(cond, blocThen)

        while self.tok==Lexer.TOK_KEYWORD and self.data=="elif":
            self._next()
            if self.tok != Lexer.TOK_PO: raise Exception("Erreur '(' manquant apres elif")
            self._next()
            cond = self._expr()
            if self.tok != Lexer.TOK_PF: raise Exception("Erreur ')' manquant apres la condition elif")
            self._next()

            blocThen = self._block()
            retIf.addElseif(cond, blocThen)

        if self.tok == Lexer.TOK_KEYWORD and self.data == "else":
            self._next()
            bloc = self._block()
            retIf.setElse(bloc)
        return  retIf


    def _exprAff(self):
        first = self._exprOr()
        op = self.tok

        if Lexer.isAff(op) and type(first) == Variable:
            self._next()
            second = self._expr()
            if op == Lexer.TOK_AFF:   return Affectation(first, second)
            if op == Lexer.TOK_MINUSEQUALS:   return Affectation(first, Soustraction(first, second))
            if op == Lexer.TOK_PLUSEQUALS:   return Affectation(first, Addition(first, second))
            if op == Lexer.TOK_MULTEQUALS:   return Affectation(first, Multiplication(first, second))
            if op == Lexer.TOK_DIVEQUALS:   return Affectation(first, Division(first, second))
            if op == Lexer.TOK_OREQUALS:   return Affectation(first, OrOperation(first, second))
            if op == Lexer.TOK_ANDEQUALS:   return Affectation(first, AndOperation(first, second))
            if op == Lexer.TOK_MODULOEQUALS:   return Affectation(first, Modulo(first, second))

        if op==Lexer.TOK_PLUSPLUS :
            self._next()
            return Affectation(first, Addition(first, Number(1)))

        if op==Lexer.TOK_MINUSUSMINUS:
            self._next()
            return Affectation(first, Soustraction(first, Number(1)))

        return first

    def _exprOr(self):
        first = self._exprAnd()
        op = self.tok
        opstr = self.data
        if op != Lexer.TOK_OR: return first

        self._next()
        second = self._exprOr()
        return OrOperation(first, second)

    def _exprAnd(self):
        first = self._exprBOr()
        op = self.tok
        opstr = self.data
        if op != Lexer.TOK_AND: return first

        self._next()
        second = self._exprAnd()
        return AndOperation(first, second)

    def _exprBOr(self):
        first = self._exprBAnd()
        op = self.tok
        opstr = self.data
        if op != Lexer.TOK_BOR: return first

        self._next()
        second = self._exprAnd()
        return BitOrOperation(first, second)


    def _exprBAnd(self):
        first = self._exprNot()
        op = self.tok
        opstr = self.data
        if op != Lexer.TOK_BAND: return first

        self._next()
        second = self._exprAnd()
        return BitAndOperation(first, second)


    def _exprNot(self):
        if self.tok == Lexer.TOK_NOT:
            self._next()
            x = self._exprNot()
            return Negation(x)
        else:
            return self._exprComp()


    def _exprComp(self):
        first = self._exprAdd()
        op = self.tok
        opstr = self.data
        if op != Lexer.TOK_CMP: return first

        self._next()
        second = self._exprComp()
        return Comparaison(opstr, first, second)

    def _exprAdd(self):
        first = self._exprMul()
        op = self.tok
        if not (op in [Lexer.TOK_ADD, Lexer.TOK_SUB]): return first

        self._next()
        second = self._exprAdd()
        if op == Lexer.TOK_ADD: return Addition(first, second)
        return Soustraction(first, second)

    def _exprMul(self):
        first = self._prim()
        op = self.tok

        if not (op in [Lexer.TOK_MUL, Lexer.TOK_DIV, Lexer.TOK_MODULO]):    return first

        self._next()
        second = self._exprMul()
        if op == Lexer.TOK_MODULO: return Modulo(first, second)
        if op == Lexer.TOK_MUL: return Multiplication(first, second)
        return Multiplication(first, second)

    PRIM_PREMIER = [Lexer.TOK_PO, Lexer.TOK_INT, Lexer.TOK_FLOAT, Lexer.TOK_IDENT, Lexer.TOK_BOOL, Lexer.TOK_STRING,
                    Lexer.TOK_CO]

    def _prim(self):
        if not (self.tok in Parser.PRIM_PREMIER): raise Exception("_exprMul: Attendu '(', int ou float : "+Lexer.tokstr(self.tok))

        # (
        if self.tok == Lexer.TOK_PO:
            self._next()
            x = self._expr()
            if self.tok != Lexer.TOK_PF:
                raise Exception("Parenthese fermante manquante=> " + Lexer.tokstr(self.tok))
            self._next()
            return x
        # Number
        if self.tok in [Lexer.TOK_INT, Lexer.TOK_FLOAT, Lexer.TOK_BOOL, Lexer.TOK_STRING]:
            ret = Number(self.data)
            self._next()
            return ret
        if self.tok == Lexer.TOK_CO:
            return self._array()
        # ident
        if self.tok in [Lexer.TOK_IDENT]:
            name = self._object()
            if self.tok == Lexer.TOK_PO:
                return self._call(name)
            return name
        raise Exception("Attendu: int, float ou '(' => " + Lexer.tokstr(self.tok))

    def _call(self, name):
        args = []
        self._next()
        if self.tok == Lexer.TOK_PF:
            self._next()
            return Appel(name, args)

        args.append(self._expr())

        while self.tok != Lexer.TOK_PF:
            if self.tok != Lexer.TOK_VIRGULE:
                raise Exception("Expected ',' in fct def : " + Lexer.tokstr(self.tok))
            self._next()
            args.append(self._expr())
        self._next()

        return Appel(name, args)

    def _object(self):
        if self.tok != Lexer.TOK_IDENT: raise Exception("IDENT expected")
        v=Variable(self._ident())

        while self.tok==Lexer.TOK_REF or self.tok==Lexer.TOK_CO:
            if self.tok==Lexer.TOK_REF:
                self._next()
                v.addReferenced(self._ident())
            else:
                self._next()
                ident=self._expr()
                if self.tok!=Lexer.TOK_CF: raise Exception("']' expected after ident reference")
                self._next()
                v.addHookReferenced(ident)

        return v

    def _array(self):
        if self.tok != Lexer.TOK_CO: raise Exception("'[' expected")
        self._next()
        x=Array()

        if self.tok == Lexer.TOK_CF:
            self._next()
            return ArrayWrapper(x)

        x.append(self._expr())

        while self.tok == Lexer.TOK_VIRGULE:
            self._next()
            x.append(self._expr())

        if self.tok != Lexer.TOK_CF: raise Exception("Array must end with ']'")
        self._next()
        return ArrayWrapper(x)

    def _ident(self):
        data = self.data
        self._next()
        return Identifier(data)
