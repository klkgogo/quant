i = 1
print(type(i))

b = 1 > 2
print(type(b))

print(isinstance(b, bool))
print(isinstance(b, int))
print(isinstance(b, float))

price_str = '10.4, 10, 10.2, 9, 9.5'
print(id(price_str))
price_str = price_str.replace(" ", "")
print(id(price_str))
print(price_str)
prices = price_str.split(',')
print(prices)
print(type(prices))
prices += '3'
print(prices)

prices_set = set(prices)
print(prices_set)
prices_set.add("45")
print(prices_set)
prices_set.remove('3')
print(prices_set)

date_array=[]
date_base = 20170110
for i in range(9):
    date_array.append(str(date_base))
    date_base += 1
print(date_array)

for i, v in enumerate(prices):
    print(i, ":", v)

# using generator
gen = (x * x for x in range(10))
print("gen:", gen)
for i in gen:
    print(i)
l = [gen]
print("list:", l)
date_array = [str(date_base + v) for _, v in enumerate(range(len(prices)))]
print(date_array)

# tuple
date_price = [(date, price) for date, price in zip(date_array, prices)]
print(date_price)

# name tuple
from collections import namedtuple
stock_namedtuple = namedtuple("stock", ("date", "price"))
stock_named_list = [stock_namedtuple(date, price) for date, price in zip(date_array, prices)]
print(stock_named_list)
print(stock_named_list[1].date,":", stock_named_list[1].price)

# dict derive
stock_dict = {key : float(v) for key, v in zip(date_array, prices)}
print(stock_dict)
print(stock_dict.keys())
print(stock_dict.values())
print("20170119日价格: {}".format(stock_dict['20170119']))

# find min prices of the dict
print(stock_dict.values())
print(min(zip(stock_dict.values(), stock_dict.keys())))


# function
def find_second_max(dict_array):
    dict_sorted = sorted(zip(stock_dict.values(), stock_dict.keys()))
    return dict_sorted[-2]

print(find_second_max(stock_dict))

fun = find_second_max
print(fun(stock_dict))

# function lambda
find_second_max_lambda = lambda dict_array: sorted(zip(dict_array.values(), dict_array.keys()))[-2]
print(find_second_max_lambda(stock_dict))

# reduce
from functools import reduce
add = lambda a, b : a + b
print(reduce(add, [1, 2, 3, 4, 5]))

# ordered dict
from collections import  OrderedDict
stock_dict_order = OrderedDict((key, float(v)) for key, v in zip(date_array, prices))
print(stock_dict_order)

change_ratio = lambda a, b : round((b - a) / a, 3)
changes = [change_ratio(a, b) for a, b in zip(list(stock_dict_order.values())[:-1], list(stock_dict_order.values())[1:])]
print(changes)
print(list(stock_dict_order.values()))
changes.insert(0, 0)


#revert a list
l = [ 9 , 1, 8, 2, 3, 4, 5]
sort_l = sorted(l)
print(sort_l)
# revert
sort_l = sort_l[::-1]
print(sort_l)
print(sort_l[4:1:-1])
