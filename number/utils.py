#!/usr/bin/python3
import inspect

class Utils:
    class FunctionInfo:
        def __init__(self, fct):
            self.ref=fct
            self.name=fct.__name__
            params=inspect.signature(fct).parameters

            self.nParamMin=0
            self.nParamMax=0
            self.nParam=len(params)
            for i in params:
                p=params[i]
                if p.default==inspect._empty:
                    self.nParamMin+=1
                else: self.nParamMax+=1

        def __str__(self):
            return self.name+"("+str(self.nParam)+")["+str(self.nParamMin)+"-"+str(self.nParamMax)+"]"