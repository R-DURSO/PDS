from ctypes import * 
import os

'''
fonction permettant de récupérer 
'''
def getPath():
    path = os.getcwd()
    fileName  = "test.so"
    absFilePath = os.path.abspath(__file__)
    path, filename = os.path.split(absFilePath)
    path,file = os.path.split(path)
    path = path.__add__("\\arm\\"+fileName)
    return path 

path = getPath()
# print(path)
lib = CDLL(path) 
lib.hello()

# print(lib)