# TEST Python file

import zmq
from ctypes import CDLL, c_int, c_char_p
import jsonplus as json
import threading
from collections import namedtuple
import timeit

def main(runs, math = 0, debug = 0, root = 0):
    start_time = timeit.default_timer()

    context1 = zmq.Context()
    control1 = context1.socket(zmq.PAIR)
    # control.bind('inproc://part_TEST_control')
    control1.bind('ipc://part_TEST1_control')

    context2 = zmq.Context()
    control2 = context2.socket(zmq.PAIR)
    control2.bind('ipc://part_TEST2_control')

    poller = zmq.Poller()
    poller.register(control1, zmq.POLLIN)
    poller.register(control2, zmq.POLLIN)

    if debug: print("Python: launching c++ .so")
    libc = CDLL("launch.so")
    t = threading.Thread(target=libc.launch, args=(runs, math, debug, root, ))
    t.start()

    i1 = 0
    i2 = 0
    while (i1 < runs or i2 < runs):
        controls = dict(poller.poll())

        if control1 in controls and i1 < runs:
            if debug: print("Python: ready to receive")
            message = control1.recv()
            message = json.loads(message)
            if debug: print("Python: received: " + str(message) + " of type: " + str(type(message)))

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