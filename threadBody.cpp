/*
Leveraging Compiled Languages to Optimize Python Frameworks
Master's Thesis Research

C++ Thread Body File
This file contains the thread body functions for C++ pthreads.

@author: EthanMayer

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
*/

// Includes
#include <pthread.h>
#include <iostream>
#include <zmq.hpp>
#include <unistd.h>
#include <nlohmann/json.hpp>

// Struct for containing pthread parameter data
typedef struct {
    std::string addr;
    int runs;
    int test_type;
    int print;
    int root;
} arg_array;

// Iterative Fibonacci function implementation for C++
int fib(int n) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }

    int prevPrevNum, prevNum = 0, curNum = 1;

    for (int i = 2; i <= n; i++) {
        prevPrevNum = prevNum;
        prevNum = curNum;
        curNum = prevNum + prevPrevNum;
    }

    return curNum;
}

// Recursive Fibonacci function implementation for C++
int fib_recursive(int n) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }

    return (fib_recursive(n - 2) + fib_recursive(n - 1));
}

// Memory allocation function implementation for C++
void memory_alloc() {
    int* ptrs[100];

    // Allocate a size 100 array of 4096 bytes
    for (int i = 0; i < 100; i++) {
        ptrs[i] = (int*)malloc(4096);
    }

    // Free the memory allocations
    for (int i = 0; i < 100; i++) {
        free(ptrs[i]);
    }
}

// Thread body function to run tests
// Extern C to avoid C++ name mangling so it can be loaded from .so
extern "C" void* thread1(arg_array arg) {
    pthread_t tid = pthread_self();
    if (arg.print) { std::cout << "Thread: Process ID: " << getpid() << " Thread ID: " << tid << std::endl; }
    if (arg.print) { std::cout << "Thread: arg.addr: " << arg.addr << " arg.runs: " << arg.runs << std::endl; }

    // Setup ZMQ PAIR socket to communicate with Python main thread
    zmq::context_t ctx;
    zmq::socket_t sock(ctx, ZMQ_PAIR);
    sock.connect(arg.addr);

    // Forward declaration of all message variables
    int i = 0;
    nlohmann::json send;
    std::string send_str;
    zmq::message_t reply;
    nlohmann::json reply_json;
    int x = 0;

    // Test run loop
    while (i < arg.runs) {

        // If no work, just send back simple JSON string message
        if (arg.test_type == 0) {
            nlohmann::json send_no_fib;
            send_no_fib["Contents"] = "Ready";
            send = send_no_fib;

        } else if (arg.test_type == 1) {

            // If light math work, send iterative Fibonacci of square root of message number
            if (arg.root) {
                x = fib((int)std::sqrt(i));

            // If heavy math work, send iterative Fibonacci of message number
            } else {
                x = fib((int)i);
            }
            std::string send_fib_str = "Fibonacci number of sqrt(" + std::to_string(i) + ")";
            nlohmann::json send_fib;
            send_fib[send_fib_str] = x;
            send = send_fib;

        } else if (arg.test_type == 2) {

            // If light function call work, send recursive Fibonacci of square root of message number
            if (arg.root) {
                x = fib_recursive((int)std::sqrt(i));

            // If heavy function call work, send recursive Fibonacci of message number
            } else {
                x = fib_recursive((int)i);
            }
            std::string send_fib_str = "Recursive Fibonacci number of sqrt(" + std::to_string(i) + ")";
            nlohmann::json send_recur_fib;
            send_recur_fib[send_fib_str] = x;
            send = send_recur_fib;

        // If memory allocation work, allocate memory before sending message back
        } else if (arg.test_type == 3) {
            memory_alloc();
            nlohmann::json send_mem;
            send_mem["Memory Allocated"] = "4096 * 100";
            send = send_mem;
        }
        
        // Send message to main thread
        send_str = send.dump();
        if (arg.print) { std::cout << "Thread: sending: " << send_str << std::endl; }
        zmq::message_t query(send_str.length());
        std::memcpy(query.data(), (send_str.c_str()), (send_str.size()));
        sock.send(query, zmq::send_flags::none);

        // Receive message from main thread
        zmq::recv_result_t e = sock.recv(reply, zmq::recv_flags::none);
        reply_json = nlohmann::json::parse(reply.to_string());
        if (arg.print) { std::cout << "Thread: reply received: \n" << reply_json.dump(4) << std::endl; }
        if (arg.print) { std::cout << "Value of Point: " << reply_json["__value__"]["values"][1] << std::endl; }

        i = (int)reply_json["__value__"]["values"][1];
    }
    
    // Close ZMQ socket and context
    sock.close();
    ctx.close();

    if (arg.print) { std::cout << "Thread: Exiting" << std::endl; }

    // Exit thread
    pthread_exit(NULL);
}
