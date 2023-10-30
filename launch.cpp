/*
C++ Thread Launch File
Created on Sept. 21, 2023

@author: EthanMayer
*/

#include <mach/thread_act.h>
#include <pthread.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include <dlfcn.h>
#include <charconv>

kern_return_t	thread_policy_set(
					thread_t			thread,
					thread_policy_flavor_t		flavor,
					thread_policy_t			policy_info,
					mach_msg_type_number_t		count);

// kern_return_t	thread_policy_get(
// 					thread_t			thread,
// 					thread_policy_flavor_t		flavor,
// 					thread_policy_t			policy_info,
// 					mach_msg_type_number_t		*count,
// 					boolean_t			*get_default);

typedef struct {
    std::string addr;
    int runs;
    int test_type;
    int print;
    int root;
} arg_array;

// Error handling
void error(std::string msg) {
    std::cout << msg << ": " << std::strerror(errno) << std::endl;
    exit(-1);
}

extern "C" int launch(int runs, int test_type = 0, int print = 0, int root = 0) {
    pthread_t t1;
    pthread_t t2;
    arg_array arg1, arg2;

    mach_port_t mach_thread_main = pthread_mach_thread_np(pthread_self());
    thread_affinity_policy_data_t policyData_main = { 2 };
    thread_policy_set(mach_thread_main, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData_main, 1);

    // int print = std::atoi(argv[3]);

    if (print) { std::cout << "Main: Process ID: " << getpid() << std::endl; }

    if (print) { std::cout << "Runs: " << runs << " Work: " << test_type << " Print: " << print << std::endl; }

    const char* libpath = "threadBody.so";
    void* libhandle = dlopen(libpath, RTLD_LAZY);

    if (libhandle == NULL) {
        error("Main: Could not open shared library in launch.cpp");
    }

    typedef void* (*fptr)();

    void* thread1 = dlsym(libhandle, "thread1");

    arg1.addr = "ipc://part_TEST1_control";
    arg1.runs = runs; //std::atoi(argv[1]);
    arg1.test_type = test_type; //std::atoi(argv[2]);
    arg1.print = print; //std::atoi(argv[3]);
    arg1.root = root;

    if (pthread_create(&t1, NULL, (void * _Nullable (* _Nonnull)(void * _Nullable))thread1, &arg1) == -1) {
        error("Main: Could not create thread in launch.cpp");
    }

    mach_port_t mach_thread1 = pthread_mach_thread_np(t1);
    thread_affinity_policy_data_t policyData1 = { 3 };
    thread_policy_set(mach_thread1, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData1, 1);

    arg2.addr = "ipc://part_TEST2_control";
    arg2.runs = runs; //std::atoi(argv[1]);
    arg2.test_type = test_type; //std::atoi(argv[2]);
    arg2.print = print; //std::atoi(argv[3]);
    arg2.root = root;

    if (pthread_create(&t2, NULL, (void * _Nullable (* _Nonnull)(void * _Nullable))thread1, &arg2) == -1) {
        error("Main: Could not create thread in launch.cpp");
    }

    mach_port_t mach_thread2 = pthread_mach_thread_np(pthread_self());
    thread_affinity_policy_data_t policyData2 = { 4 };
    thread_policy_set(mach_thread2, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData2, 1);

    if (print) { std::cout << "Joining Threads" << std::endl; }

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    if (print) { std::cout << "launch.cpp Exiting" << std::endl; }

    return 0;

    // pthread_exit(NULL);
}