# Leveraging Compiled Languages to Optimize Python Frameworks
# Master's Thesis Research
#   
# Build Script
# This is the script used to build the C++ component of the project and bundle the compiled code into a shared library.
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

# Make and clean build folder
mkdir build
rm -rf ~/build/*

# Compile C code
echo "====Compiling C++ code...===="
clang++ -std=c++17 -stdlib=libc++ -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk -I /opt/homebrew/Cellar/zeromq/4.3.4/include -I /opt/homebrew/Cellar/cppzmq/4.10.0/include -c launch.cpp -o build/launch.o
clang++ -std=c++17 -stdlib=libc++ -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk -I /opt/homebrew/Cellar/zeromq/4.3.4/include -I /opt/homebrew/Cellar/cppzmq/4.10.0/include -I /opt/homebrew/Cellar/nlohmann-json/3.11.2/include -c threadBody.cpp -o build/threadBody.o

# Bundle compiled C code into .so
echo "====Bundling C++ code...===="
clang++ -bundle -undefined dynamic_lookup -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk build/launch.o -o launch.so
clang++ -bundle -undefined dynamic_lookup -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk build/threadBody.o -o threadBody.so