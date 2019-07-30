#!/usr/bin/python3

def _print(x):
    print(x)

BUILTIN={
    "print": _print,
    "int": int,
    "float": float,
    "bool": bool,
    "string": str,
    "array": list,
    "list": list,
    "len": len,
    "object": dict
}

def hasBuiltin(name):
    return name in BUILTIN

def getBuiltIn(name):
    return BUILTIN[name]

def execBuiltin(name, args):
    return BUILTIN[name](*tuple(args))

