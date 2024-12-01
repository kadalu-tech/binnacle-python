from binnacle.core import binnacle_task

@binnacle_task
def compare_equal(value1, value2, task=None):
    task.ok = value1 == value2
    if task.ok:
        task.debug(f"Value 1 & Value 2 are same:\n{value1}")
    else:
        task.info(f"Value 1:\n{value1}\n---\nValue 2:\n{value2}")


@binnacle_task
def compare_not_equal(value1, value2, task=None):
    task.ok = value1 != value2
    if task.ok:
        task.debug(f"Value 1:\n{value1}\n---\nValue 2:\n{value2}")
    else:
        task.info(f"Value 1 & Value 2 are same:\n{value1}")
