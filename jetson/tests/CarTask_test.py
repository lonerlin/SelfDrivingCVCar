import sys
sys.path.append('..')
from car.car_task import CarTask
from car.car_timer import CarTimer
import time

task_list = []


def _do_work(**kwargs):
    direction = kwargs['direction']
    print("direction:{}".format(direction))


def do(direction=True, delay=3):
    task_list.append(CarTask(name="hello", activated=True, priority=1,
                             timer=CarTimer(start_time=time.perf_counter(), interval=delay),
                             work=_do_work, direction=direction))


def update():

    for task in task_list:
        while not task.timer.timeout():
            task.work_function(task.args)
            time.sleep(0.1)


if __name__ == '__main__':
   do()
   for task in task_list:
       task.work_function(**task.args)