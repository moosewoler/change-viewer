# 一些函数
def conv_F12_header(f12, browser):
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

# 返回字符串长度，汉字按两个算
def strlen(txt):
    lenTxt = len(txt) 
    lenTxt_utf8 = len(txt.encode('utf-8')) 
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    return size

# 打印抬头
def print_title(msg):
    tail = ''
    for i in range(0,80-strlen(msg)-6):
        tail = tail + '-'
    print('----- %s %s' % (msg, tail))

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
    
# 将数字（字符串）转换为数字
def str2num(s):
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