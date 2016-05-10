# -*- coding: utf8 -*-

def utf82gbk(s):
    return s.decode('utf8').encode('gbk')

def gbk2utf8(s):
    return s.decode('gbk').encode('utf8')


if __name__ == '__main__':
    print utf82gbk('中文')
