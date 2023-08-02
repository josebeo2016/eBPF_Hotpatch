/**********************************************************************
* linux-chmod.c
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
    char name[] = "test chmod";
    FILE * fp;
    int fd = open(name, O_RDWR | O_CREAT, 0755);
    fp = fdopen(fd, "w");
    fprintf(fp, "the permission if this file should be changed.\n");

    unsigned short change_mode;
    change_mode = 0777;

    int retval;
    retval = -EPERM;
    if (chmod(name, change_mode) < 0){
        printf("program exit with an error\n");
        return retval;
    }

    printf("program exit without an error\n");

    return 0;
}