import os
import inspect
from datetime import datetime
from functools import wraps

import requests
from termcolor import colored

_verbose = os.environ.get("DEBUG", "false").lower() in ["true", "1", "yes"]
TASK_LINE_LENGTH = 42
_light_bg = os.environ.get("LIGHT_BG", "false").lower() in ["true", "1", "yes"]

def debug_color():
    return "dark_grey" if _light_bg else "light_yellow"


def task_line(line):
    if len(line) <= TASK_LINE_LENGTH:
        return f"%-{TASK_LINE_LENGTH + 3}s" % line

    return f"{line[0:TASK_LINE_LENGTH]}..."


def humanize_duration(value):
    if value > 1:
        return "%6.2fs" % value

    return "%6.2fms" % (value * 1000)


class Task:
    def __init__(self):
        self.id = 0
        self.filename = ""
        self.line_number = -1
        self.line = ""
        self.duration_seconds = 0
        self.ok = False
        self.start_time = datetime.now()
        self.verbose_output = []
        self.info_output = []

    def debug(self, msg):
        if _verbose:
            self.verbose_output += msg.split("\n")

    def info(self, msg):
        self.info_output += msg.split("\n")

    def completed(self):
        self.end_time = datetime.now()
        self.duration_seconds = (datetime.now() - self.start_time).total_seconds()
        
    def show(self):
        for msg in self.info_output:
            print(colored(f"# {msg}", debug_color()))

        for msg in self.verbose_output:
            print(colored(f"# {msg}", debug_color()))

        output = "[%s] [%3d]  file=%s:%s  [%s]" % (
            humanize_duration(self.duration_seconds),
            self.id,
            self.filename,
            self.line_number,
            task_line(self.line)
        )
        print("%s  %s" % (ok_not_ok(self.ok), colored(output, attrs=["bold"])))

    @classmethod
    def from_frameinfo(cls):
        info = inspect.stack()[2]
        task = cls()
        task.filename = info.filename
        task.line_number = info.lineno
        task.line = info.code_context[0].strip()
        return task

def ok_not_ok(condition):
    if condition:
        return colored("%-6s" % "OK", "green")

    return colored("%-6s" % "NOT OK", "red")


class Summary:
    def __init__(self):
        self.tasks = []
        self.count = 0
        self.ok_tasks = 0
        self.start_time = datetime.now()

    def add_completed_task(self, task, show = True):
        task.completed()
        task.id = self.count + 1
        if task.ok:
            self.ok_tasks += 1

        self.tasks.append(task)
        self.count += 1
        if show:
            task.show()

    def show(self):
        self.end_time = datetime.now()
        self.duration_seconds = (datetime.now() - self.start_time).total_seconds()

        output = "[%s]  total=%s  passed=%s  failed=%s" % (
            humanize_duration(self.duration_seconds),
            self.count,
            self.ok_tasks,
            self.count - self.ok_tasks
        )
        print("%s  %s" % (
            ok_not_ok(self.ok_tasks == self.count),
            colored(output, attrs=["bold"])
        ))


summary = Summary()

def show_summary():
    print("#")
    print("# Summary:")
    summary.show()


def debug(msg):
    if not _verbose:
        return

    msg_data = f"{msg}"
    for line in msg_data.split("\n"):
        print(colored(f"# {line}", debug_color()))


def binnacle_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task = Task.from_frameinfo()
        kwargs["task"] = task
        ret = None

        try:
            ret = func(*args, **kwargs)
        except Exception as ex:
            debug(ex)

        summary.add_completed_task(task)
        return ret

    return wrapper
