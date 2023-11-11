/*
C++ Thread Launch File
Function to load thread body functions from .so file and launch them as pthreads

@author: EthanMayer
*/

// Includes
#include <mach/thread_act.h>
#include <pthread.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include <dlfcn.h>
#include <charconv>

// Define thread_policy_set function for MacOS scheduler API
kern_return_t	thread_policy_set(
					thread_t			thread,
					thread_policy_flavor_t		flavor,
					thread_policy_t			policy_info,
					mach_msg_type_number_t		count);

// Policy_get function not used
// kern_return_t	thread_policy_get(
// 					thread_t			thread,
// 					thread_policy_flavor_t		flavor,
// 					thread_policy_t			policy_info,
// 					mach_msg_type_number_t		*count,
// 					boolean_t			*get_default);

// Struct for containing pthread parameter data
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

// Loads thread body functions from .so shared library and launches them as pthreads
// Extern C to avoid C++ name mangling so it can be loaded from .so
extern "C" int launch(int runs, int test_type = 0, int print = 0, int root = 0) {
    pthread_t t1;
    pthread_t t2;
    arg_array arg1, arg2;

    // MacOS set CPU affinity for this function on core 2
    mach_port_t mach_thread_main = pthread_mach_thread_np(pthread_self());
    thread_affinity_policy_data_t policyData_main = { 2 };
    thread_policy_set(mach_thread_main, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData_main, 1);

    if (print) { std::cout << "Main: Process ID: " << getpid() << std::endl; }

    if (print) { std::cout << "Runs: " << runs << " Work: " << test_type << " Print: " << print << std::endl; }

    // Load thread body functions from .so file
    const char* libpath = "threadBody.so";
    void* libhandle = dlopen(libpath, RTLD_LAZY);

    if (libhandle == NULL) {
        error("Main: Could not open shared library in launch.cpp");
    }

    typedef void* (*fptr)();

    void* thread1 = dlsym(libhandle, "thread1");

    // Setup test parameters for thread 1
    arg1.addr = "ipc://part_TEST1_control";
    arg1.runs = runs;
    arg1.test_type = test_type;
    arg1.print = print;
    arg1.root = root;

    // Create first pthread
    if (pthread_create(&t1, NULL, (void * _Nullable (* _Nonnull)(void * _Nullable))thread1, &arg1) == -1) {
        error("Main: Could not create thread in launch.cpp");
    }

    // Set CPU core affinity for first thread on core 3
    mach_port_t mach_thread1 = pthread_mach_thread_np(t1);
    thread_affinity_policy_data_t policyData1 = { 3 };
    thread_policy_set(mach_thread1, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData1, 1);

    // Setup test parameters for thread 2
    arg2.addr = "ipc://part_TEST2_control";
    arg2.runs = runs;
    arg2.test_type = test_type;
    arg2.print = print;
    arg2.root = root;

    // Create second pthread
    if (pthread_create(&t2, NULL, (void * _Nullable (* _Nonnull)(void * _Nullable))thread1, &arg2) == -1) {
        error("Main: Could not create thread in launch.cpp");
    }

    // Set CPU core affinity for second thread on core 4
    mach_port_t mach_thread2 = pthread_mach_thread_np(pthread_self());
    thread_affinity_policy_data_t policyData2 = { 4 };
    thread_policy_set(mach_thread2, THREAD_AFFINITY_POLICY, (thread_policy_t)&policyData2, 1);

    if (print) { std::cout << "Joining Threads" << std::endl; }

    // Wait for threads to join
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    if (print) { std::cout << "launch.cpp Exiting" << std::endl; }

    // Return and let Python know threads are finished
    return 0;
}