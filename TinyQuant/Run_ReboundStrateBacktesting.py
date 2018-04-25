from TinyBackTestingFrame import *
from ReboundStrate import *

if __name__ == '__main__':

    my_strate = ReboundStrate()
    frame = TinyBackTestingFrame(my_strate, "2018-04-12")
    frame.run()