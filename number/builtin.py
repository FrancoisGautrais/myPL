#!/usr/bin/python3

import time

class Array(list):
    def __init__(self):
        list.__init__(self)

    def length(self): return self.__len__()

    def at(self, n): return self[n]

    def contains(self, n):
        return n in self

    def set(self, n, val):
        self[n] = val
        return  val

BUILTIN={
    "print": print,
    "int": int,
    "float": float,
    "bool": bool,
    "string": str,
    "array": Array,
    "list": Array,
    "len": len,
    "object": dict,
    "timestamp": time.time
}

