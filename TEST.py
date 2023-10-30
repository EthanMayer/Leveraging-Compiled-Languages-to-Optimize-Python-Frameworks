# TEST Python file

import zmq
import jsonplus as json
import threading
from collections import namedtuple
import timeit
import os

def fib(n):
    if (n == 0): return 0
    if (n == 1): return 1

    prevNum = 0
    curNum = 1

    for i in range(2,n+1):
        prevPrevNum = prevNum
        prevNum = curNum
        curNum = prevNum + prevPrevNum

    return curNum

def fib_recursive(n):
    if (n == 0): return 0
    if (n == 1): return 1

    return (fib_recursive(n - 1) + fib_recursive(n - 2))

def memory_alloc():
    lists = [None] * 100

    for i in range(0,100):
        lists[i] = [0]*4096

def threadBody(context, addr, runs, test_type = 0, debug = 0, root = 0):
    from math import sqrt

    control = context.socket(zmq.PAIR)
    control.connect(addr)

    i = 0
    while (i < runs):
        if debug: print("Python_Thread: ready to send")

        if (test_type == 0): 
            send = json.dumps(("Contents", "Ready"))
        elif (test_type == 1):
            if root:
                x = fib(int(sqrt(i)))
            else:
                x = fib(int(i))
            send_str = "Fibonacci number of sqrt(" + str(i) + ")"
            send = json.dumps((send_str, x))
        elif (test_type == 2):
            if root:
                x = fib_recursive(int(sqrt(i)))
            else:
                x = fib_recursive(int(i))
            send_str = "Recursive Fibonacci number of sqrt(" + str(i) + ")"
            send = json.dumps((send_str, x))
        elif (test_type == 3):
            memory_alloc()
            send = json.dumps(("Memory Allocated", "4096 * 100"))

        control.send(bytes(send, encoding='utf8'))

        if debug: print("Python_Thread: ready to receive")
        message = control.recv()
        message = json.loads(message)
        if debug: print("Python_Thread: received: " + str(message))
        # i = message.y
        i = i + 1

def main(type, runs, test_type = 0, debug = 0, root = 0):
    os.sched_setaffinity(0, 1)
    start_time = timeit.default_timer()

    context1 = zmq.Context()
    control1 = context1.socket(zmq.PAIR)
    if type:
        control1.bind('ipc://part_TEST1_control')
    else:
        control1.bind('inproc://PYTHON_TEST1_control')

    context2 = zmq.Context()
    control2 = context2.socket(zmq.PAIR)
    if type:
        control2.bind('ipc://part_TEST2_control')
    else:
        control2.bind('inproc://PYTHON_TEST2_control')

    poller = zmq.Poller()
    poller.register(control1, zmq.POLLIN)
    poller.register(control2, zmq.POLLIN)

    if type:
        from ctypes import CDLL

        if debug: print("Python: launching c++ .so")
        libc = CDLL("launch.so")
        t = threading.Thread(target=libc.launch, args=(runs, test_type, debug, root, ))
        t.start()
    else:
        t = threading.Thread(target=threadBody, args=(context1, 'inproc://PYTHON_TEST1_control', runs, test_type, debug, root, ))
        t.start()

        os.sched_setaffinity(t.native_id, 2)

        t2 = threading.Thread(target=threadBody, args=(context2, 'inproc://PYTHON_TEST2_control', runs, test_type, debug, root, ))
        t2.start()

        os.sched_setaffinity(t2.native_id, 3)

    i1 = 0
    i2 = 0
    while (i1 < runs or i2 < runs):
        controls = dict(poller.poll())

        if control1 in controls and i1 < runs:
            if debug: print("Python: ready to receive")
            message = control1.recv()
            message = json.loads(message)
            if debug: print("Python: received: " + str(message))

            Point = namedtuple("Point", ["x", "y"])
            send = json.dumps(Point(i1, i1+1))
            # send = json.pretty({"dot": Point(1, 2)})
            control1.send(bytes(send, encoding='utf8'))
            i1 = i1 + 1

        if control2 in controls and i2 < runs:
            message = control2.recv()
            message = json.loads(message)

            Point = namedtuple("Point", ["x", "y"])
            send = json.dumps(Point(i2, i2+1))
            control2.send(bytes(send, encoding='utf8'))
            i2 = i2 + 1

    if debug: print("Python: Exiting")

    end_time = timeit.default_timer()
    total_time = end_time - start_time
    return total_time