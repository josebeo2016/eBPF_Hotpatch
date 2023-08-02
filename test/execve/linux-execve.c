/**********************************************************************
* linux-execve.c
**********************************************************************/

/* CAUTION: all error checking omitted for clarity */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>

int main(void) 
{

    char cmd[] = "/usr/bin/ls";

    char * arg_vec[] = {"ls", "-l", NULL};
    char * env_vec[] = {NULL};

    printf("Start of execve call %s:\n", cmd);
    printf("==========================================================\n");

    int retval;
    retval = -EPERM;
    if(execve(cmd, arg_vec, env_vec) < 0){
        printf("program exit with an error\n");
        return retval;
    }

    printf("program exit without an error\n");

    return 0;
}