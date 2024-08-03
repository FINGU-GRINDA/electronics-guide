# import asyncio

# tasks = {}

# def create_task(task_id, async_gen):
#     async def run_generator():
#         async for item in async_gen:
#             # Here, you would normally do something with the item
#             pass

#     tasks[task_id] = asyncio.create_task(run_generator())

# def get_task(task_id):
#     return tasks.get(task_id)

# def cancel_task(task_id):
#     task = tasks.get(task_id)
#     if task:
#         task.cancel()
#         return True
#     return False

# def remove_task(task_id):
#     if task_id in tasks:
#         del tasks[task_id]
