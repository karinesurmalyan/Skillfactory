def my_decorator(fn):
    k = {}
    def wrapper(num):
        nonlocal k
        if num not in k:
            k[num] = fn(num)
        print(k)
        return k[num]
    return wrapper

@my_decorator
def f(n):
   return n * 123456789


f(1)
f(2)
f(1)