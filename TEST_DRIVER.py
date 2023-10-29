from TEST import main
from statistics import median, mean, stdev
import numpy as np
import sys

PYTHON = 0
CPP = 1

runs = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
test_type = int(sys.argv[2]) if len(sys.argv) > 2 else 0
debug = int(sys.argv[3]) if len(sys.argv) > 3 else 0
root = int(sys.argv[4]) if len(sys.argv) > 4 else 1
tests = int(sys.argv[5]) if len(sys.argv) > 5 else 10

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
print("Debug Print: " + str(bool(debug)))
print("Square Root Fib: " + str(bool(root)))
print("===================================")

print("===================================")
print("Running PURE PYTHON Tests...")
times = []

for i in range(tests):
    times.append(main(PYTHON, runs, test_type, debug, root))

times = list(np.around(np.array(times), 3))

median1 = round(median(times), 3)
mean1 = round(mean(times), 3)
std1 = round(stdev(times), 3)

print("Median time (Python): " + str(median1))
print("Mean time (Python): " + str(mean1))
print("Standard Deviation (Python): " + str(std1))
print("All times (Python): " + str(times))

print("===================================")
print("Running PYTHON + C++ Tests...")
times = []

for i in range(tests):
    times.append(main(CPP, runs, test_type, debug, root))

times = list(np.around(np.array(times), 3))

median2 = round(median(times), 3)
mean2 = round(mean(times), 3)
std2 = round(stdev(times), 3)

print("Median time (Python + C++): " + str(median2))
print("Mean time (Python + C++): " + str(mean2))
print("Standard Deviation (Python + C++): " + str(std2))
print("All times (Python + C++): " + str(times))

speedup = round(((mean2 - mean1) / mean1 * 100), 3)
print("Average runtime difference: " + str(speedup) + "%")