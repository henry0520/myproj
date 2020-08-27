"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

Task decorators

"""

from celery.task import task
from celery.task import periodic_task
from celery.canvas import subtask
from myproj.celery import app

__all__ = ["app", "task", "subtask", "periodic_task"]
