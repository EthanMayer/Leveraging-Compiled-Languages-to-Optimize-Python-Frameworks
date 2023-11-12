# Leveraging-Compiled-Languages-to-Optimize-Python-Frameworks
This repository is for the research and implementation for my thesis "Leveraging Compiled Languages to Optimize Python Frameworks". This is a continuation and compartmentalization of work done in my riaps-pycom fork.


# Leveraging-Compiled-Languages-to-Optimize-Python-Frameworks
This repository contains the implementation code used for my Master's Thesis, "Leveraging Compiled Languages to Optimize Python Frameworks". This work is a culmination of work done in several previous repositories, including [MS-Research](https://github.com/EthanMayer/MS-Research) and my two fork branches, `cython` and `cpp_comop`, of [riaps-pycom](https://github.com/EthanMayer/riaps-pycom).


## Contents

* [Authors](#authors)
* [Background](#background)
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)
## Authors

- [@EthanMayer](https://github.com/EthanMayer)


## Background

Abstract:
This thesis proposes methods of improving the performance of Python frameworks by incorporating the use of compiled languages. The framework in question in this research is RIAPS, a large, embedded software framework, written entirely in Python, whose purpose is to host distributed developer applications for the smart grid. Due to the nature of the Python programming language, fast performance is traded for ease of use and accessibility. Python’s single-core nature prevents it from taking advantage of the abundance of independent cores found on modern CPUs. However, novel techniques are investigated to speed up Python frameworks such as this. Incorporating compiled languages, such as Cython or C/C++, is done to determine which is the ideal solution to enhance the performance of frameworks such as RIAPS. By using these faster, compiled languages, the performance-centric portions of RIAPS can be sped up significantly. Prototype implementations are created for the investigated solutions, and they are then tested in a proof-of-concept fashion in order to quantify the potential performance improvement. Many different tests with varying workloads are performed to achieve a wide range of data representative of many different potential situations the framework may encounter. The results of these tests are analyzed to determine not only if the proposed solution is an effective speedup, but also to quantitatively show how much of an improvement can be achieved in the varying types of workloads tested.

To learn more about RIAPS, visit:

* https://riaps.github.io
* https://riaps.isis.vanderbilt.edu

## Setup

This project was originally run with Python3.11 on MacOS. In order to install Python 3.11 using Homebrew, and other external libraries used for the C++ portion of this project, run:

`xargs brew install < brew_requirements.txt`

This project relies on several external Python libraries listed in `requirements.txt`. To install them, run:

`pip install -r pip_requirements.txt`

The included `build.sh` Bash script is used to automate the building and compiling necessary to run the project. To use it, run:

`bash build.sh`

If this completes successfully, the project is ready to be run (see [Usage](#usage)). If there are errors, see below.

**Additional Information**

This research test implementation is primarily made up of two different implementations: the Python Control Implementation and the Python + C++ Prototype. Both perform the exact same functions for the purpose of benchmarking.

The Python Control Implementation is made of pure Python code. All threads used are Python threads, and thus do not trul execute in parallel.

The Python + C++ Prototype uses a Python main thread to load a C++ function from a .so shared library. This function then loads more functions from the .so file and launches them as pthreads. These threads then do the same functions as the Python threads mentioned above.
## Usage

The driver is meant to setup and run a test suite for this thesis. Although at one point command line arguments were supported, they currently do nothing as all 10 tests are setup specifically within the driver code. To start the driver, and thus run the tests, run:

`python3.11 TEST_DRIVER.py`

Within `TEST_DRIVER.py`, many different test parameters can be set. This includes:

`runs`: number of runs per test (int)
`test_type`: which test to run (specifically, which work to do between messages) (int)
`root`: whether to take the square root of the number being used in mathematical operations between messages (Bool)
`debug`: enable debug printing (otherwise known as verbose mode) (Bool)
`tests`: how many times to run each test per language (int)

When finished, a CSV file containing all test data will be deposited in the `data/` folder. The test data will be under the relevant column titles specified in the driver script.

## License

Copyright 2023 Ethan Mayer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.