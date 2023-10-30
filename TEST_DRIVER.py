from TEST import main
from statistics import median, mean, stdev
import numpy as np
import sys
import os
from csv import writer
import os.path
import time

PYTHON = 0
CPP = 1
times = []

runs = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
test_type = int(sys.argv[2]) if len(sys.argv) > 2 else 0
root = int(sys.argv[3]) if len(sys.argv) > 3 else 1
debug = int(sys.argv[4]) if len(sys.argv) > 4 else 0
tests = int(sys.argv[5]) if len(sys.argv) > 5 else 10

# Append a list as a row to the CSV
def append_list_as_row(write_obj, list_of_elem):
    # Create a writer object from csv module
    csv_writer = writer(write_obj)
    # Add contents of list as last row in the csv file
    csv_writer.writerow(list_of_elem)

def run():
    global times
    times1 = []
    times2 = []

    print("===================================")
    print("SPEED TESTS")
    print("Parameters:")
    print("Tests Per Category: " + str(tests))
    print("Messages Per Test: " + str(runs))
    if (test_type == 0):
        print("Work Between Messages: " + str(bool(test_type)))
    elif (test_type == 1):
        print("Math Between Messages: " + str(bool(test_type)))
    elif (test_type == 2):
        print("Function Calls Between Messages: " + str(bool(test_type)))
    elif (test_type == 3):
        print("Memory Allocation Between Messages: " + str(bool(test_type)))
    print("Debug Print: " + str(bool(debug)))
    if (test_type == 1): print("Square Root Fib: " + str(bool(root)))
    print("===================================")

    print("===================================")
    print("Running PURE PYTHON Tests...")

    for i in range(tests):
        times1.append(main(PYTHON, runs, test_type, debug, root))

    times1 = list(np.around(np.array(times1), 3))

    times.append(times1)

    median1 = round(median(times1), 3)
    mean1 = round(mean(times1), 3)
    std1 = round(stdev(times1), 3)

    print("Median time (Python): " + str(median1))
    print("Mean time (Python): " + str(mean1))
    print("Standard Deviation (Python): " + str(std1))
    print("All times (Python): " + str(times1))

    print("===================================")
    print("Running PYTHON + C++ Tests...")

    for i in range(tests):
        times2.append(main(CPP, runs, test_type, debug, root))

    times2 = list(np.around(np.array(times2), 3))

    times.append(times2)

    median2 = round(median(times2), 3)
    mean2 = round(mean(times2), 3)
    std2 = round(stdev(times2), 3)

    print("Median time (Python + C++): " + str(median2))
    print("Mean time (Python + C++): " + str(mean2))
    print("Standard Deviation (Python + C++): " + str(std2))
    print("All times (Python + C++): " + str(times2))

    speedup = round(((mean2 - mean1) / mean1 * 100), 3)
    print("Average runtime difference: " + str(speedup) + "%")

# os.sched_setaffinity(0, 0)

# Initialize CSV file for recording IMU data
if not os.path.exists("data"):
    os.makedirs("data")
timestr = time.strftime("%Y%m%d-%H%M%S")
file_name = "data/LOG_" + timestr + ".csv"
open(file_name, 'w+', newline='')

with open(file_name, 'a+', newline='') as write_obj:

    # Write column titles to csv
    csvTitles = ["Python - 100k", "C++ - 100k", "Python - 500k", "C++ - 500k", "Python - 100k, Sqrt Fib", "C++ - 100k, Sqrt Fib", "Python - 500k, Sqrt Fib", "C++ - 500k, Sqrt Fib", "Python - 1k, Fib", "C++ - 1k, Fib", "Python - 5k, Fib", "C++ - 5k, Fib", "Python - 1k, Functions", "C++ - 1k, Functions", "Python - 5k, Functions", "C++ - 5k, Functions", "Python - 100k, Memory", "C++ - 100k, Memory", "Python - 500k, Memory", "C++ - 500k, Memory"]
    append_list_as_row(write_obj, csvTitles)
        
    debug = 0
    tests = 10
    root = 1

    runs = 100000
    test_type = 0
    run()

    runs = 500000
    test_type = 0
    run()

    runs = 100000
    test_type = 1
    run()

    runs = 500000
    test_type = 1
    run()

    root = 0

    runs = 1000
    test_type = 1
    run()

    runs = 5000
    test_type = 1
    run()

    runs = 1000
    test_type = 2
    run()

    runs = 5000
    test_type = 2
    run()

    runs = 100000
    test_type = 3
    run()

    runs = 500000
    test_type = 3
    run()

    for i in range(0,10):
        cur_times = []

        for list in times:
            cur_times.append(list[i])

        append_list_as_row(write_obj, cur_times)