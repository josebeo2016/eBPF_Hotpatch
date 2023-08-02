/**********************************************************************
* ex_setreuid.c                                                       *
* exmple source – set real user id and effective user id              *
**********************************************************************/

// Reference from: http://ehpub.co.kr/tag/seteuid/
// Usage: ./linux-seteuid 1000 0 (two arguments)

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>

int main(int argc, char **argv)
{
    if(argc != 3)
    {
        printf("Usage: %s [real user id] [effective user id]\n",argv[0]);
        printf("*** user id is number ***\n");
        return 1;
    }
 
    printf("real user id:%d effective user id:%d\n",getuid(), geteuid());
    
	int retval;
	uid_t ruid=atoi(argv[1]);
    uid_t euid = atoi(argv[2]);
    
	retval = -EPERM;
	if(setreuid(ruid,euid)==0)
    {
        printf("real user id:%d effective user id:%d\n",getuid(), geteuid());
    }
    else
    {
		return retval;
    }
 
	printf("exit without error\n");
    return 0;
}