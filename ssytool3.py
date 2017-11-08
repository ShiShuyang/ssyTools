import os, hashlib, math, multiprocessing, functools
from datetime import datetime, timedelta
__version__ = '171108'

defaultCoding='utf8'
class f:
    def viewFile(filename, limit=10, jumplines=0, encoding=defaultCoding):
        f = open(filename, encoding=encoding)
        c = ''
        for i in range(jumplines): f.readline()
        for i in range(limit): c += f.readline()
        f.close()
        print(c)
        
    def fileCharacteristic(filename, length = 0):
        m = hashlib.md5()
        f = open(filename, 'rb')
        c = f.read(length) if length else f.read()
        f.close()
        m.update(c)
        ans = m.hexdigest()    
        return ans

    def readText(filename, encoding=defaultCoding):
        f = open(filename, encoding=encoding)
        c = f.read()
        f.close()
        return c

    def appandText(filename, text, encoding=defaultCoding):
        f = open(filename, 'a', encoding=encoding)
        f.write(text)
        f.close()

    def writeText(filename, text, encoding=defaultCoding):
        f = open(filename, 'w', encoding=encoding)
        f.write(text)
        f.close()

    def iterLines(filename, strip=True, jumpLines=0, encoding=defaultCoding):
        with open(filename, encoding=defaultCoding) as f:
            iterfile = iter(f.readline, '')
            for i in range(jumpLines): next(iterfile)
            for line in iterfile:
                yield line.strip() if strip else line

    def iterCellLines(filename, structure=None, delimiter=',', jumpLines=0, encoding=defaultCoding):
        with open(filename, encoding=encoding) as f:
            iterfile = iter(f.readline, '')
            for i in range(jumpLines): next(iterfile)
            for line in iterfile:
                if structure:
                    if type(structure) is list:
                        yield [j(k) for j, k in zip(structure, line.strip().split(delimiter))]
                    else:
                        yield [structure(k) for k in line.strip().split(delimiter)]
                else:
                    yield line.strip().split(delimiter)
    icl = iterCellLines

    def formatLine(l, spliter = ',', endWithEnter = True):
        sentence = spliter.join(map(str, l)) 
        return sentence + '\n' if endWithEnter else sentence

def oswalk(path = os.getcwd()):
    l = []
    for dirname, _, filenames in os.walk(path):
        l += [os.path.join(dirname, filename) for filename in filenames]
    return l

def entropy(l):
    s, e = sum(l), 0.0
    for i in l:
        if i:
            p = 1.0*i/s
            e += p*math.log(p)
    return e 

class geo:
    def haversine(point1, point2):
        lon1, lat1, lon2, lat2 = list(map(math.radians, [point1[0], point1[1], point2[0], point2[1]]))    
        dlon = lon2 - lon1   
        dlat = lat2 - lat1   
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  
        c = 2 * math.asin(math.sqrt(a))   
        r = 6371 # 地球平均半径，单位为公里  
        return c * r * 1000
    class date:    
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
            else: raise AttributeError(attrname)
        def __str__(self): return datetime.strftime(self.__t, '%y%m%d %H%M%S')
        __repr__ = __str__
        def __sub__(self, other):
            if type(other) == int:
                delta = timedelta(0, other)
                result = self.__t - delta
                return geo.date(datetime.strftime(result, '%y%m%d %H%M%S'))
            else:
                delta = self.datetime - other.datetime
                return int(delta.total_seconds())
        def __add__(self, other):
            delta = timedelta(0, other)
            result = self.__t + delta
            return geo.date(datetime.strftime(result, '%y%m%d %H%M%S'))
        __radd__ = __add__
        def __lt__(self, other): return self.datetime < other.datetime
        def __le__(self, other): return self.datetime <= other.datetime
        def __gt__(self, other): return self.datetime > other.datetime
        def __ge__(self, other): return self.datetime >= other.datetime
        def __eq__(self, other): return self.datetime == other.datetime
        def __nq__(self, other): return self.datetime != other.datetime

    class metrotime:
        def __init__(self, s):
            self.hour = int(s[:2])
            self.minute = int(s[2:4])
            self.second = int(s[4:])
            self.__f = lambda x: str(x) if x>=10 else '0' + str(x) 
        def __getattr__(self, attrname):
            if attrname == 'abs_second': return 3600*self.hour + 60*self.minute + self.second
            else: raise AttributeError(attrname) 
        def __str__(self):        
            s = list(map(self.__f, [self.hour, self.minute, self.second]))
            return ''.join(s)
        __repr__ = __str__
        def abs_second2time(self, n):
            h = n/3600
            m = (n-h*3600)/60
            s = n - h*3600 - m*60
            return geo.metrotime(''.join(map(self.__f, [h, m, s])))
        def __sub__(self, other):
            if type(other) is int:
                return self.abs_second2time(self.abs_second - other)
            else:
                return self.abs_second - other.abs_second
        def __add__(self, other):
            return self.abs_second2time(self.abs_second + other)
        __radd__ = __add__
        def __lt__(self, other): return self.abs_second < other.abs_second
        def __le__(self, other): return self.abs_second <= other.abs_second
        def __gt__(self, other): return self.abs_second > other.abs_second
        def __ge__(self, other): return self.abs_second >= other.abs_second
        def __eq__(self, other): return self.abs_second == other.abs_second
        def __nq__(self, other): return self.abs_second != other.datetime.abs_second

class mp:
    def multiFile(filelist, function, args=None, processNum=4):
        result = []
        pool = multiprocessing.Pool(processNum)
        for filename in filelist:
            a = (filename, ) + tuple(args) if args else (filename, )
            result.append(pool.apply_async(function, a))
        pool.close()
        pool.join()
        return [x.get() for x in result]
    def worker(lines, structure, delimiter, function, args):
        result = []
        for line in lines:
            if type(structure) is list:
                line = [j(k) for j, k in zip(structure, line.strip().split(delimiter))]
            else:
                line = [structure(k) for k in line.strip().split(delimiter)]
            result.append(line)
        args = (result, ) + tuple(args) if args else (result, )
        return function(*args)           
    def singleFile(filename, function, args=None, structure=str, delimiter=',', processNum=6, buff=5000000, jumpLines=0):
        with open(filename, 'r') as f:
            for i in range(jumpLines): f.readline()
            result = []
            pool = multiprocessing.Pool(processNum)
            lines = f.readlines(buff)
            while lines:
                result.append(pool.apply_async(mp.worker, (lines, structure, delimiter, function, args)))
                lines = f.readlines(buff)
            pool.close()
            pool.join()    
        return [x.get() for x in result]
    def add(l): return functools.reduce(lambda x, y: x+y, l)
        
        
if __name__ == '__main__':
    print(fileCharacteristic('test.txt', 12))

