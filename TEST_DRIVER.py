# Test Driver
# Created on October 16, 2023
#
# @author: EthanMayer
#

# Imports
from TEST import main
from statistics import median, mean, stdev
import numpy as np
import sys
import os
from csv import writer
import os.path
import time

# Constants
PYTHON = 0
CPP = 1

# Forward declaration for global list
times = []

# Command line arguments (if any)
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

# Run the tests
def run():
    global times
    times1 = []
    times2 = []

    # Test parameters for both Python Control Implementation and Python + C++ Prototype
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
    if (test_type == 1 or test_type == 2): print("Square Root Fib: " + str(bool(root)))
    print("===================================")

    ############### Run tests with Python Control Implementation ###############
    print("===================================")
    print("Running PURE PYTHON Tests...")

    # For each test run, append the time to the end of the list
    for i in range(tests):
        times1.append(main(PYTHON, runs, test_type, debug, root))

    # Round all times in the list to 3 decimal places
    times1 = list(np.around(np.array(times1), 3))

    # Append all rounded times from current test to the global list
    times.append(times1)

    # Calculate statistical information over all runs for the current test
    median1 = round(median(times1), 3)
    mean1 = round(mean(times1), 3)
    std1 = round(stdev(times1), 3)

    # Append this test's mean time to the global list (for CSV formatting purposes)
    times.append([mean1]*10)

    # Report test results to console
    print("Median time (Python): " + str(median1))
    print("Mean time (Python): " + str(mean1))
    print("Standard Deviation (Python): " + str(std1))
    print("All times (Python): " + str(times1))

    ############### Run tests with Python + C++ Prototype ###############
    print("===================================")
    print("Running PYTHON + C++ Tests...")

    # For each test run, append the time to the end of the list
    for i in range(tests):
        times2.append(main(CPP, runs, test_type, debug, root))

    # Round all times in the list to 3 decimal places
    times2 = list(np.around(np.array(times2), 3))

    # Append all rounded times from current test to the global list
    times.append(times2)

    # Calculate statistical information over all runs for the current test
    median2 = round(median(times2), 3)
    mean2 = round(mean(times2), 3)
    std2 = round(stdev(times2), 3)

    # Append this test's mean time to the global list (for CSV formatting purposes)
    times.append([mean2]*10)

    # Report test results to console
    print("Median time (Python + C++): " + str(median2))
    print("Mean time (Python + C++): " + str(mean2))
    print("Standard Deviation (Python + C++): " + str(std2))
    print("All times (Python + C++): " + str(times2))

    # Calculate percentage speedup achieved by Python + C++ prototype and report it
    speedup = round(((mean2 - mean1) / mean1 * 100), 3)
    print("Average runtime difference: " + str(speedup) + "%")

# os.sched_setaffinity(0, 0) # ONLY FOR LINUX, DOES NOT WORK ON MACOS SO UNUSED

# Initialize CSV file for recording test data
if not os.path.exists("data"):
    os.makedirs("data")
timestr = time.strftime("%Y%m%d-%H%M%S")
file_name = "data/LOG_" + timestr + ".csv"
open(file_name, 'w+', newline='')

# Open CSV file and try to append
with open(file_name, 'a+', newline='') as write_obj:
    try:
        # Write tests as column titles to CSV
        csvTitles = ["Python - 100k", "Average", "C++ - 100k", "Average", "Python - 500k", "Average", "C++ - 500k", "Average", "Python - 100k, Sqrt Fib", "Average", "C++ - 100k, Sqrt Fib", "Average", "Python - 500k, Sqrt Fib", "Average", "C++ - 500k, Sqrt Fib", "Average", "Python - 1k, Fib", "Average", "C++ - 1k, Fib", "Average", "Python - 5k, Fib", "Average", "C++ - 5k, Fib", "Average", "Python - 10, Functions", "Average", "C++ - 10, Functions", "Average", "Python - 40, Functions", "Average", "C++ - 40, Functions", "Average", "Python - 100k, Memory", "Average", "C++ - 100k, Memory", "Average", "Python - 500k, Memory", "Average", "C++ - 500k, Memory", "Average"]
        append_list_as_row(write_obj, csvTitles)
            
        # Set test parameters
        debug = 0
        tests = 10
        root = 1

        runs = 100000
        test_type = 0
        run() # Run test

        # Set test parameters
        runs = 500000
        test_type = 0
        run() # Run test

        # Set test parameters
        runs = 100000
        test_type = 1
        run() # Run test

        # Set test parameters
        runs = 500000
        test_type = 1
        run() # Run test

        # Set test parameters
        root = 0

        runs = 1000
        test_type = 1
        run() # Run test

        # Set test parameters
        runs = 5000
        test_type = 1
        run() # Run test

        # Set test parameters
        runs = 10
        test_type = 2
        run() # Run test

        # Set test parameters
        runs = 40
        test_type = 2
        run() # Run test

        # Set test parameters
        runs = 100000
        test_type = 3
        run() # Run test

        # Set test parameters
        runs = 500000
        test_type = 3
        run() # Run test

        # Write all test results to CSV file
        for i in range(0,10):
            cur_times = []

            for list in times:
                cur_times.append(list[i])

            append_list_as_row(write_obj, cur_times)

    # Stop logging on keyboard interrupt and gracefully exit
    except KeyboardInterrupt:
        if debug: print("\nStopping logging due to keyboard interrupt") #ctrl-c

        # Write as much data as we have
        for i in range(0,10):
            cur_times = []

            for list in times:
                cur_times.append(list[i])

            append_list_as_row(write_obj, cur_times)

    # Print exception that occurred
    except Exception as e:
        print("\nTEST EXCEPTION:\n" + str(e))

        # Write as much data as we have
        for i in range(0,10):
            cur_times = []

            for list in times:
                cur_times.append(list[i])

            append_list_as_row(write_obj, cur_times)