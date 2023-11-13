# import asyncio
#
#
# async def f1():
#     print('f1:1')
#     await asyncio.sleep(12)
#     print('f1:2')
#     return 1
#
#
# async def f2():
#     print('f2:1')
#     await asyncio.sleep(2)
#     print('f2:2')
#     return 2
#
# # async def f():
# #     await f1()
# #     await f2()
#
#
# async def f():
#     res=await asyncio.gather(f1(), f2())
#     print(res)
#
#
# asyncio.run(f())

import asyncio


async def func1():
    await asyncio.sleep(12)
    print('协程1')
    return "协程1"


async def func2():
    await asyncio.sleep(2)
    print('协程2')
    return "协程2"


# task可为列表,即任务列表
# task = func1()
task = [func1(), func2()]
# 创建事件循环
loop = asyncio.get_event_loop()
# 添加任务，直至所有任务执行完成
res=loop.run_until_complete(asyncio.wait(task))
print(res)
# 关闭事件循环
loop.close()
# 事件循环关闭后，再次调用loop，将不会再次执行。