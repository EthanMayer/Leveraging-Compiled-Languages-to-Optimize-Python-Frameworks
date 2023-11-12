# Leveraging Compiled Languages to Optimize Python Frameworks
# Master's Thesis Research
#
# Test File
# This file performs the research tests for either the Python Control Implementation or the Python + C++ Prototype.
#
# @author: EthanMayer
#
# Copyright 2023 Ethan Mayer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
import zmq
import jsonplus as json
import threading
from collections import namedtuple
import timeit # timer used for benchmark times
# import os # not used since sched_setaffinity only works for Linux

# Iterative Fibonacci function implementation for Python
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

# Recursive Fibonacci function implementation for Python
def fib_recursive(n):
    if (n == 0): return 0
    if (n == 1): return 1

    return (fib_recursive(n - 1) + fib_recursive(n - 2))

# Memory allocation function implementation for Python
def memory_alloc():
    lists = [None] * 100

    # Allocate a 4096 length list of 0, 100 times
    for i in range(0,100):
        lists[i] = [0]*4096

# Thread function body implementation for Python
def threadBody(context, addr, runs, test_type = 0, debug = 0, root = 0):
    from math import sqrt

    # Create ZMQ PAIR socket from address supplied via function parameter
    control = context.socket(zmq.PAIR)
    control.connect(addr)

    # Test run loop
    i = 0
    while (i < runs):
        if debug: print("Python_Thread: ready to send")

        # If no work, just send back simple JSON string message
        if (test_type == 0): 
            send = json.dumps(("Contents", "Ready"))

        elif (test_type == 1):

            # If light math work, send iterative Fibonacci of square root of message number
            if root:
                x = fib(int(sqrt(i)))

            # If heavy math work, send iterative Fibonacci of message number
            else:
                x = fib(int(i))
            send_str = "Fibonacci number of sqrt(" + str(i) + ")"
            send = json.dumps((send_str, x))

        elif (test_type == 2):

            # If light function call work, send recursive Fibonacci of square root of message number
            if root:
                x = fib_recursive(int(sqrt(i)))

            # If heavy function call work, send recursive Fibonacci of message number
            else:
                x = fib_recursive(int(i))
            send_str = "Recursive Fibonacci number of sqrt(" + str(i) + ")"
            send = json.dumps((send_str, x))

        # If memory allocation work, allocate memory before sending message back
        elif (test_type == 3):
            memory_alloc()
            send = json.dumps(("Memory Allocated", "4096 * 100"))

        # Send message to main thread
        control.send(bytes(send, encoding='utf8'))

        # Receive message from main thread
        if debug: print("Python_Thread: ready to receive")
        message = control.recv()
        message = json.loads(message)
        if debug: print("Python_Thread: received: " + str(message))

        i = i + 1

# Setup appropriate test (Python vs Python + C++) and launch threads
def main(type, runs, test_type = 0, debug = 0, root = 0):
    # os.sched_setaffinity(0, 1) # ONLY FOR LINUX, DOES NOT WORK ON MACOS SO UNUSED

    # Start timer
    start_time = timeit.default_timer()

    # Setup main thread ZMQ PAIR socket for thread 1
    context1 = zmq.Context()
    control1 = context1.socket(zmq.PAIR)

    # Use in-process communication for Python threads
    if type:
        control1.bind('ipc://part_TEST1_control')

    # Use inter-process communication for C++ pthreads
    else:
        control1.bind('inproc://PYTHON_TEST1_control')

    # Setup main thread ZMQ PAIR socket for thread 2
    context2 = zmq.Context()
    control2 = context2.socket(zmq.PAIR)

    # Use in-process communication for Python threads
    if type:
        control2.bind('ipc://part_TEST2_control')

    # Use inter-process communication for C++ pthreads
    else:
        control2.bind('inproc://PYTHON_TEST2_control')

    # Setup ZMQ poller to handle incoming messages so the main thread does not block on waiting to receive
    poller = zmq.Poller()
    poller.register(control1, zmq.POLLIN)
    poller.register(control2, zmq.POLLIN)

    # If test type is C++, load function from .so shared library and launch pthreads
    if type:
        from ctypes import CDLL

        if debug: print("Python: launching c++ .so")
        libc = CDLL("launch.so")
        t = threading.Thread(target=libc.launch, args=(runs, test_type, debug, root, ))
        t.start()

    # If test type is Python, launch Python threads with thread body function
    else:
        t = threading.Thread(target=threadBody, args=(context1, 'inproc://PYTHON_TEST1_control', runs, test_type, debug, root, ))
        t.start()

        # os.sched_setaffinity(t.native_id, 2) # ONLY FOR LINUX, DOES NOT WORK ON MACOS SO UNUSED

        t2 = threading.Thread(target=threadBody, args=(context2, 'inproc://PYTHON_TEST2_control', runs, test_type, debug, root, ))
        t2.start()

        # os.sched_setaffinity(t2.native_id, 3) # ONLY FOR LINUX, DOES NOT WORK ON MACOS SO UNUSED

    # Main thread test loop
    i1 = 0
    i2 = 0
    while (i1 < runs or i2 < runs):
        controls = dict(poller.poll())

        # If message waiting for ZMQ socket for thread 1, handle it
        if control1 in controls and i1 < runs:

            # Receive message from thread
            if debug: print("Python: ready to receive")
            message = control1.recv()
            message = json.loads(message)
            if debug: print("Python: received: " + str(message))

            # Send message to thread
            Point = namedtuple("Point", ["x", "y"])
            send = json.dumps(Point(i1, i1+1))
            control1.send(bytes(send, encoding='utf8'))

            i1 = i1 + 1

        # If message waiting for ZMQ socket for thread 2, handle it
        if control2 in controls and i2 < runs:

            # Receive message from thread
            message = control2.recv()
            message = json.loads(message)

            # Send message to thread
            Point = namedtuple("Point", ["x", "y"])
            send = json.dumps(Point(i2, i2+1))
            control2.send(bytes(send, encoding='utf8'))
            
            i2 = i2 + 1

    if debug: print("Python: Exiting")

    # End timer once test ends
    end_time = timeit.default_timer()

    # Calculate time passed and report time to driver
    total_time = end_time - start_time
    return total_time