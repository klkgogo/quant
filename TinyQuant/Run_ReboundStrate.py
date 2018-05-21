# encoding: UTF-8

'''
    策略运行脚本
'''

from TinyQuantFrame import *
from ReboundStrate import *

if __name__ == '__main__':
    my_strate = ReboundStrateWarrant()
    frame = TinyQuantFrame(my_strate)
    frame.run()