# -*- coding: utf8 -*-
import urllib2, os, hashlib
__version__ = '161109'

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

def readLines(filename, strip = True, jumpLines = 0, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    c = c[jumpLines:]
    if strip:
        return [i.strip() for i in c]
    else:
        return c

def readCellLines(filename, spliter = ',', structure = None, jumpLines = 0, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    c = c[jumpLines:]
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
        

def iterCellLines(filename, spliter = ',', structure = None, jumpLines = 0, mode = 'r'):
    with open(filename, mode) as f:
        iterfile = iter(f.readline, '')
        for i in xrange(jumpLines): iterfile.next()
        for line in iterfile:
            if structure:
                if type(structure) is list:
                    yield [j(k) for j, k in zip(structure, line.strip().split(spliter))]
                else:
                    yield [structure(k) for k in line.strip().split(spliter)]
            else:
                yield line.strip().split(spliter)
    
def iterLines(filename, strip = True, jumpLines = 0, mode = 'r'):
    with open(filename, mode) as f:
        iterfile = iter(f.readline, '')
        for i in xrange(jumpLines): iterfile.next()
        for line in iterfile:
            yield line.strip() if strip else line

def formatline(l, spliter = ',', endWithEnter = True):
    sentence = spliter.join(map(str, l))
    return sentence + '\n' if endWithEnter else sentence

def fileCharacteristic(filename, length = 0):
    m = hashlib.md5()
    f = open(filename, 'rb')
    c = f.read(length) if length else f.read()
    f.close()
    m.update(c)
    ans = m.hexdigest()    
    return ans
    
        

if __name__ == '__main__':
    setup()
    for line in iterCellLines('test.txt', jumpLines = 2, structure = str):
        print line
    print fileCharacteristic('J:\BaiduYunDownload\moon.cia', 100000)
    print fileCharacteristic('J:\BaiduYunDownload\Pokemon Moon (ALL) (RF).cia', 100000)

