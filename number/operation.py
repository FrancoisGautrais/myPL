#!/usr/bin/python3

from .builtin import hasBuiltin, execBuiltin, BUILTIN
import sys

class FunctionEntry:
	def __init__(self, val, argsName):
		self.fct=val # Operation not ident
		self.argsName=argsName
	
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		x="fct("
		for i in range(len(self.argsName)):
			if i>0: x+=", "
			x+=self.argsName[i]
		return x+")="+str(self.fct)

class Environement:
	
	def __init__(self, name="__main__"):
		self.var={}
		self.name=name
	
	def has(self, key):
		return key in self.var
		
	def get(self, key):
		if (not key in self.var):
				raise Exception("Var '",key,"' not defined")
		return self.var[key]
		
	def set(self, key, val):
		self.var[key]=val

	def __repr__(self): return self.__str__()

	def __str__(self):
		s=""+self.name+"\n"
		for key in  self.var:
			if len(key)<=2 or key[:2]!="__":
				s+="\t"+key+"='"+str(self.var[key])+"'\n"
		return s

class Test:
	def __init__(self):
		self.a=1
		self.b=1
		self.c=1

class Stack:
	def __init__(self):
		self.envs=[Environement()]
		self.set("test", Test())
		for x in BUILTIN:
			self.set(x, FunctionEntry(BUILTIN[x], []))
	
	def pushEnv(self, env=Environement()):
		self.envs.append(env)
	
	def popEnv(self):
		self.envs.pop()
	
	def has(self, key):
		for env in reversed(self.envs):
			if env.has(key): return True
		return False
	
	def get(self, key):
		key=str(key)
		for env in reversed(self.envs):
			if env.has(key): return env.get(key)

		raise Exception("Var '"+key+"' not defined")
	
	def set(self, key, val):
		for env in reversed(self.envs):
			if env.has(key):
				env.set(key, val)
				return
		self.envs[-1].set(key, val)

	def print(self):
		print(self)

	def __str__(self):
		i=0
		x=""
		for env in reversed(self.envs):
			x+= str(i)+":"+str(env)
			i+=1
		return x

def nts(n):
	x=""
	for i in range(n):
		x+="  "
	return x

class Operation:
	def getOperande(self, n):
		raise Exception("Not implemented")
		
	def countOperande(self):
		raise Exception("Not implemented")
	
	def countAll(self):
		if self.isLeaf(): return 1
		acc=1
		for i in range(self.countOperande()):
			acc+=self.getOperande(i).countAll()
		return acc
	
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		raise Exception(sys._getframe().f_code.co_name, " not implemented for "+type(self).__name__)
		
	def eval(self, env=Stack()):
		raise Exception(sys._getframe().f_code.co_name, " not implemented for "+type(self).__name__)

	def maxDepth(self, n=0):
		if self.isLeaf(): return n+1
		max=0
		for i in range(self.countOperande()):
			x=self.getOperande(i).maxDepth(n+1)
			max=x if x>max else max
		return max
		
	def isLeaf(self):
		raise Exception(sys._getframe().f_code.co_name, " not implemented for "+type(self).__name__)

	def clone(self, data=None):
		raise Exception(sys._getframe().f_code.co_name, " not implemented for "+type(self).__name__)
	
	def print(self, n=0):
		for i in range(self.countOperande()):
			op=self.getOperande(i)
			if op.isLeaf():
				print(op.first)
			else: op.print(n+1)
			
class BinaryOperation(Operation):
	def __init__(self, first=None, second=None):
		self.first=first
		self.second=second
		
	def isLeaf(self): return False
	
	def countOperande(self): return 2
	
	def getOperande(self, n):
		if n==0: return self.first
		if n==1: return self.second
		raise Exception("Out of band")
		
	def clone(self, data=None): return type(self)(self.first, self.second)
	
		

class UnaryOperation(Operation):
	def __init__(self, first=None):
		self.first=first
	
	def getOperande(self, n):
		if n==0: return self.first
		raise Exception("Out of band")
		
	def countOperande(self): return 1
	
	def clone(self, data=None): return type(self)(self.first)

