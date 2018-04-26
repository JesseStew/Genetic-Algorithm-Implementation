""" 
Program: HW_Sample.py
Programmed By: Jared Hall
Description: A sample homework file containing some programming styles.
Trace Folder: Jared007
"""

#---------------------------------Imports--------------------------------------
#imports go here
import numpy as np
import math
#------------------------------------------------------------------------------

#---------------------------------Variables------------------------------------
#global variables go here
global globalVar
moduleVar = "SomeValue"
#------------------------------------------------------------------------------

#---------------------------------Classes/Functions----------------------------
class SomeClass():
	"""A descriptive statement about the class"""
	
	def __init__(self, arg1):
		#some descriptive comment about the method
		self.arg = arg1
		
	def __str__(self):
		return str(self.arg)
		
	def setArg(self, newArg):
		self.arg = newArg
	
	def getArg(self):
		return self.arg
		
def someAlgorithmFunction(obj1, obj2):
	#some descriptive comment
	A = obj1.getArg() + obj2.getArg()
	B = obj1.getArg() - obj2.getArg()
	
	#some comment about the formula
	result = (A+B)/((A-B)*(A+B))
	return result
#------------------------------------------------------------------------------

#---------------------------------Program Main---------------------------------
def main():
	if(__name__ == "__main__"):
	
		#some subsection
		object1 = SomeClass(2)
		object2 = SomeClass(10)
		
		#some processing comment
		algorithmResult = someAlgorithmFunction(object1, object2)
		object1.setArg(algorithmResult) #some descriptive comment
		object2.setArg(someAlgorithmFunction(object1, object2))
		print("Object 1 content: ", object1)
		print("Object 2 content: ", object2)
main()		
#---------------------------------End of Program-------------------------------
