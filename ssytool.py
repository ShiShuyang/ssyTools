# -*- coding: utf8 -*-

import urllib2

def utf82gbk(s):
    return s.decode('utf8').encode('gbk')

def gbk2utf8(s):
    return s.decode('gbk').encode('utf8')

def openurl(url, timeoutTime = 10 ,timeoutFlag = True):
    if timeoutFlag:
        try:
            return urllib2.urlopen(url, timeout = timeoutTime).read()
        except:
            return openurl(url, timeloutTime, True)		
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

def readCellLines(filename, split, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    return [i.strip().split(split) for i in c]

def appendText(filename, text, mode = 'a'):
    f = open(filename, mode)
    f.write(text)
    f.close()

def writeText(filename, text, mode = 'w'):
    f = open(filename, mode)
    f.write(text)
    f.close()    

if __name__ == '__main__':
    print utf82gbk('中文')
    print 'miao'
