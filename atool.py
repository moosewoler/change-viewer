################################################################################
#           atool.py
# 一些工具函数
################################################################################


def pretty(var, depth=0):
    """递归缩进式打印变量，用来替换print_dict_fine()

    var     : 待打印变量

    depth   : 打印深度

    return s: 格式化完毕的字符串
    """
    def __gettab(depth):
        TAB = ''
        for _ in range(depth):
            #TAB = TAB + '\t'
            TAB = TAB + '    '
        return TAB

    if type(var) == int:
        s = '%d\n' %(var)
    elif type(var) == str:
        s = '%s\n' %(var)
    elif type(var) == list:
        s = '[\n'
        depth = depth + 1
        for t in var:
            s = s + __gettab(depth) + pretty(t, depth)
        s = s + '\n'
        depth = depth -1 
        s = s + __gettab(depth) + ']\n'
    elif type(var) == dict:
        s = '{\n'
        depth = depth + 1
        for k in var:
            s = s + __gettab(depth) + k + '=' + pretty(var[k], depth)
        depth = depth - 1
        s = s + __gettab(depth) +'}\n'
    else:
        #return print(var)
        return var

    #if depth == 0:
    #    print(s)

    return s

def strlen(txt):
    """返回字符串长度，汉字按两个算

    txt : 字符串

    return size: 字符串长度
    """
    lenTxt = len(txt) 
    lenTxt_utf8 = len(txt.encode('utf-8')) 
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    return size

def str2num(s):
    """将数字（字符串）转换为数字

    s : 字符串

    return i: 对应的数字
    """
    try:
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        rs = list(s)
        rs.reverse()
        b = 1
        i = 0
        
        for c in rs:
            if c in numbers:   # c \in ['0', '9']
                i = i+b*int(c)
                b = b*10
            elif c == '.':
                i = i/b
                b = 1
            else:
                raise Exception("Invalid Character!")

        return i
    except Exception:
        print('Can not convert %s to number.' % (s))
        return False

# 对齐打印dict，dict各字段的值必须是字符串
import math
def print_dict_fine(d, slim=False):
    max_key_len = 0
    #max_value_len = 0
    # 找到最大key长
    for k in d:
        if strlen(k) > max_key_len:
            max_key_len = strlen(k)
        #if strlen(d[k]) > max_value_len:
        #    max_value_len = strlen(d[k])
    # 根据key长度算出合适的tab_stop，并且根据value内容截取部分
    for k in d:
        tab_stop = ''
        for i in range(int(strlen(k)/8), math.ceil(max_key_len/8)):
            tab_stop= tab_stop+'\t'
        
        if slim == False:
            if isinstance(d[k], str): 
                print('%s%s: %s' % (k, tab_stop, d[k]))
            else:
                print('%s%s: ' % (k, tab_stop), d[k])
        else:
            if strlen(d[k]) < (80-8*math.ceil(max_key_len/8)):
                if isinstance(d[k], str): 
                    print('%s%s: %s' % (k, tab_stop, d[k]))
                else:
                    print('%s%s: ' % (k, tab_stop), d[k])
            else:
                if isinstance(d[k], str): 
                    print('%s%s: %s ( 尾部省略 ... )' % (k, tab_stop, d[k][0:(80-8*math.ceil(max_key_len/8))]))
                else:
                    print('%s%s: ' % (k, tab_stop), d[k])
    print('-------------------------------------------------------------------------------')


def conv_F12_header(f12, browser):
    """将F12中复制过来的header转换成dict

    f12(dict)       : 复制过来的dict

    browser(str)    : 从哪个浏览器里复制过来的

    return r(dict)  : 可以直接作为header用的dict变量
    """

    r = {}
    if browser == 'firefox':
        for k in f12:
            headers = f12[k]
        headers= headers['headers']

        for d in headers:
            for k in d:
                if k == 'name' :
                    key = d[k]
                elif k == 'value':
                    value = d[k]
                else:
                    print('未知条目 %s: %s' % (k, d[k]))
            r[key] = value
    else:
        print('未支持的浏览器')
    return r

def conv_F12_data(f12, browser):
    r = {}
    if browser == 'firefox':
        for k in f12:
            r = f12[k]
    return r

# 打印抬头
def print_title(msg):
    tail = ''
    for i in range(0,80-strlen(msg)-6):
        tail = tail + '-'
    print('----- %s %s' % (msg, tail))

def log(s):
    import traceback
    if not hasattr(log, 'prev_func'):
        log.prev_func = 'empty'

    stackTuple = traceback.extract_stack(limit=2)[0]    # limit=2表示调用者的stack

    filename = stackTuple[0].split('/')
    linenumber = stackTuple[1]
    funcname = stackTuple[2]

    if log.prev_func == funcname:
        pass
    else:
        print("\033[1;34m---------- %s/%s() --------------------\033[0;30m" % (filename[-1], funcname))
        log.prev_func = funcname

    print("[%s]" % (linenumber), s)

def warn(s):
    import traceback
    if not hasattr(warn, 'prev_func'):
        warn.prev_func = 'empty'

    stackTuple = traceback.extract_stack(limit=2)[0]    # limit=2表示调用者的stack

    filename = stackTuple[0].split('/')
    linenumber = stackTuple[1]
    funcname = stackTuple[2]

    if warn.prev_func == funcname:
        pass
    else:
        print("\033[1;31m---------- %s/%s() --------------------\033[0;30m" % (filename[-1], funcname))
        warn.prev_func = funcname

    print("[%s]" % (linenumber), s)


# 封装logging
# https://blog.csdn.net/huangwencai123/article/details/91492727
import sys
import logging

class LoggerClass(object):
    def __init__(self, 
                 level=logging.INFO, 
                 format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s', 
                 date_format = '%Y-%m-%d %H:%M:%S',
                 file_name = ''):
        # 1. 获取一个logger对象
        self.__logger = logging.getLogger()
        # 2. 设置format对象
        self.__formatter = logging.Formatter(fmt=format,datefmt=date_format)
        # 3. 设置日志输出
        #两者也可选其一
        ## 3.1 设置文件日志模式
        #self.__logger.addHandler(self.__handler)
        # 3.2 设置终端日志模式（默认）
        self.__handler = self.get_console_handler()
        self.__logger.addHandler(self.__handler)
        # 4. 设置日志等级
        self.__logger.setLevel(level)

    def reinit(self, format, date_format, file_name):
        # 2. 设置format对象
        self.__formatter = logging.Formatter(fmt=format,datefmt=date_format)
        # 3. 设置日志输出
        if file_name != '':
            self.__logger.removeHandler(self.__handler)
            self.__handler = self.get_file_handler(file_name)
            self.__logger.addHandler(self.__handler)

    def get_file_handler(self, filename):
        # 1. 获取一个文件日志handler
        filehandler = logging.FileHandler(filename=filename,encoding="utf-8")
        # 2. 设置日志格式
        filehandler.setFormatter(self.__formatter)
        # 3. 返回
        return filehandler

    def get_console_handler(self):
        # 1. 获取一个输出到终端日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 2. 设置日志格式
        console_handler.setFormatter(self.__formatter)
        # 3. 返回handler
        return console_handler

    @property
    def log(self):
        return self.__logger

Logger = LoggerClass()