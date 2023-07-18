import sys
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

def load(n: int) -> str:
    fib1 = fib2 = 1
    n -= 2
    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1
    return str(fib2)


# import asyncio

# async def load(n: int):
#     await asyncio.sleep(n)
#     return 'OK'