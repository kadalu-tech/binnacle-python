from binnacle.core import *


def compare_equal(value1, value2):
    task = Task.from_frameinfo()    
    task.ok = value1 == value2
    if task.ok:
        task.debug(f"Value 1 & Value 2 are same:\n{value1}")
    else:
        task.info(f"Value 1:\n{value1}\n---\nValue 2:\n{value2}")

    summary.add_completed_task(task)


def compare_not_equal(value1, value2):
    task = Task.from_frameinfo()    
    task.ok = value1 != value2
    if task.ok:
        task.debug(f"Value 1:\n{value1}\n---\nValue 2:\n{value2}")
    else:
        task.info(f"Value 1 & Value 2 are same:\n{value1}")
    summary.add_completed_task(task)

