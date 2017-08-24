# -*- coding: utf8 -*-
import urllib2, os, hashlib
import math
from datetime import datetime, timedelta
__version__ = '161208'

def setup(): os.system('copy ssytool.py C:\Python27\Lib\site-packages\ssytool.py /Y')
def utf82gbk(s): return s.decode('utf8').encode('gbk')
def gbk2utf8(s): return s.decode('gbk').encode('utf8')
def u2g(s): return s.decode('utf8').encode('gbk')
def g2u(s): return s.decode('gbk').encode('utf8')

class date():    
    def __init__(self, s):
        self.__s = s
        self.__t = datetime.strptime(s, '%y%m%d %H%M%S')
    def __getattr__(self, attrname):
        if attrname == 'datetime': return self.__t
        if attrname == 'year': return self.__t.year%100
        elif attrname == 'month': return self.__t.month
        elif attrname == 'day': return self.__t.day
        elif attrname == 'hour': return self.__t.hour
        elif attrname == 'minute': return self.__t.minute
        elif attrname == 'second': return self.__t.second
        elif attrname == 'weekday': return self.__t.weekday()+1
        elif attrname == 'tuple': return (self.__t.year%100, self.__t.month, self.__t.day, self.__t.hour, self.__t.minute, self.__t.second)
        elif attrname == 'toString': return datetime.strftime(self.__t, '%y%m%d %H%M%S')
        else: raise AttributeError,attrname
    def __str__(self): return datetime.strftime(self.__t, '%y%m%d %H%M%S')
    __repr__ = __str__
    def __sub__(self, other):
        if type(other) == int:
            delta = timedelta(0, other)
            result = self.__t - delta
            return date(datetime.strftime(result, '%y%m%d %H%M%S'))
        else:
            delta = self.datetime - other.datetime
            return int(delta.total_seconds())
    def __add__(self, other):
        delta = timedelta(0, other)
        result = self.__t + delta
        return date(datetime.strftime(result, '%y%m%d %H%M%S'))
    def __lt__(self, other): return self.datetime < other.datetime
    def __le__(self, other): return self.datetime <= other.datetime
    def __gt__(self, other): return self.datetime > other.datetime
    def __ge__(self, other): return self.datetime >= other.datetime
    def __eq__(self, other): return self.datetime == other.datetime
    def __nq__(self, other): return self.datetime != other.datetime

def haversine(point1, point2):
    lon1, lat1, lon2, lat2 = map(math.radians, [point1[0], point1[1], point2[0], point2[1]])    
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  
    c = 2 * math.asin(math.sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000

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
    return [i.strip() for i in c] if strip else c

def readCellLines(filename, spliter = ',', structure = None, jumpLines = 0, mode = 'r'):
    f = open(filename, mode)
    c = f.readlines()
    f.close()
    c = c[jumpLines:]
    if structure:
        if type(structure) is list:
            return [[j(k) for j, k in zip(structure, line.strip().split(spliter))] for line in c]
        else:
            return [[structure(k) for k in line.strip().split(spliter)] for line in c]
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

def formatLine(l, spliter = ',', endWithEnter = True):
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
    
def viewFile(filename, limit = 10, jumplines = 0, mode = 'r'):
    f = open(filename, mode)
    c = ''
    for i in xrange(jumplines): f.readline()
    for i in xrange(limit): c += f.readline()
    f.close()
    return c

if __name__ == '__main__':
    setup()
    print viewFile('test.txt', 100, 3)
    for line in iterCellLines('test.txt', jumpLines = 2, structure = str):
        print line
    print fileCharacteristic('J:\BaiduYunDownload\moon.cia', 100000)
    print fileCharacteristic('J:\BaiduYunDownload\Pokemon Moon (ALL) (RF).cia', 100000)

