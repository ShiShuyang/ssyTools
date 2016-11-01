# -*- coding: utf8 -*-
import urllib2, os
__version__ = '161101'

def setup(): os.system('copy ssytool.py C:\Python27\Lib\site-packages\ssytool.py /Y')
def utf82gbk(s): return s.decode('utf8').encode('gbk')
def gbk2utf8(s): return s.decode('gbk').encode('utf8')
def u2g(s): return s.decode('utf8').encode('gbk')
def g2u(s): return s.decode('gbk').encode('utf8')

def openurl(url, timeoutTime = 10 , errorFlag = ['time']):
    if errorFlag:
        try:
            return urllib2.urlopen(url, timeout = timeoutTime).read()
        except Exception, e:
            if sum([i in str(e) for i in errorFlag]):
                return openurl(url, timeoutTime, errorFlag)
            else:
                raise e
    else:
        return urllib2.urlopen(url, timeout = timeoutTime).read()

def readText(filename, mode = 'r'):
    f = open(filename, mode)
    c = f.read()
    f.close()
    return c

def readLines(filename, strip = True, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    if strip:
        return [i.strip() for i in c]
    else:
        return c

def readCellLines(filename, spliter = ',', structure = None, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    if structure:
        return [[j(k) for j, k in zip(structure, i.strip().split(spliter))] for i in c]
    else:
        return [i.strip().split(spliter) for i in c]

def appendText(filename, text, mode = 'a'):
    f = open(filename, mode)
    f.write(text)
    f.close()

def writeText(filename, text, mode = 'w'):
    f = open(filename, mode)
    f.write(text)
    f.close()

def oswalk(path = os.getcwd()):
    l = []
    for dirname, _, filenames in os.walk(path):
        l += [os.path.join(dirname, filename) for filename in filenames]
    return l
        

def iterCellLines(filename, spliter = ',', structure = None, mode = 'r'):
    with open(filename, mode) as f:
        for line in iter(f.readline, ''):
            if structure:
                yield [j(k) for j, k in zip(structure, line.strip().split(spliter))]
            else:
                yield line.strip().split(spliter)
    
def iterLines(filename, strip = True, mode = 'r'):
    with open(filename, mode) as f:
        for line in iter(f.readline, ''):
            yield line.strip() if strip else line

if __name__ == '__main__':
    setup()
    print openurl('https://www.sasfdsfdsdasafsdaffsdafdsasfadsfdafsadf.com/', '10', ['404'])




