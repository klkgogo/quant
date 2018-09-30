
def yield_int(n):
    for i in range(1,n):
        print("yield {0}".format(i)) #执行__next__()的时候 for循环才会被执行。
        yield(i)

if __name__ == '__main__':
    n = yield_int(10) #执行__next__()的时候 for循环才会被执行。
    n.__next__()
    for i in n:
        print("get {0}".format(i))