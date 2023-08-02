/**********************************************************************
* linux-chmod.c

reference: http://www.vishalchovatiya.com/clone-system-call-example/
**********************************************************************/

/* CAUTION: all error checking omitted for clarity */
#include <errno.h>
#include <fcntl.h>
#include <linux/sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>

#define STACK 8192

int do_something(){
        printf("Child pid : %d\n", getpid());
        return 0;
}

int main() {
        void *stack = malloc(STACK);    // Stack for new process
        if(!stack) {
                perror("Malloc Failed");
                exit(0);
        }
        if( clone( &do_something, (char *)stack + STACK, CLONE_VM, 0) < 0 ){
                perror("Clone Failed");
                exit(0);
        }
        printf("Parent pid : %d\n", getpid());
        sleep(1);       // Add sleep so we can she both processes output
        free(stack);
        return 0;
}