class Nop(Operation):
	def isLeaf(self): return True

	def countOperande(self): return 0

	def getOperande(self, n): return None

	def eval(self, env=Stack()):
		return None


class For(Operation):
	def __init__(self):
		self.aff=Nop()
		self.cond=Number(True)
		self.inc=Nop()
		self.bloc=None

	def eval(self, env=Stack()):
		ret=None
		env.pushEnv(Environement())
		self.aff.eval(env)
		while self.cond.eval(env):
			ret= self.bloc.eval(env)
			self.inc.eval(env)

		env.popEnv()
		return ret


class While(Operation):
	def __init__(self, cond=None, bloc=None):
		self.cond=cond
		self.bloc=bloc

	def eval(self, env=Stack()):
		ret=None
		while self.cond.eval(env):
			ret= self.bloc.eval(env)
		return ret

class IfThenElse(Operation):
	def __init__(self, cond=None, bloc=None):
		self.condIf=cond
		self.blocThen=bloc
		self.eleseif=[] # [[cond1, bloc1], [cond2, bloc2] ]
		self.blocElse=None

	def setThen(self, op):
		self.blocThen=op

	def addElseif(self, cond, bloc):
		self.eleseif.append([cond, bloc])

	def setElse(self, op):
		self.blocElse=op

	def eval(self, env=Stack()):
		if(self.condIf.eval(env)): return self.blocThen.eval(env)
		for tup in self.eleseif:
			cond=tup[0]
			bloc=tup[1]
			if cond.eval(env): return bloc.eval(env)
		if self.blocElse==None: return None
		return self.blocElse.eval(env)


class Bloc(Operation):
	def __init__(self, inst=None):
		self.insts=[]
		self.enclose=True
		if inst!=None: self.insts.append(inst)

	def isLeaf(self): return len(self.insts)==0

	def countOperande(self): return len(self.insts)

	def getOperande(self, n): return self.insts[n]

	def addInst(self, inst):
		self.insts.append(inst)

	def eval(self, env=Stack()):
		ret=None
		if self.enclose: env.pushEnv()
		for inst in self.insts:
			ret=inst.eval(env)
		if self.enclose: env.popEnv()
		return ret;

	def __repr__(self): return self.__str__()

	def __str__(self):
		x="{"
		for i in range(len(self.insts)):
			if i>0: x+="; "
			x+=str(self.insts[i])
		return x+"}"



class Number(UnaryOperation):
	def eval(self, env=Stack()):
		return self.first
	
	def type(self):
		return type(self.data)
	
	def __str__(self):
		return str(self.first)
	
	def isLeaf(self): return True

class String(UnaryOperation):
	def eval(self, env=Stack()):
		return self.first

	def type(self):
		return type(self.data)

	def __str__(self):
		return str(self.first)

	def isLeaf(self): return True


class Negation(UnaryOperation):
	def eval(self, env=Stack()):
		return (not self.first.eval())
		
	def __str__(self):
		return "!"+str(self.first)
	
	def isLeaf(self): return True

class Identifier(UnaryOperation):
	def eval(self, env=Stack()):
		return self.first
		
	def __str__(self):
		return str(self.first)
		
	def isLeaf(self): return True
	
"""
class Variable(UnaryOperation):
	def eval(self, env=Stack()):
		var=env.get(self.first.eval(env))
		if var==None: raise Exception("Variable '"+self.first.eval(env)+"' inconnu")
		return var
		
	def __str__(self):
		return str(self.first)
		
	def isLeaf(self): return False"""

