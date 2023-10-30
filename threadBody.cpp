/*
C++ Thread Body File
Created on Sept. 21, 2023

@author: EthanMayer
*/

#include <pthread.h>
#include <iostream>
#include <zmq.hpp>
#include <unistd.h>
#include "json.hpp"

typedef struct {
    std::string addr;
    int runs;
    int test_type;
    int print;
    int root;
} arg_array;

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

int fib_recursive(int n) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }

    return (fib_recursive(n - 2) + fib_recursive(n - 1));
}

void memory_alloc() {
    int* ptrs[100];

    for (int i = 0; i < 100; i++) {
        ptrs[i] = (int*)malloc(4096);
    }

    for (int i = 0; i < 100; i++) {
        free(ptrs[i]);
    }
}

extern "C" void* thread1(arg_array arg) {
    pthread_t tid = pthread_self();
    if (arg.print) { std::cout << "Thread: Process ID: " << getpid() << " Thread ID: " << tid << std::endl; }
    if (arg.print) { std::cout << "Thread: arg.addr: " << arg.addr << " arg.runs: " << arg.runs << std::endl; }

    // CppComponent testComp(NULL);

    // std::cout << "Test Component Name: " << testComp.getName() << std::endl;

    zmq::context_t ctx;
    zmq::socket_t sock(ctx, ZMQ_PAIR);
    sock.connect(arg.addr);

    int i = 0;
    nlohmann::json send;
    std::string send_str;
    zmq::message_t reply;
    nlohmann::json reply_json;
    int x = 0;

    while (i < arg.runs) {

        if (arg.test_type == 0) {
            nlohmann::json send_no_fib;
            send_no_fib["Contents"] = "Ready";
            send = send_no_fib;
        } else if (arg.test_type == 1) {
            if (arg.root) {
                x = fib((int)std::sqrt(i));
            } else {
                x = fib((int)i);
            }
            std::string send_fib_str = "Fibonacci number of sqrt(" + std::to_string(i) + ")";
            nlohmann::json send_fib;
            send_fib[send_fib_str] = x;
            send = send_fib;
        } else if (arg.test_type == 2) {
            if (arg.root) {
                x = fib_recursive((int)std::sqrt(i));
            } else {
                x = fib_recursive((int)i);
            }
            std::string send_fib_str = "Recursive Fibonacci number of sqrt(" + std::to_string(i) + ")";
            nlohmann::json send_recur_fib;
            send_recur_fib[send_fib_str] = x;
            send = send_recur_fib;
        } else if (arg.test_type == 3) {
            memory_alloc();
            nlohmann::json send_mem;
            send_mem["Memory Allocated"] = "4096 * 100";
            send = send_mem;
        }
        
        send_str = send.dump();
        if (arg.print) { std::cout << "Thread: sending: " << send_str << std::endl; }
        zmq::message_t query(send_str.length());
        std::memcpy(query.data(), (send_str.c_str()), (send_str.size()));
        sock.send(query, zmq::send_flags::none);

        zmq::recv_result_t e = sock.recv(reply, zmq::recv_flags::none);
        reply_json = nlohmann::json::parse(reply.to_string());
        if (arg.print) { std::cout << "Thread: reply received: \n" << reply_json.dump(4) << std::endl; }
        if (arg.print) { std::cout << "Value of Point: " << reply_json["__value__"]["values"][1] << std::endl; }
        i = (int)reply_json["__value__"]["values"][1];
    }
    
    sock.close();
    ctx.close();

    if (arg.print) { std::cout << "Thread: Exiting" << std::endl; }

    pthread_exit(NULL);
}