class Variable(Operation):
	def __init__(self, first=None):
		self.stack=[]
		if first: self.stack.append(first)

	def eval(self, env=Stack()):
		return self.getFinalObject(env)

	def countRef(self): return len(self.stack)-1

	def getBaseObject(self, env):
		if len(self.stack) < 2: return None
		name = self.stack[0].eval(env)
		ret=env.get(name)
		if ret==None: raise Exception("Variable '"+self.stack[0]+"' inconnu")
		for i in range(1, len(self.stack) - 1):
			ret = getattr(ret, self.stack[i])
		return ret

	def getFinalObject(self, env):
		if len(self.stack)==0: return None
		name=self.stack[0].eval(env)
		ret=env.get(name)
		if ret==None: raise Exception("Variable '"+self.stack[0]+"' inconnu")
		for i in range(1, len(self.stack)):
			ret=getattr(ret, self.stack[i].first)
		return ret

	def getFirstName(self):
		return self.stack[0]

	def getFinalName(self):
		return self.stack[-1]

	def addReferenced(self, name):
		self.stack.append(name)

	def __str__(self):
		s=""
		for i in range(len(self.stack)):
			if i>0: s+="."
			s+=self.stack[i].first
		return s
		
	def isLeaf(self): return False

class Addition(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env)+self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+"+"+str(self.second)+")"

class Soustraction(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env)-self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+"-"+str(self.second)+")"


class Multiplication(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env)*self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+"*"+str(self.second)+")"


class Modulo(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env)%self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+"%"+str(self.second)+")"


class Division(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env)/self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+"/"+str(self.second)+")"


class AndOperation(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env) and self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+" and "+str(self.second)+")"


class OrOperation(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env) or self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+" or "+str(self.second)+")"


class BitAndOperation(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env) & self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+" & "+str(self.second)+")"


class BitOrOperation(BinaryOperation):
	def eval(self, env=Stack()):
		return self.first.eval(env) | self.second.eval(env)

	def __str__(self):
		return "("+str(self.first)+" | "+str(self.second)+")"


class Affectation(BinaryOperation):
	def eval(self, env=Stack()):
		x=self.second.eval(env)

		if self.first.countRef()>0:
			setattr(self.first.getBaseObject(env), self.first.getFinalName().first, x)
		else:
			env.set(str(self.first.getFirstName()), x)
		return x

	def __str__(self):
		return "("+str(self.first)+"="+str(self.second)+")"


class Appel(Operation):
	def __init__(self, name, args):
		self.name=name
		self.args=args
		
	def eval(self, stack):
		name=self.name.getFinalName()

		fct=stack.get(name)
		env=Environement()
		if self.name.countRef>0:
			env.set(self, )

		args=[]

		if type(fct)==FunctionEntry and callable(fct.fct):
			for i in range(len(self.args)): args.append(self.args[i].eval(stack))
			return fct.fct(*tuple(args))
		elif type(fct)==FunctionEntry:
			if len(self.args)<len(fct.argsName):
				raise Exception("Error: "+str(self.name)+" takes "+str(len(fct.argsName))+" args, "+str(len(self.args))+" given")
			for i in range(len(fct.argsName)):
				env.set(fct.argsName[i], self.args[i].eval(stack))
			stack.pushEnv(env)
			#stack.print()
			out=fct.fct.eval(stack)
			stack.popEnv()
			return out
		else:
			for i in range(len(self.args)): args.append(self.args[i].eval(stack))
			return fct(*tuple(args))

	
	def __str__(self):
		return str(self.name)
	
	def isLeaf(self): return True


class Definition(BinaryOperation):
	def __init__(self, key, val, args):
		BinaryOperation.__init__(self, key, val)
		self.args=args
		
	def eval(self, env=Stack()):
		fct=FunctionEntry(self.second, self.args)
		if self.first: env.set(str(self.first), fct)
		return fct

	def __str__(self):
		s="def "
		if self.first: s+=str(self.first)
		s+="("
		for i in range(len(self.args)):
			if i>0: s+=","
			s+=self.args[i]
		s+=") = "+str(self.second)
		return s


class Comparaison(BinaryOperation):
	def __init__(self, op, a, b):
		BinaryOperation.__init__(self, a,b)
		self.op=op
		
	def eval(self, env=Stack()):
		a=self.first.eval(env)
		b=self.second.eval(env)
		if self.op == ">": return a>b
		if self.op == ">=": return a>=b
		if self.op == "<": return a<b
		if self.op == "<=": return a<=b
		if self.op == "!=": return a!=b
		if self.op == "==": return a==b

	def __str__(self):
		return "("+str(self.first)+self.op+str(self.second)+")"
		
	def clone(self, data=None): return type(self)(self.op, self.first, self.second)


